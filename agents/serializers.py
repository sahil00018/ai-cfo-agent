from rest_framework import serializers
from .models import QueryLog
from .models import FinancialMetric
from .models import FinancialUpload



class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = '__all__'

from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

class AskAgentSerializer(serializers.Serializer):

    question = serializers.CharField(
        required=True,
        max_length=500,
        allow_blank=False,
    )




class FinancialMetricSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialMetric
        fields = "__all__"



class FinancialUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialUpload
        fields = "__all__"