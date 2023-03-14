from apriori import apriori_blueprint
from flask import jsonify
from flask import request

from efficient_apriori import apriori
from util import utils
from util import consts
import csv
import json
import pandas as pd

@apriori_blueprint.route('/datamining', methods=['POST'])
def datamine():
    formdata = json.loads(request.form.get('data'))
    if 'min_support' not in formdata:
        return utils.error(400, '请输入最小支持度')
    if 'min_confidence' not in formdata:
        return utils.error(400, '请输入最小置信度')

    stop_words = set()
    tcmSet = set() # 中药集
    if 'stopWords' in formdata:
        stopWords = formdata['stopWords']
        splits = stopWords.split(' ')
        for split in splits:
            stop_words.add(split)

    min_support_value = float(formdata['min_support'])
    min_confidence_value = float(formdata['min_confidence'])

    fileStorage = request.files['file']
    tempFile = consts.TEMP_DIR + fileStorage.filename
    fileStorage.save(tempFile)

    df = pd.read_csv(tempFile, names=["symptom", "tcm"])
    symptom = df['symptom']
    tcm = df['tcm']

    # 数据加载
    symptom_data = []
    tcm_data = []
    for data in symptom:
        splits = data.split(',')
        filteredData = []
        for split in splits:
            if len(split) == 0:
                continue
            if split not in stop_words: # 过滤高频词
                filteredData.append(split.strip())
        symptom_data.append(filteredData)
    for data in tcm:
        splits = data.split(',')
        filteredData = []
        for split in splits:
            if len(split) == 0:
                continue
            if split not in stop_words: # 过滤高频词
                filteredData.append(split.strip())
                tcmSet.add(split.strip()) # 加入中药集
        tcm_data.append(filteredData)

    size = len(tcm_data)
    symptom_tcm_data = []
    for i in range(0, size):
        data = symptom_data[i] + tcm_data[i]
        symptom_tcm_data.append(data)

    # 挖掘频繁项集和关联规则 - 症状
    symptom_itemsets, symptom_rules = do_apriori(symptom_data, min_support_value, min_confidence_value, tcmSet, False)

    # 挖掘频繁项集和关联规则 - 中药
    tcm_itemsets, tcm_rules = do_apriori(tcm_data, min_support_value, min_confidence_value, tcmSet, False)

    # 挖掘频繁项集和关联规则 - 症状和中药
    symptom_tcm_rules, tcm_symptom_rules = do_apriori(symptom_tcm_data, min_support_value, min_confidence_value, tcmSet, True)

    export_excel(symptom_itemsets, symptom_rules, tcm_itemsets, tcm_rules, symptom_tcm_rules, tcm_symptom_rules)

    aprioriResult = {}
    aprioriResult['tcm_itemsets'] = tcm_itemsets
    aprioriResult['tcm_rules'] = tcm_rules
    aprioriResult['symptom_itemsets'] = symptom_itemsets
    aprioriResult['symptom_rules'] = symptom_rules
    aprioriResult['symptom_tcm_rules'] = symptom_tcm_rules
    aprioriResult['tcm_symptom_rules'] = tcm_symptom_rules

    return utils.success(aprioriResult)

import time
def export_excel(symptom_itemsets, symptom_rules, tcm_itemsets, tcm_rules, symptom_tcm_rules, tcm_symptom_rules):
    filename = consts.STATIC_DIR + str(time.time()) + '.xls'
    symptom_itemsets_df = pd.DataFrame(symptom_itemsets)
    symptom_rules_df = pd.DataFrame(symptom_rules)

    tcm_itemsets_df = pd.DataFrame(tcm_itemsets)
    tcm_rules_df = pd.DataFrame(tcm_rules)

    symptom_tcm_rules_df = pd.DataFrame(symptom_tcm_rules)
    tcm_symptom_rules_df = pd.DataFrame(tcm_symptom_rules)

    with pd.ExcelWriter(
        filename,
        # datetime_format='YYYY-MM-DD'  # 只显示年月日, 不显示时分秒
    ) as writer:
        symptom_itemsets_df.to_excel(writer, sheet_name='症状出现频次')
        symptom_rules_df.to_excel(writer, sheet_name='症状关联规则')

        tcm_itemsets_df.to_excel(writer, sheet_name='中药出现频次')
        tcm_rules_df.to_excel(writer, sheet_name='中药关联规则')

        symptom_tcm_rules_df.to_excel(writer, sheet_name='症状-中药关联规则')
        tcm_symptom_rules_df.to_excel(writer, sheet_name='中药-症状关联规则')


def do_apriori(data, min_support_value, min_confidence_value, tcm_set, is_mix):
    size = len(data)
    raw_itemsets, raw_rules = apriori(data, min_support=min_support_value, min_confidence=min_confidence_value)

    itemsets = []
    for i in raw_itemsets:
        dict = raw_itemsets[i]
        for j in dict:
            tcm = '{}'.format(j).replace("'", ""). \
                replace("(", "").replace(",)", "").replace(")", "").replace(" ", "").replace(",", " ")
            result = {}
            result['count'] = i
            result['entity'] = tcm
            result['occurrence'] = dict[j]
            result['frequency'] = "%0.2f%%" % (dict[j] / size * 100)
            itemsets.append(result)

    rules = []
    symptom_tcm_rules = []
    tcm_symptom_rules = []
    for rule in raw_rules:
        if rule.lift <= 1.0:
            continue

        left = '{}'.format(rule.lhs).replace("'", ""). \
            replace("(", "").replace(",)", "").replace(")", "").replace(" ", "").replace(",", " ")
        right = '{}'.format(rule.rhs).replace("'", ""). \
            replace("(", "").replace(",)", "").replace(")", "").replace(" ", "").replace(",", " ")
        result = {}
        result['LHS'] = left
        result['RHS'] = right
        result['confidence'] = "%0.2f" % rule.confidence
        result['support'] = "%0.2f" % rule.support
        result['lift'] = "%0.2f" % rule.lift
        rules.append(result)

        if is_mix:
            if isAllSymptom(tcm_set, left) and isAllTCM(tcm_set, right):
                symptom_tcm_rules.append(result)
            elif isAllTCM(tcm_set, left) and isAllSymptom(tcm_set, right):
                tcm_symptom_rules.append(result)

    if is_mix:
        return symptom_tcm_rules, tcm_symptom_rules
    else:
        return itemsets, rules

def isAllTCM(tcmset, str):
    splits = str.split(' ')
    for split in splits:
        if split not in tcmset:
            return False
    return True

def isAllSymptom(tcmset, str):
    splits = str.split(' ')
    for split in splits:
        if split in tcmset:
            return False
    return True