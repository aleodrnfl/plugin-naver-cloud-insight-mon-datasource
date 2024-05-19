import logging
import time
import json
import requests
import base64
import hmac
import hashlib

from spaceone.core import utils
from spaceone.core.connector import BaseConnector
from src.spaceone.monitoring.connector.naver_cloud_connector.naver_cloud_metric import NaverCloudMetric

__all__ = ['NaverCloudConnector']
_LOGGER = logging.getLogger(__name__)

class NaverCloudConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = None
        self.base_url = 'https://cw.apigw.ntruss.com'

    def make_signature(self, access_key, secret_key, method, uri, timestamp):
        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        secret_key = bytes(secret_key, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey.decode()

    def set_connect(self, schema, options: dict, secret_data: dict, endpoint, payload):
        self.url = f"{self.base_url}{endpoint}"
        self.endpoint = endpoint
        method = 'POST'
        timestamp = str(int(time.time() * 1000))
        metric_access_key = secret_data['ncloud_access_key_id']
        metric_secret_key = secret_data['ncloud_secret_key']

        headers = {
            'x-ncp-apigw-signature-v2': self.make_signature(metric_access_key, metric_secret_key, method,
                                                       endpoint,
                                                       timestamp),
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': metric_access_key,
            'Content-Type': 'application/json'
        }
        if options is None:
            options = {}

        self.client = requests.post(self.url, headers=headers, json=payload).json()
        print(self.client)
    def list_metrics(self, *args):
        return NaverCloudMetric(self.client, self.url).list_metrics(*args)
    def get_metric_data(self, *args):
        return NaverCloudMetric(self.client, self.url).get_metric_data(*args)
    def get_labels(self, *args):
        return NaverCloudMetric(self.client, self.url).get_labels(*args)


