import os
import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
import logging

from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from src.spaceone.monitoring.error import *
from src.spaceone.monitoring.connector.naver_cloud_connector import NaverCloudConnector
from src.spaceone.monitoring.manager.naver_cloud_manager import NaverCloudManager

_LOGGER = logging.getLogger(__name__)
AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)
class TestMetricManager(unittest.TestCase):
    # secret_data = {
    #     'ncloud_access_key_id': AKI,
    #     'ncloud_secret_key': SK
    # }

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='src.spaceone.monitoring')
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    @patch.object(NaverCloudConnector, '__init__', return_value=None)
    def test_convert_stat(self, *args):
        naver_cloud_manager = NaverCloudManager()
        stat = naver_cloud_manager._convert_stat('MEAN')
        print_data(stat, 'test_convert_stat')

    @patch.object(NaverCloudConnector, '__init__', return_value=None)
    def test_make_period_from_time_range(self, *args):
        naver_cloud_manager = NaverCloudManager()

        end = datetime.utcnow()
        start = end - timedelta(days=1)
        period = naver_cloud_manager._make_period_from_time_range(start, end)
        print_data(period, 'test_make_period_from_time_range')

if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)