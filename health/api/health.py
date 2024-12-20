from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView

from health.api.serializers import HealthSerializer


class HealthAPI(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HealthSerializer

    @extend_schema(
        description="Endpoint to test out service state",
        operation_id="getHealth"
    )
    def get(self, request):
        return JsonResponse({"response": True})
