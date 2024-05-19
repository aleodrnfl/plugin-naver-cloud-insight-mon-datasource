import logging
import time
import datetime
from duration import to_iso8601

from spaceone.core.manager import BaseManager
from src.spaceone.monitoring.error import *
from src.spaceone.monitoring.connector.naver_cloud_connector import NaverCloudConnector

_LOGGER = logging.getLogger(__name__)

_STAT_MAP = {
    'MEAN': 'Average',
    'MAX': 'Maximum',
    'MIN': 'Minimum',
    'SUM': 'Total'
}

class NaverCloudManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.naver_cloud_connector: NaverCloudConnector = self.locator.get_connector('NaverCloudConnector')

    def verify(self, schema, options, secret_data, endpoint, payload):
        """ Check connection
        """
        self.naver_cloud_connector.set_connect(schema, options, secret_data, endpoint, payload)
    def set_connector(self, schema, secret_data, endpoint, payload):
        self.naver_cloud_connector.set_connect(schema, {}, secret_data, endpoint, payload)

    def list_metrics(self, schema, options, secret_data, endpoint, payload):
        self.naver_cloud_connector.set_connect(schema, options, secret_data, endpoint, payload)

        metrics_info = self.naver_cloud_connector.list_metrics(payload)
        return metrics_info

    def get_metric_data(self, schema, options, secret_data, cw_key, metric, dimensions, timeStart, timeEnd, endpoint, payload):
        self.naver_cloud_connector.set_connect(schema, options, secret_data, endpoint, payload)
        return self.naver_cloud_connector.get_metric_data(cw_key=cw_key, metric=metric, dimensions=dimensions, timeStart= timeStart, timeEnd = timeEnd)

    @staticmethod
    def _convert_stat(stat):
        if stat is None:
            stat = 'MEAN'

        if stat not in _STAT_MAP.keys():
            print("convert stat error")
            # raise ERROR_NOT_SUPPORT_STAT(supported_stat=' | '.join(_STAT_MAP.keys()))

        return _STAT_MAP[stat]
    @staticmethod
    def _make_period_from_time_range(start, end):
        start_time = int(time.mktime(start.timetuple()))    #start = datetime(2024, 5, 15, 23, 37)
                                                            #start_time은 타임스탬프 형태 1715813820
        end_time = int(time.mktime(end.timetuple()))
        time_delta = end_time - start_time
        interval = 0
        # Max 60 point in start and end time range
        if time_delta <= 60*60:         # ~ 1h
            interval = 60
        elif time_delta <= 60*60*6:     # 1h ~ 6h
            interval = 60*10
        elif time_delta <= 60*60*12:    # 6h ~ 12h
            interval = 60*20
        elif time_delta <= 60*60*24:    # 12h ~ 24h
            interval = 60*30
        elif time_delta <= 60*60*24*3:  # 1d ~ 2d
            interval = 60*60
        elif time_delta <= 60*60*24*7:  # 3d ~ 7d
            interval = 60*60*3
        elif time_delta <= 60*60*24*14:  # 1w ~ 2w
            interval = 60*60*6
        elif time_delta <= 60*60*24*14:  # 2w ~ 4w
            interval = 60*60*12
        else:                            # 4w ~
            interval = 60*60*24

        return str(interval)+'s'