from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from testcases.models import TestRun
from testcases.api.serializers import TestRunSerializer, NewTestRunSerializer


class TestRunsAPI(generics.ListAPIView):
    serializer_class = TestRunSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="List Test Runs (Support Pagination)",
        operation_id="listTestRuns"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        qs = TestRun.objects.filter(test_id = kwargs["pk"])
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class NewTestRunAPI(APIView):
    serializer_class = NewTestRunSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Create new Test Run",
        operation_id="createTestRun",
        request=NewTestRunSerializer,
        responses={
            201:TestRunSerializer
        }
    )
    def post(self, request, pk):
        request.data['test_id'] = pk
        serializer = TestRunSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestRunAPI(APIView):
    serializer_class = TestRunSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Get test run by id",
        operation_id="getTestRun"
    )
    def get(self, request, pk):
        test_run = self.__get_test_run(pk)
        if not test_run:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TestRunSerializer(test_run)
        return Response(serializer.data)


    @extend_schema(
        description="Update test run by id",
        operation_id="updateTestRun"
    )
    def put(self, request, pk):
        test_run = self.__get_test_run(pk)
        if not test_run:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = JSONParser().parse(request)
        serializer = TestRunSerializer(test_run, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Delete test run by id",
        operation_id="deleteTestRun"
    )
    def delete(self, request, pk):
        test_run = self.__get_test_run(pk)
        if not test_run:
            return Response(status=status.HTTP_404_NOT_FOUND)

        test_run.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def __get_test_run(pk):
        try:
            return TestRun.objects.get(pk=pk)
        except TestRun.DoesNotExist:
            return None