from django.db import models


class Feature(models.Model):
    task = models.TextField()
    description = models.TextField()
    estimated_loc = models.IntegerField()
    actual_loc = models.IntegerField()
    estimated_hours = models.IntegerField()
    actual_hours = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task


class Requirement(models.Model):
    requirement = models.TextField()
    features = models.ManyToManyField(Feature, related_name="requirements")
    estimated_total_loc = models.IntegerField()
    actual_total_loc = models.IntegerField()
    estimated_total_hours = models.IntegerField()
    actual_total_hours = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Requirement {self.id}"
