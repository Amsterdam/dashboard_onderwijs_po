from django.db import models
from django.contrib.postgres.fields import JSONField


class DataSummary(models.Model):
    row_key = models.CharField(max_length=255, unique=True)
    columns = JSONField()
