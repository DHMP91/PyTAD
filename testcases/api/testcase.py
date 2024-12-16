from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status, permissions
from testcases.models import TestCase
from testcases.serializers import TestCaseSerializer


class TestCasesAPI(APIView):
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        List all test_cases
        """
        cases = TestCase.objects.all()
        serializer = TestCaseSerializer(cases, many=True)
        return Response(serializer.data)

class NewTestCaseAPI(APIView):
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = TestCaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestCaseAPI(APIView):
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        test_case = self.__get_test_case(pk)
        if not test_case:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TestCaseSerializer(test_case)
        return Response(serializer.data)


    def put(self, request, pk):
        test_case = self.__get_test_case(pk)
        if not test_case:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = JSONParser().parse(request)
        serializer = TestCaseSerializer(test_case, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        test_case = self.__get_test_case(pk)
        if not test_case:
            return Response(status=status.HTTP_404_NOT_FOUND)

        test_case.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def __get_test_case(pk):
        try:
            return TestCase.objects.get(pk=pk)
        except TestCase.DoesNotExist:
            return None