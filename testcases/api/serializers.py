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


class SearchTestCaseSerializer(serializers.Serializer):
    relative_path = serializers.CharField(max_length=300)


class NewTestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRun
        fields = [
            'name',
            'suite_id',
            'status',
            'start_time',
            'end_time',
            'marks',
            'product_version',
            'environment',
            'defects'
        ]


class TestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRun
        fields = [
            'id',
            'name',
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