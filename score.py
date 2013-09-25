#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import traceback
import logging
import re

# 基础配置
logging.basicConfig(level = logging.DEBUG)

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
    typename = ['语文', '数学', '英语',\
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

    allScoreSum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 各科成绩之和
    allStudentCnt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 各科参考人数

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
        lineNum = 1
        for line in dataFile: # 处理一个学生成绩
          if re.match(r'([+-]?\d+([.]?[\d]+)?[,]?)+$', line): # 过滤出数字
            logging.debug('正在处理第%d行' % (lineNum+1))
            scoreCode = 0

            allSum = 0
            wSum = 0
            lSum = 0

            scoreFlg = 0 # 该生没有获得成绩，全部缺考
            wScoreFlg = 0 # 没有文综相关成绩，文综缺考
            lScoreFlg = 0 # 没有理综相关成绩，理综缺考
            for score in line.split(','):
              score = float(score) # 类型转换

              logging.debug('%s: %3.1f' % (typename[scoreCode], score))

              if score >= 0:
                allScoreSum[scoreCode] += score # 计算各科总分
                allStudentCnt[scoreCode] += 1 # 各个学科参考人数

                scoreFlg = 1 # 该生有学科获得成绩，可以计入参考学生
                allSum += score # 计算学生总成绩
                if scoreCode >= 3 and scoreCode <= 5: # 计算理综总成绩
                  lSum += score # 计算理综总成绩
                  lScoreFlg = 1 # 该生有理综学科成绩
                if scoreCode >= 6 and scoreCode <= 8:
                  wSum += score # 计算文综总成绩
                  wScoreFlg = 1 # 该生有文综学科成绩

              scoreCode += 1
            # 成绩循环完毕
            allScoreSum[9] = lSum
            allScoreSum[10] = wSum
            allStudentCnt[9] = max(allStudentCnt[3:5])
            allStudentCnt[10] = max(allStudentCnt[6:8])
            if scoreFlg: studentCnt += 1 # 该生有学科获得成绩，计入参考人数

            logging.debug('参考学生计数: %d' % studentCnt)
            logging.debug('学生总成绩: %3.1f' % cutfloat(allSum))
            logging.debug('文综总成绩: %3.1f' % cutfloat(allScoreSum[9]))
            logging.debug('理综总成绩: %3.1f' % cutfloat(allScoreSum[10]))

            lineNum += 1
          else: # 行数据验证有错误
            if lineNum == 1: continue # 忽略第一行标题
            logging.error('第%d行数据有误，请检查' % (lineNum+1))
            sys.exit(-1)
        # 学生循环完毕
        logging.info('此文件导入学生数据%d条。' % int(studentCnt - oldStudentCnt))

        logging.info('导入学生数据总数%d条。' % studentCnt)
        oldStudentCnt = studentCnt # 更新上一个文件数据数量为当前数据数量

  except SystemExit:
    pass
  except:
    traceback.print_exc()
