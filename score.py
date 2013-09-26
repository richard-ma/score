#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import traceback
import logging
import re
import pprint

# 基础配置
logging.basicConfig(level = logging.DEBUG)

def removeCR(line):
    if line[-1] == '\n': return line[0:-1]

def getFileList(path):
    path = str(path)
    if path == "":
      return []
    a = os.listdir(path)
    b = [x for x in a if os.path.isfile(path + x)]
    return b

def cutfloat(x):
    return float(int(x * 10)) / 10

if __name__ == '__main__':
  try:
    name = ['语文', '数学', '英语',\
            '物理', '化学', '生物',\
            '历史', '地理', '政治',\
            '理综', '文综', '合计']
    lineScore = [
            [150, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30], # 语文
            [150, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30], # 数学
            [150, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30], # 英语
            [120, 110, 100, 90, 80, 70, 60, 50, 40, 30],           # 物理
            [100, 90, 80, 70, 60, 50, 40, 30],                     # 化学
            [80, 70, 60, 50, 40, 30],                              # 生物
            [100, 90, 80, 70, 60, 50, 40, 30],                     # 历史
            [100, 90, 80, 70, 60, 50, 40, 30],                     # 地理
            [100, 90, 80, 70, 60, 50, 40, 30],                     # 政治
            [300, 270, 240, 210, 180, 150, 120, 90],               # 理综
            [300, 270, 240, 210, 180, 150, 120, 90],               # 文综
            ]
    passRate = 0.60 # 及格分数为总分的60%

    allScoreSum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 各科成绩之和
    allStudentCnt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 各科参考人数

    dataDir = os.getcwd() + '/data/'
    ansDir = os.getcwd() + '/ans/'
    logging.info('数据目录: %s' % dataDir)
    logging.info('输出目录: %s' % ansDir)

    # 判断数据目录是否存在
    if not os.path.exists(dataDir):
      logging.error('没有data目录，请先创建数据')
      sys.exit(1)

    '''
    # 判断输出目录是否存在
    if os.path.exists(ansDir):
      logging.error('ans目录已存在，请删除或移动此目录后重新执行。')
      sys.exit(1)
    else:
      os.makedirs(ansDir) # 创建输出目录
      logging.info('已创建ans目录')
    '''

    studentCnt = 0 # 参考学生计数初始化
    oldStudentCnt = 0 # 上一个文件完成时学生计数
    for scoreFile in getFileList(dataDir): # 找出所有数据文件
      with open(dataDir + scoreFile, 'r') as dataFile: # 打开数据文件
        logging.info('数据文件: %s' % scoreFile)

        lineNum = 0
        for line in dataFile: # 处理一个学生成绩
          line = removeCR(line) # 去除行尾回车
          if re.match(r'([+-]?\d+([.]?[\d]+)?[,]?)+$', line): # 过滤出数字
            # 分割数字并转换成浮点数
            scores = line.split(',')
            scores = [float(x) for x in scores]

            # 统计每个元科目的参考人数和总成绩
            for idx, score in enumerate(scores):
              if score >= 0:
                allStudentCnt[idx] += 1
                allScoreSum[idx] += score

            # 文综和理综成绩是否齐全，list中求和为0证明成绩齐全
            llist = map((lambda x: 0 if x > 0 else x), scores[3:6])
            pprint.pprint(llist)
            wlist = map((lambda x: 0 if x > 0 else x), scores[6:9])
            pprint.pprint(wlist)
            alllist = map((lambda x: 0 if x > 0 else x), scores[0:9])
            pprint.pprint(alllist)

            # 将成绩中的缺考信息替换为成绩0
            scores = map((lambda x: 0 if x<0 else x), scores)

            # 理综成绩统计
            if sum(llist) >= 0:
              scores.append(sum(scores[3:6]))  # 添加理综成绩
              allStudentCnt[9] += 1
              allScoreSum[9] += scores[9]
            else:
              scores.append(0)
            # 文综成绩统计
            if sum(wlist) >= 0:
              scores.append(sum(scores[6:9]))  # 添加文综成绩
              allStudentCnt[10] += 1
              allScoreSum[10] += scores[10]
            else:
              scores.append(0)
            # 总成绩统计
            if sum(alllist) >= 0:
              scores.append(sum(scores[0:9])) # 添加总成绩
              allStudentCnt[11] += 1
              allScoreSum[11] += scores[11]
            else:
              scores.append(0)

            pprint.pprint(scores)
            pprint.pprint(allStudentCnt)
            pprint.pprint(allScoreSum)

            lineNum += 1
          else: # 行数据验证有错误
            if lineNum == 0: continue # 忽略第一行标题
            logging.error('第%d行数据有误，请检查' % (lineNum+1))
            sys.exit(-1)
        # 学生循环完毕
        logging.info('此文件导入学生数据%d条。' % int(studentCnt - oldStudentCnt))
        oldStudentCnt = studentCnt # 更新上一个文件数据数量为当前数据数量
    logging.info('导入学生数据总数%d条。' % studentCnt)

  except SystemExit:
    pass
  except:
    traceback.print_exc()
