#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:46
# @Author  : Vodka0629
# @Email   : 563511@qq.com, ZhangXiangming@gmail.com
# @FileName: test.py
# @Software: Mahjong II
# @Blog    :

import unittest

case_path = 'case'
report_path = 'report'

cases = unittest.defaultTestLoader.discover(start_dir=case_path, pattern = "test*.py")
# print(cases)

runner = unittest.TextTestRunner()
runner.run(cases)

