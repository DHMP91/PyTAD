from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from . import views
from .api.testbody import TestBodyAPI
from .api.testcase import TestCaseAPI, TestCasesAPI, NewTestCaseAPI, SearchTestCase
from .api.testrun import *

urlpatterns = [
    path("", views.index, name="index"),

    # Test Case API
    path("api/list",TestCasesAPI.as_view()), # all test cases
    path("api/testcase", NewTestCaseAPI.as_view()), # Post new test case
    path("api/testcase/search", SearchTestCase.as_view()),
    path("api/testcase/<int:pk>", TestCaseAPI.as_view()), # GET, PUT, DELETE test case
    path("api/testcase/<int:pk>/testbody", TestBodyAPI.as_view()),  # list testcase codes/bodies

    #Test Runs API
    path("api/testcase/<int:pk>/testruns", TestRunsAPI.as_view()),  # all test cases
    path("api/testcase/<int:pk>/testrun", NewTestRunAPI.as_view()),  # Post new test case
    path("api/testrun/<int:pk>", TestRunAPI.as_view()),  # GET, PUT, DELETE test cas
]