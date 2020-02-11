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

    def test_chkBracket1(self):
        self.assertEqual(graphs.checkBrackets("123456"), 0, "Should be 0")

    def test_chkBracket2(self):
        self.assertEqual(graphs.checkBrackets("12+(3*4)+56"), 1, "Should be 1")

    def test_chkBracket3(self):
        self.assertEqual(graphs.checkBrackets("12+(3*4+56"), -1, "Should be -1")

    def test_analizeOprs_ok(self):
        self.assertEqual(graphs.analizeOperations("1+2+3+4"), True, "Should be true")

    def test_analizeOprs_nok(self):
        self.assertEqual(graphs.analizeOperations("++1+2+3+4"), False, "Should be false")

    def test_analizeOprs_nok2(self):
        self.assertEqual(graphs.analizeOperations("1+2++3+4"), False, "Should be false")

if __name__ == '__main__':
    unittest.main()