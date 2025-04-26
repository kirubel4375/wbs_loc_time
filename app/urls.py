from django.urls import path
from .views import EstimateFromGroqAPIView, RequirementListCreate, RequirementRetrieveUpdateAPIView, FeatureRetrieveUpdateAPIView, FeatureList
urlpatterns = [
    path('estimate', EstimateFromGroqAPIView.as_view(), name='estimate'),
    path('requirements', RequirementListCreate.as_view(), name="requirement_view_create"),
    path('requirement/<int:pk>', RequirementRetrieveUpdateAPIView.as_view(), name="requirement_view_update"),
    path('features', FeatureList.as_view(), name='feature_list'),
    path('feature/<int:pk>', FeatureRetrieveUpdateAPIView.as_view(), name='feature_view_update')
]
