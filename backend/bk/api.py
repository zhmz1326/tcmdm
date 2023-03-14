from bk import bk_blueprint
from flask import request

from util import utils
from util import consts
from itertools import product
import json
import pandas as pd

import bk.graph as graph
import bk.bkalgorithm as bkalgorithm

@bk_blueprint.route('/datamining', methods=['POST'])
def datamine():
    formdata = json.loads(request.form.get('data'))
    if 'threshold' not in formdata:
        threshold = 0
    else:
        threshold = int(formdata['threshold'])

    if 'cbwn' not in formdata:
        return utils.error(400, '请输入置信度（CBWN）')
    if 'sbc' not in formdata:
        return utils.error(400, '请输入支持度的α水平值（SBCα）')
    if 'draw_threshold' not in formdata:
        return utils.error(400, '绘制图形最小共现数')

    cbwn = float(formdata['cbwn'])
    sbc = float(formdata['sbc'])
    draw_threshold = int(formdata['draw_threshold'])

    stop_words = set()
    if 'stopWords' in formdata:
        stopWords = formdata['stopWords']
        splits = stopWords.split(' ')
        for split in splits:
            stop_words.add(split)

    fileStorage = request.files['file']
    tempFile = consts.TEMP_DIR + fileStorage.filename
    fileStorage.save(tempFile)

    df = pd.read_csv(tempFile, names=["symptom", "tcm"])
    symptom = df['symptom']
    tcm = df['tcm']

    # 数据加载
    symptom_set = set()  # 症状中药集
    tcm_set = set()  # 症状中药集
    symptom_tcm_set = set() # 症状中药集
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
                symptom_tcm_set.add(split.strip())
                symptom_set.add(split.strip())
        symptom_data.append(filteredData)

    for data in tcm:
        splits = data.split(',')
        filteredData = []
        for split in splits:
            if len(split) == 0:
                continue
            if split not in stop_words: # 过滤高频词
                filteredData.append(split.strip())
                symptom_tcm_set.add(split.strip()) # 加入中药集
                tcm_set.add(split.strip())
        tcm_data.append(filteredData)

    size = len(tcm_data)
    symptom_tcm_data = []
    for i in range(0, size):
        data = symptom_data[i] + tcm_data[i]
        symptom_tcm_data.append(data)

    symptom_tcm_id_dict = {}
    id_symptom_tcm_dict = {}
    index = 0
    for data in symptom_tcm_set:
        index += 1
        symptom_tcm_id_dict[data] = index
        id_symptom_tcm_dict[index] = data

    tcm_rules, tcm_img = bkanalysis(tcm_data, threshold, cbwn, sbc, symptom_tcm_id_dict, id_symptom_tcm_dict, draw_threshold)
    symptom_rules, symptom_img = bkanalysis(symptom_data, threshold, cbwn, sbc, symptom_tcm_id_dict, id_symptom_tcm_dict, draw_threshold)
    mix_rules, mix_img = bkanalysis(symptom_tcm_data, threshold, cbwn, sbc, symptom_tcm_id_dict, id_symptom_tcm_dict, draw_threshold)

    export_excel(tcm_rules, symptom_rules, mix_rules)
    bkResult = {'tcm_rules': tcm_rules, 'symptom_rules': symptom_rules, 'mix_rules': mix_rules,
                'tcm_img': tcm_img, 'symptom_img': symptom_img, 'mix_img': mix_img }

    return utils.success(bkResult)

import time
def export_excel(tcm_rules, symptom_rules, mix_rules):
    filename = consts.STATIC_DIR + str(time.time()) + '.xls'
    symptom_rules_df = pd.DataFrame(symptom_rules)
    tcm_rules_df = pd.DataFrame(tcm_rules)
    mix_rules_df = pd.DataFrame(mix_rules)

    with pd.ExcelWriter(
        filename,
        # datetime_format='YYYY-MM-DD'  # 只显示年月日, 不显示时分秒
    ) as writer:
        symptom_rules_df.to_excel(writer, sheet_name='核心症状')
        tcm_rules_df.to_excel(writer, sheet_name='核心药对')
        mix_rules_df.to_excel(writer, sheet_name='中药-症状联合极大团')

def bkanalysis(data, threshold, cbwn, sbc, symptom_tcm_id_dict, id_symptom_tcm_dict, draw_threshold):
    pair_dict = {}
    for one in data:
        tuple_list = list(product(one, one))
        for temp in tuple_list:
            if temp[0] < temp[1]:
                key = temp[0] + ',' + temp[1]
                if key in pair_dict:
                    pair_dict[key] += 1
                else:
                    pair_dict[key] = 1

    ADT = graph.graph()

    draw_data = []
    for key in pair_dict:
        splits = key.split(",")
        draw_line = [splits[0], splits[1], pair_dict[key]]
        draw_data.append(draw_line)
        if pair_dict[key] >= threshold:
            ADT.append(symptom_tcm_id_dict[splits[0]], symptom_tcm_id_dict[splits[1]], pair_dict[key])

    img = draw_graph(draw_data, draw_threshold)

    ADT.reveal()
    ADT.mat()

    result = bkalgorithm.bron_kerbosch(ADT, P=set(ADT.vertex()))

    rules = []
    result_list = list(result)
    index = 0
    for s in result_list:
        if len(s) < 2:
            continue

        rule = ''
        rule_set = set()
        sum = 0
        filtered_rule_count = 0
        for i in s:
            value = id_symptom_tcm_dict[i]
            rule += value + " "
            rule_set.add(value)

        for line in data:
            intersection = set(line) & rule_set # 交集
            rate = len(intersection) / len(line)
            sum += rate
            if rate >= sbc:
                filtered_rule_count += 1
        current_cbwn = sum / len(data)
        current_sbc = filtered_rule_count / len(data)

        if current_cbwn >= cbwn and current_sbc > 0:
            index += 1
            rule_dict = {'index': index, 'rule': rule, 'count': len(s), 'cbwn': "%0.2f" % current_cbwn, 'sbc': "%0.2f" % current_sbc}
            rules.append(rule_dict)
    return rules, img

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
def draw_graph(draw_data, draw_threshold):
    # 设置字体为楷体
    matplotlib.rcParams['font.sans-serif'] = ['KaiTi']

    G = nx.Graph()

    for line in draw_data:
        if line[2] > draw_threshold:
            G.add_edge(line[0], line[1], weight=line[2])

    threshold = draw_threshold * 2 # 50
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > threshold]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= threshold]
    edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])

    # pos = nx.spring_layout(G, seed=1)  # positions for all nodes - seed for reproducibility
    pos = nx.shell_layout(G)
    # pos = nx.random_layout(G)
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='#FFFFFF')

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1, label='weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_family="sans-serif")
    nx.draw_networkx_edges(
        G, pos, edgelist=esmall, width=1, alpha=0.5, edge_color="b", style="dashed", label='weight'
    )

    # labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    filename = str(time.time()) + '.jpg'
    img = consts.STATIC_DIR + filename
    plt.savefig(img) # 保存
    plt.clf()
    # plt.show()
    return filename
