from decision import decision_blueprint
from flask import jsonify
from flask import request

from util import utils
from util import consts
import json
import pandas as pd
import numpy as np
from sklearn import tree
import pydotplus
import os

@decision_blueprint.route('/datamining', methods=['POST'])
def datamine():
    formdata = json.loads(request.form.get('data'))
    if 'tcm' not in formdata:
        return utils.error(400, '请输入分析中药')

    tcm_analysis = formdata['tcm']

    fileStorage = request.files['file']
    tempFile = consts.TEMP_DIR + fileStorage.filename
    fileStorage.save(tempFile)

    df = pd.read_csv(tempFile, names=["symptom", "tcm"])
    symptom = df['symptom']
    tcm = df['tcm']

    symptom_data = []
    tcm_data = []
    for data in symptom:
        splits = data.split(',')
        filtered_data = []
        for split in splits:
            split = split.strip()
            if len(split) == 0:
                continue
            filtered_data.append(split)
        symptom_data.append(filtered_data)
    for data in tcm:
        splits = data.split(',')
        filtered_data = []
        for split in splits:
            split = split.strip()
            if len(split) == 0:
                continue
            filtered_data.append(split)
        tcm_data.append(filtered_data)

    df_symptoms = pd.DataFrame(symptom_data)
    df_tcms = pd.DataFrame(tcm_data)
    unique_symptoms = get_unique_list(df_symptoms)
    unique_tcms = get_unique_list(df_tcms)

    index = get_index(unique_tcms, tcm_analysis)
    if (index == -1):
        return utils.error(400, '分析中药不存在')

    mix_img = decision_analysis(df_symptoms, df_tcms, unique_symptoms, unique_tcms, index)

    decisionResult = {'mix_img': mix_img}
    return utils.success(decisionResult)

def get_index(unique_tcms, tcm):
    try:
        return unique_tcms.index(tcm)
    except:
        return -1

def get_unique_list(df):
    (row_num, col_num) = df.shape
    unique_list = []
    while col_num > 0:
        unique_list = unique_list + list(set(df[col_num - 1]))
        col_num = col_num - 1
    unique_list = list(set(unique_list))
    if '' in unique_list:
        unique_list.remove('')
    return unique_list

import time
def decision_analysis(df_symptoms, df_tcms, unique_symptoms, unique_tcms, index):
    os.environ["PATH"] += os.pathsep + consts.GRAPHVIZ_DIR
    df_symptoms_onehot = onehot_data(df_symptoms, unique_symptoms)
    df_tcms_onehot = onehot_data(df_tcms, unique_tcms)

    clf = tree.DecisionTreeClassifier(criterion='gini', random_state=50, splitter="random", max_depth=25)
    clf.fit(df_symptoms_onehot, np.array(df_tcms_onehot)[:, index])

    dot_data = tree.export_graphviz(clf, out_file=None,
                                    feature_names=unique_symptoms,
                                    class_names=['无' + unique_tcms[index],unique_tcms[index]],
                                    rounded=True,
                                    filled=True)
    dot_data = dot_data.replace('helvetica', 'MicrosoftYaHei')
    graph = pydotplus.graph_from_dot_data(dot_data)
    filename = str(time.time()) + '.png'
    img = consts.STATIC_DIR + filename
    graph.write_png(img)
    return filename

def onehot_data(df, unique_list):
    data_array = np.array(df)
    [row_num, col_num] = data_array.shape
    data_onehot = np.zeros([row_num, len(unique_list)])
    col_num_effective_max = 0
    while row_num > 0:
        col_index = 0
        while col_index < col_num:
            if data_array[row_num - 1][col_index] not in unique_list:
                col_index = col_index + 1
                break
            index_set = unique_list.index(data_array[row_num - 1][col_index])
            data_onehot[row_num - 1][index_set] = 1
            col_index = col_index + 1
        if col_index > col_num_effective_max:
            col_num_effective_max = col_index
        row_num = row_num - 1

    return pd.DataFrame(data_onehot, dtype=np.bool)