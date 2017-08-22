from rest_framework import serializers

from JobPostService.alert_app.models import AlertConfig


class AlertConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertConfig
        fields = '__all__'
