import unittest
import tidyextractors as tx
import pandas as pd

class TestBaseExtractor(unittest.TestCase):

    def setUp(self):
        self.basex = tx.BaseExtractor('')

    def test_construction(self):
        self.assertEqual(isinstance(self.basex, tx.BaseExtractor), True)

    def test_raw(self):
        self.assertEqual(isinstance(self.basex.raw(), pd.DataFrame), True)


if __name__ == '__main__':
    unittest.main()