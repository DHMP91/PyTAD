from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from testcases.models import TestRun
from testcases.api.serializers import TestRunSerializer



class TestRunsAPI(APIView):
    serializer_class = TestRunSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, test_id):
        """
        List all test runs for test case
        """
        runs = TestRun.objects.filter(test_id = test_id)
        serializer = TestRunSerializer(runs, many=True)
        return Response(serializer.data)


class NewTestRunAPI(APIView):
    serializer_class = TestRunSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, test_id):
        data = JSONParser().parse(request)
        serializer = TestRunSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestRunAPI(APIView):
    serializer_class = TestRunSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        test_run = self.__get_test_run(pk)
        if not test_run:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TestRunSerializer(test_run, many=True)
        return Response(serializer.data)


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

    def delete(self, pk):
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