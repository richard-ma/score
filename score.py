#!/usr/evn/bin python
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

if __name__ == '__main__':
  try:
    dataDir = os.getcwd() + '/data/'
    ansDir = os.getcwd() + '/ans/'

    # 判断数据目录是否存在
    if not os.path.exists(dataDir):
      logging.error('没有data目录，请先创建数据')
      sys.exit(1)

    '''
    # 判断输出目录是否存在
    if os.path.exists(ansDir):
      logging.info('ans目录已存在，请删除或移动此目录后重新执行。')
      sys.exit(1)
    else:
      os.makedirs(ansDir) # 创建输出目录
      logging.info('已创建ans目录')
    '''

    for scoreFile in getFileList(dataDir): # 找出所有数据文件
      logging.debug("**Opening " + dataDir + scoreFile)
      with open(dataDir + scoreFile, 'r') as dataFile: # 打开数据文件
        for line in dataFile: # 处理一个学生成绩
          for score in line.split(','):
            if re.match(r'[+-]?\d+$', score):
              print score

  except SystemExit:
    pass
  except:
    traceback.print_exc()
