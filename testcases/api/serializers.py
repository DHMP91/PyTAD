from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
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
            "internal_id"
        ]


class NewTestCaseSerializer(serializers.ModelSerializer):
    code_hash = serializers.CharField()
    code =  serializers.CharField()
    class Meta:
        model = TestCase
        fields = [
            'id',
            'name',
            'relative_path',
            'create_date',
            "code_hash",
            "code",
            "internal_id"
        ]

class SearchTestCaseSerializer(serializers.ModelSerializer):
    code_hash = serializers.SerializerMethodField()
    class Meta:
        model = TestCase
        fields = [
            'name',
            'relative_path',
            "code_hash",
            "internal_id"
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_code_hash(self):
        pass

class NewTestRunSerializer(serializers.ModelSerializer):
    code_hash = serializers.CharField()
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
            'defects',
            'code_hash'
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
            'defects',
            'test_body_id'
        ]