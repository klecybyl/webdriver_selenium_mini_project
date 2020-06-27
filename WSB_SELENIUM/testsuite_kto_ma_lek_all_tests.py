import unittest

from kto_ma_lek_start_page_tests import KtoMaLekStartPageTests
from kto_ma_lek_find_drug_tests import KtoMaLekFindDrugTests


def full_suite():
    test_suite = unittest.TestSuite()

    # adding test classes:
    test_suite.addTest(unittest.makeSuite(KtoMaLekStartPageTests))
    test_suite.addTest(unittest.makeSuite(KtoMaLekFindDrugTests))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(full_suite())
