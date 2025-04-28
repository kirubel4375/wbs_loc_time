from rest_framework import serializers
from .models import Feature, Requirement

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class RequirementSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(read_only=True, many=True)
    class Meta:
        model = Requirement
        fields = '__all__'