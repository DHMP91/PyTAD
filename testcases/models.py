import datetime

from django.db import models
from django.utils import timezone


class TestCase(models.Model):
    name = models.CharField(max_length=30, blank=False)
    relative_path = models.CharField(max_length=300, blank=False)
    create_date = models.DateTimeField(blank=False, default=datetime.datetime.now())


class TestRun(models.Model):
    class Result(models.TextChoices):
        PASS = "PASS"
        FAIL = "FAIL"
        ERROR = "ERROR"
        UNKNOWN = "UNKNOWN"
        XFAIL = "XFAIL"
        XPASS = "XPASS"
        SKIPPED = "SKIPPED"
        INPROGRESS = "INPROGRESS"

    class TestLevel(models.TextChoices):
        UNIT = "UNIT"
        API = "API"
        UI = "UI"

    suite_id = models.CharField(max_length=30) # Test suite id
    test_id = models.ForeignKey(TestCase, models.CASCADE, related_name="test_runs", null=True) # Test Case ID. If null, untracked test
    status = models.CharField(
        max_length=30,
        choices=Result.choices,
        default=Result.UNKNOWN
    ) # Outcome/status of test
    start_time = models.DateTimeField(blank=False, default=datetime.datetime.now()) # Test start time. Default to now
    end_time = models.DateTimeField(null=True) # Test end time
    marks = models.CharField(max_length=30, blank=True) # Pytest marks or tags
    product_version = models.CharField(max_length=30, blank=True) # Product version tested against
    environment = models.CharField(max_length=200, blank=True) # Environment detail of test run
    defects = models.CharField(max_length=100, blank=True) # Related/Known defects related to test


