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
        self.assertEqual(graphs.check_brackets("123456"), 1, "Should be 1")

    def test_chkBracket2(self):
        self.assertEqual(graphs.check_brackets("12+(3*4)+56"), 1, "Should be 1")

    def test_chkBracket3(self):
        self.assertEqual(graphs.check_brackets("12+(3*4+56"), 0, "Should be 0")

    def test_analizeOprs_ok(self):
        self.assertEqual(graphs.check_dbl_operators("12+2*(3*4+10/5)"), True, "Should be true")

    def test_analizeOprs_nok(self):
        self.assertEqual(graphs.check_dbl_operators("++1+2+3+4"), False, "Should be false")

    def test_analizeOprs_nok2(self):
        self.assertEqual(graphs.check_dbl_operators("1+2++3+4"), False, "Should be false")

    def test_analyze_op_after_CB_ok(self):
        self.assertEqual(graphs.check_op_after_cb("12+2*(1+(3*4+10/5))"), True, "Should be true")
    
    def test_analyze_op_after_CB_ok2(self):
        self.assertEqual(graphs.check_op_after_cb("12+2*(1+(3*4+10/5))+1"), True, "Should be true")
    
    def test_analyze_op_after_CB_nok(self):
        self.assertEqual(graphs.check_op_after_cb("12+2*1+(3*4+10/5)1"), False, "Should be false")        

    def test_evalexpr_ok(self):
        self.assertEqual(graphs.eval_expr("12+2*(3*4+10/5)"), 40, "Should be 40")
        
    def test_evalexpr_ok1(self):
        self.assertEqual(graphs.eval_expr("3^3^2"), 19683, "Should be 19683")

if __name__ == '__main__':
    unittest.main()