from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from testcases.api.serializers import TestBodySerializer
from testcases.models import TestBody


class TestBodyAPI(generics.ListAPIView):
    serializer_class = TestBodySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        qs = TestBody.objects.filter(test_case_id = kwargs["pk"]).order_by("-id")
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
