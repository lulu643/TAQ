import unittest

from src.prepare_taq_data.FilterSP500 import FilterSP500


class Test_FilterSP500(unittest.TestCase):

    def test(self):
        # Instantiate a s&p500 filter
        filter_obj = FilterSP500()
        # Make sure we are getting only tickers in s&p500 list during the period
        # test 1: list some of s&p500 indices and test if they are in the tickers list
        # test 2: list some of non-s&p500 indices and test if they are not in the tickers list
        tickers = filter_obj.get_SP500_tickers()
        self.assertTrue(all(ele in tickers for ele in ['AMZN', 'MSFT', 'IBM']))
        self.assertTrue(all(ele not in tickers for ele in ['RBA', 'KVT', 'CIA']))



if __name__ == "__main__":
    unittest.main()
