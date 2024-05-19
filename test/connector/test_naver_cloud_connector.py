import unittest
import os
import logging
from datetime import datetime, timedelta
from unittest.mock import patch
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core.unittest.result import print_data
import json


from src.spaceone.monitoring.connector.naver_cloud_connector import NaverCloudConnector
from src.spaceone.monitoring.manager.naver_cloud_manager import NaverCloudManager

_LOGGER = logging.getLogger(__name__)
AKI = os.environ.get('NCLOUD_ACCESS_KEY_ID', None)
SK = os.environ.get('NCLOUD_SECRET_KEY', None)

class TestNaverCloudConnector(unittest.TestCase):
    secret_data = {
        'ncloud_access_key_id': AKI,
        'ncloud_secret_key': SK,
    }
    @classmethod
    def setUpClass(cls):
        config.init_conf(package='src.spaceone.monitoring')
        cls.schema = 'naver_client_secret'
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_list_metrics(self):
        options = {}
        payload = {
            "prodKey": "460438474722512896"
        }
        secret_data = self.secret_data
        endpoint = '/cw_fea/real/cw/api/rule/group/metric/search'
        self.naver_cloud_connector = NaverCloudConnector(secret_data=secret_data)

        self.naver_cloud_connector.set_connect({}, options=options, secret_data=secret_data, endpoint=endpoint, payload=payload)
        metrics_info = self.naver_cloud_connector.list_metrics(payload)
        print("ss",metrics_info)
        print_data(metrics_info, 'test_list_metrics')

    def test_get_labels(self):
        options = {}
        payload = {
            "prodKey": "460438474722512896"
        }
        secret_data = self.secret_data
        endpoint = '/cw_fea/real/cw/api/rule/group/metric/search'
        self.naver_cloud_connector = NaverCloudConnector(secret_data=secret_data)
        self.naver_cloud_connector.set_connect({}, options=options, secret_data=secret_data, endpoint=endpoint, payload=payload)
        label_info = self.naver_cloud_connector.get_labels(payload)
        print_data(label_info, 'test_get_labels')
    def test_get_metric_data(self):
        options = {}
        end = datetime.utcnow()
        start = end - timedelta(minutes=60)

        end_millisec = int(end.timestamp() * 1000)
        start_millisec = int(start.timestamp() * 1000)

        payload = {
          "timeEnd": end_millisec,   #1715813940000
          "timeStart": start_millisec,     #1715813820000
          "cw_key": "460438474722512896",
          "productName":"System/Auto Scaling(VPC)",
          "metric": "used_rto",
          # "interval": "Min1",
          # "aggregation": "AVG",
          "dimensions": {
              "type": "disk",
              "disk_idx": "loop0"
          }
        }

        secret_data = self.secret_data
        endpoint = '/cw_fea/real/cw/api/data/query'
        self.naver_cloud_connector = NaverCloudConnector(secret_data=secret_data)
        self.naver_cloud_connector.set_connect({}, options=options, secret_data=secret_data, endpoint=endpoint, payload=payload)

        metrics_info = self.naver_cloud_connector.get_metric_data(
            payload.get('timeEnd'),
            payload.get('timeStart'),
            payload.get('cw_key'),
            payload.get('productName', []),
            payload.get('metric'),
            payload.get('interval', []),
            payload.get('aggregation', []),
            payload.get('dimensions')
        )

        print("test", metrics_info)
        print_data(metrics_info, 'test_list_metrics')



if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)

