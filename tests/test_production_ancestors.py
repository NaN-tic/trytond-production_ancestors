# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import doctest_setup, doctest_teardown
from trytond.tests.test_tryton import doctest_checker


class ProductionAncestorsTestCase(ModuleTestCase):
    'Test Production Ancestors module'
    module = 'production_ancestors'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProductionAncestorsTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_production_ancestors.rst',
        setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
        checker=doctest_checker,
        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
