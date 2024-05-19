import logging
import time
from pprint import pprint
from spaceone.core import utils
from datetime import datetime, timezone

__all__ = ['NaverCloudMetric']
_LOGGER = logging.getLogger(__name__)
PERCENT_METRIC = ['10^2.%']

class NaverCloudMetric(object):
    def __init__(self, client, url):
        self.client = client
        self.url = url

    def list_metrics(self, payload):
        metrics_info = []
        for metric in self.client['metrics']:
            metric_info = {
                'key': metric.get('idDimension'),
                'name': metric.get('metric'),
                'unit': self._get_metric_unit(metric.get('unit')),
                'metric_query': {
                    'dimValues': payload.get('dimValues', []),
                    'query': payload.get('query', []),
                    'dimensionsSelectedList': payload.get('dimensionsSelectedList', []),
                    'prodKey': payload['prodKey']
                }
            }
            metrics_info.append(metric_info)
        return {'metrics': metrics_info}

    def get_labels(self, payload):
        all_labels = []
        for metric in self.client['metrics']:
            labels = {}
            for dim_val in metric.get('dimensions', []):
                dim = dim_val.get('dim')
                val = dim_val.get('val')
                labels[dim] = val
            all_labels.append(labels)
        return all_labels


    def get_metric_data(self, timeEnd, timeStart, cw_key, productName, metric, interval, aggregation, dimensions):
        metrics_data_info = []
        for metric in self.client:
            label = metric[0]
            value = metric[1]
            metric_data_info = {
                'labels': label,    #timestamp
                'values': value
            }
            metrics_data_info.append(metric_data_info)

        return metrics_data_info

    @staticmethod
    def _get_metric_unit(unit):
        unit_name = unit
        if unit == 's':
            unit_name = 'Seconds'
        elif unit == 'By':
            unit_name = 'Bytes'
        elif unit == '10^2.%' or unit == '%':
            unit_name = 'Percentage'
        elif unit == '1' or unit == 1:
            unit_name = 'Count'
        elif unit == 's{idle}':
            unit_name = 'Idle/s'
        elif unit == 's{uptime}':
            unit_name = 'Uptime/s'
        elif unit == 's{CPU}':
            unit_name = 'CPU/s'

        return {
            'x': 'Timestamp',
            'y': unit_name
        }




