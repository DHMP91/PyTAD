from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from . import views
from .api.testcase import TestCaseAPI, TestCasesAPI, NewTestCaseAPI
from .api.testrun import *

urlpatterns = [
    path("", views.index, name="index"),

    # Test Case API
    path("api/list",TestCasesAPI.as_view()), # all test cases
    path("api/testcase", NewTestCaseAPI.as_view()), # Post new test case
    path("api/testcase/<int:pk>", TestCaseAPI.as_view()), # GET, PUT, DELETE test case
    # path("api/testcase/<int:pk>/testruns", None), # all test runs for test case
    # path("api/testcase/<int:pk>/testrun/<int:pk>", None), # GET, POST, PUT, DELETE test run

    #Test Runs API
    path("api/testcase/<int:test_id>/list", TestRunsAPI.as_view()),  # all test cases
    path("api/testcase/<int:test_id>/testrun", NewTestRunAPI.as_view()),  # Post new test case
    path("api/testcase/testrun/<int:test_id>", TestRunAPI.as_view()),  # GET, PUT, DELETE test case
]