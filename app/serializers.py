from rest_framework import serializers
from .models import Feature, Requirement

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "task", "description", "estimated_loc", "actual_loc", "estimated_hours", "actual_hours", "created_at"]


class RequirementSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(read_only=True, many=True)
    class Meta:
        model = Requirement
        fields = ["id", "requirement", "features", "estimated_total_loc", "actual_total_loc", "estimated_total_hours", "actual_total_hours", "created_at"]