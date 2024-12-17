from drf_spectacular.utils import extend_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from testcases.models import TestCase
from testcases.api.serializers import TestCaseSerializer, SearchTestCaseSerializer


class TestCasesAPI(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]


class NewTestCaseAPI(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]

class SearchTestCase(APIView):

    @extend_schema(
        request=SearchTestCaseSerializer,
        responses=TestCaseSerializer
    )
    def post(self, request):
        request_serializer = SearchTestCaseSerializer(data=request.data)
        if request_serializer.is_valid():
            path = request_serializer.data['relative_path']
            try:
                test_case = TestCase.objects.get(relative_path=path)
                serializer = TestCaseSerializer(test_case)
                return Response(serializer.data)
            except TestCase.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestCaseAPI(APIView):
    authentication_classes = [TokenAuthentication]
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

    def delete(self, request, pk):
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