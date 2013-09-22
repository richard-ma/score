#!/usr/evn/bin python
# -*- coding: utf-8 -*-

import os

dataDir = os.getcwd() + '/data'
ansDir = os.getcwd() + '/ans'

# 判断数据目录是否存在
if not os.path.exists(dataDir):
    print '没有data目录，请先创建数据'

# 判断输出目录是否存在
if os.path.exists(ansDir):
    print 'ans目录已存在，请删除此目录后重新执行。' # 已经存在输出目录，提示删除
else:
    os.makedirs(ansDir) # 创建输出目录
