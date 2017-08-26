from rest_framework import serializers

from alert_app.models import AlertConfig


class AlertConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertConfig
        fields = '__all__'
