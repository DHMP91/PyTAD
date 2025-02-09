from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from typing import Type, Union

from testcases.models import TestCase, TestBody
from testcases.api.serializers import TestCaseSerializer, SearchTestCaseSerializer, NewTestCaseSerializer


class TestCasesAPI(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="List Test Cases (Support Pagination)",
        operation_id="listTestCases"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class NewTestCaseAPI(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = NewTestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Create Test Cases. Has test change resiliency feature",
        operation_id="createTestCase",
        responses = {
            200: TestCaseSerializer, # Already exists updating
            201: TestCaseSerializer, # Created test case
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = NewTestCaseSerializer(data=request.data)
        if serializer.is_valid():
            test_case = SearchTestCase.search(serializer)
            data = dict(request.data)
            if test_case:
                return self.__update_test(test_case, data)
            else:
                code = request.data['code']
                code_hash = request.data['code_hash']
                del data['code']
                del data['code_hash']
                return self.__create_new_test(data, code, code_hash)
        elif not serializer.is_valid() and "code='unique'" in str(serializer.errors) and "already exists" in str(serializer.errors):
            test_case = SearchTestCase.search(serializer)
            data = dict(request.data)
            return self.__update_test(test_case, data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def __create_new_test(self, data: dict,  code: str, code_hash: str):
        new_serializer = TestCaseSerializer(data=data)
        if new_serializer.is_valid():
            new_serializer.save()
            headers = self.get_success_headers(new_serializer)
            response = Response(new_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            test_case = TestCase.objects.get(pk=new_serializer.data['id'])
            TestBody(test_case=test_case, code=code, code_hash=code_hash).save()
            return response
        else:
            return Response(new_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def __update_test(test_case, data):
        try:
            TestBody.objects.get(code_hash=data['code_hash'])
        except TestBody.DoesNotExist:
            TestBody(test_case=test_case, code=data['code'], code_hash=data['code_hash']).save()
        return TestCaseAPI.update(test_case, data)


class SearchTestCase(APIView):

    @extend_schema(
        description="Search for test cases based on test's fields. Precedence order: internal_id, relative_path, code hash",
        operation_id="searchTestCase",
        request=SearchTestCaseSerializer,
        responses=TestCaseSerializer
    )
    def post(self, request):
        request_serializer = SearchTestCaseSerializer(data=request.data)
        if request_serializer.is_valid():
                test_case = SearchTestCase.search(TestCase, request_serializer)
                if test_case:
                    serializer = TestCaseSerializer(test_case)
                    return Response(serializer.data)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def search(search_request: Union[SearchTestCaseSerializer, NewTestCaseSerializer]) -> TestCase:
        """
         Search matching test case order: internal_id, relative_path, hash

            internal_id: External id associated to the test, ID is unique unless due to user error
            relative_path: High chance of matching since module can't have same test/func name
            hash: High chance of exact matching since test body should be different
            name: Low chance of exact matching since test may have same name in different module

        :param model:
        :param search_request:
        :return:
        """
        search_fields = [
            ("internal_id", search_request.data['internal_id']),
            ("relative_path", search_request.data['relative_path']),
            ("code_hash", search_request.data['code_hash']),
        ]

        test_case = None
        for field, value in search_fields:
            if value:
                try:
                    if field == "code_hash":
                        test_body: TestBody = TestBody.objects.get(**{field: value})
                        test_case: TestCase = TestCase.objects.get(pk=test_body.test_case_id)
                    else:
                        test_case: TestCase = TestCase.objects.get(**{field: value})
                    break
                except (TestCase.DoesNotExist, TestBody.DoesNotExist):
                    continue
        return test_case


class TestCaseAPI(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Get test case by id",
        operation_id="getTestCase"
    )
    def get(self, request, pk):
        test_case = self.__get_test_case(pk)
        if not test_case:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TestCaseSerializer(test_case)
        return Response(serializer.data)

    @extend_schema(
        description="Update test case",
        operation_id="updateTestCase"
    )
    def put(self, request, pk):
        test_case = self.__get_test_case(pk)
        if not test_case:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return TestCaseAPI.update(test_case, request.data)

    @extend_schema(
        description="Delete test case",
        operation_id="deleteTestCase"
    )
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

    @staticmethod
    def update(test_case: TestCase, update_data: dict):
        serializer = TestCaseSerializer(test_case, data=update_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)