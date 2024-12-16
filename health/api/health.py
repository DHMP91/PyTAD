from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView

from health.api.serializers import HealthSerializer


class HealthAPI(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HealthSerializer
    def get(self, request):
        return JsonResponse({"response": True})
