#!/usr/evn/bin python
# -*- coding: utf-8 -*-

import os



# 判断输出目录是否存在
if os.path.exists(os.getcwd()+'/ans'):
# 已经存在输出目录，提示删除
    print '输出目录已存在，请删除此目录后重新执行。'
else:
# 创建输出目录
    os.makedirs(os.getcwd()+'/ans')
