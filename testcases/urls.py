from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from . import views
from .api.testcase import TestCaseAPI, TestCasesAPI, NewTestCaseAPI, SearchTestCase
from .api.testrun import *

urlpatterns = [
    path("", views.index, name="index"),

    # Test Case API
    path("api/list",TestCasesAPI.as_view()), # all test cases
    path("api/testcase", NewTestCaseAPI.as_view()), # Post new test case
    path("api/testcase/search", SearchTestCase.as_view()),
    path("api/testcase/<int:pk>", TestCaseAPI.as_view()), # GET, PUT, DELETE test case

    #Test Runs API
    path("api/testcase/<int:pk>/testruns", TestRunsAPI.as_view()),  # all test cases
    path("api/testcase/<int:pk>/testrun", NewTestRunAPI.as_view()),  # Post new test case
    path("api/testrun/<int:pk>", TestRunAPI.as_view()),  # GET, PUT, DELETE test case
]