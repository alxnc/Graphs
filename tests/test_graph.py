#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_graphs
----------------------------------
Tests for `graphs`.
"""
import graphs
import unittest

class TestGraphs(unittest.TestCase):

    def test_chkBracket1_(self):
        self.assertEqual(graphs.checkBrackets("123456"), 0, "Should be 0")

    def test_chkBracket2_(self):
        self.assertEqual(graphs.checkBrackets("12+(3*4)+56"), 1, "Should be 1")

    def test_chkBracket3_(self):
        self.assertEqual(graphs.checkBrackets("12+(3*4+56"), -1, "Should be -1")

if __name__ == '__main__':
    unittest.main()


    