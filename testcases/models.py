import datetime

from django.db import models
from django.utils import timezone


class TestCase(models.Model):
    name = models.CharField(max_length=100, blank=False)
    relative_path = models.CharField(max_length=300, blank=False, unique=True)
    create_date = models.DateTimeField(blank=False, auto_now_add=True)
    internal_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    code = None
    code_hash = None

class TestBody(models.Model):
    code = models.TextField(max_length=1000, blank=False)
    code_hash = models.CharField(max_length=300, blank=False, unique=True)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)

class TestRun(models.Model):
    class Result(models.TextChoices):
        PASS = "PASSED"
        FAIL = "FAILED"
        ERROR = "ERROR"
        UNKNOWN = "UNKNOWN"
        XFAIL = "XFAILED"
        XPASS = "XPASSED"
        SKIPPED = "SKIPPED"
        INPROGRESS = "INPROGRESS"

    class TestLevel(models.TextChoices):
        UNIT = "UNIT"
        API = "API"
        UI = "UI"

    name = models.CharField(max_length=100)  # Test suite id
    suite_id = models.CharField(max_length=30, blank=True) # Test suite id
    test_id = models.ForeignKey(TestCase, models.CASCADE, related_name="test_runs")
    status = models.CharField(
        max_length=30,
        choices=Result.choices,
        default=Result.UNKNOWN
    ) # Outcome/status of test
    start_time = models.DateTimeField(blank=False, auto_now_add=True) # Test start time. Default to now
    end_time = models.DateTimeField(null=True) # Test end time
    marks = models.CharField(max_length=30, blank=True) # Pytest marks or tags
    product_version = models.CharField(max_length=30, blank=True) # Product version tested against
    environment = models.CharField(max_length=200, blank=True) # Environment detail of test run
    defects = models.CharField(max_length=100, blank=True) # Related/Known defects related to test
    test_body_id = models.ForeignKey(TestBody, on_delete=models.CASCADE)
    code_hash = None

