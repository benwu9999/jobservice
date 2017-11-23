from rest_framework import serializers

from job_post_app.serializers import CompensationSerializer
from models import Alert, Query


class QuerySerializer(serializers.ModelSerializer):
    min_comp = CompensationSerializer()
    max_comp = CompensationSerializer()

    class Meta:
        model = Query
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(QuerySerializer, self).to_representation(instance)
        ret['terms'] = ret['terms'].split(',')
        ret['employer_names'] = ret['employer_names'].split(',')
        ret['locations'] = ret['locations'].split(',')
        return ret

class AlertSerializer(serializers.ModelSerializer):
    query = QuerySerializer()

    class Meta:
        model = Alert
        fields = '__all__'
