from schematics.models import Model
from schematics.types import BaseType, ListType, DictType, StringType, UnionType, IntType, FloatType
from schematics.types.compound import ModelType

__all__ = ['MetricsModel']


class MetricModel(Model):
    idDimension = StringType(required=True)
    name = StringType(required=True)
    unit = DictType(StringType, required=True)
    group = StringType(serialize_when_none=False)
    metric_query = DictType(BaseType, default={})


class MetricsModel(Model):
    metrics = ListType(ModelType(MetricModel), required=True)

