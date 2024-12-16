from rest_framework import serializers
from testcases.models import TestRun, TestCase


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = [
            'id',
            'name',
            'relative_path',
            'create_date',
        ]

class TestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRun
        fields = [
            'id',
            'suite_id',
            'test_id',
            'status',
            'start_time',
            'end_time',
            'marks',
            'product_version',
            'environment',
            'defects'
        ]