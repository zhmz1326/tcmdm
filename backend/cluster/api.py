from cluster import cluster_blueprint
from flask import jsonify
from flask import request

from util import utils
from util import consts
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

@cluster_blueprint.route('/datamining', methods=['POST'])
def datamine():
    formdata = json.loads(request.form.get('data'))
    if 'tcm_minimum_frequency' not in formdata:
        return utils.error(400, '请输入中药最小纳入频次')
    if 'symptom_minimum_frequency' not in formdata:
        return utils.error(400, '请输入症状最小纳入频次')

    tcm_minimum_frequency = int(formdata['tcm_minimum_frequency'])
    symptom_minimum_frequency = int(formdata['symptom_minimum_frequency'])

    fileStorage = request.files['file']
    tempFile = consts.TEMP_DIR + fileStorage.filename
    fileStorage.save(tempFile)

    df = pd.read_csv(tempFile, names=["symptom", "tcm"])
    symptom = df['symptom']
    tcm = df['tcm']

    symptom_dict = {}
    tcm_dict = {}
    for data in symptom:
        splits = data.split(',')
        for split in splits:
            if split.startswith('拟'):
                continue
            if split in symptom_dict:
                symptom_dict[split] += 1
            else:
                symptom_dict[split] = 1
    for data in tcm:
        splits = data.split(',')
        for split in splits:
            if split in tcm_dict:
                tcm_dict[split] += 1
            else:
                tcm_dict[split] = 1

    # 数据加载
    symptom_data = []
    tcm_data = []
    for data in symptom:
        splits = data.split(',')
        line = ''
        for split in splits:
            if len(split) == 0:
                continue
            if symptom_dict[split] >= symptom_minimum_frequency: # 最小纳入频次
                line += split.strip() + ' '
        symptom_data.append(line)
    for data in tcm:
        splits = data.split(',')
        line = ''
        for split in splits:
            if len(split) == 0:
                continue
            if tcm_dict[split] >= tcm_minimum_frequency: # 最小纳入频次
                line += split.strip() + ' '
        tcm_data.append(line)

    size = len(tcm_data)
    symptom_tcm_data = []
    for i in range(0, size):
        data = symptom_data[i] + tcm_data[i]
        symptom_tcm_data.append(data)

    tcm_img = cluster_analysis(tcm_data)
    symptom_img = cluster_analysis(symptom_data)
    mix_img = cluster_analysis(symptom_tcm_data)

    clusterResult = {'tcm_img': tcm_img, 'symptom_img': symptom_img, 'mix_img': mix_img}
    return utils.success(clusterResult)

import scipy.cluster.hierarchy as sch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

def cluster_analysis(data):
    # tv = TfidfVectorizer(use_idf=True, smooth_idf=True, norm=None)
    tv = CountVectorizer()
    tv_fit = tv.fit_transform(data)
    fn = tv.get_feature_names()
    ta = tv_fit.toarray()

    # 进行层次聚类: 簇合并方法使用 ward 法
    Z = sch.linkage(ta.T, metric='euclidean', method='ward')

    plt.rc('font', **{'family': 'Microsoft YaHei, SimHei'})  # 设置中文字体的支持
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10, 10))
    # 将层级聚类结果以树状图表示出来并保存
    P = sch.dendrogram(Z, labels=fn, orientation='right', show_leaf_counts=True,
                       leaf_font_size = 8, color_threshold=1000,
                       above_threshold_color='C1',
                       count_sort=True, distance_sort=True)
    filename = str(time.time()) + '.jpg'
    img = consts.STATIC_DIR + filename
    plt.savefig(img)
    plt.clf()
    return filename
