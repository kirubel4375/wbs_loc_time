from rest_framework import generics
# your_app/views.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from .models import Requirement, Feature
from .serializers import RequirementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FeatureSerializer


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def format_history_for_prompt(history_queryset):
    prompt_lines = []
    for h in history_queryset:
        related_features = h.features.all()
        serialized_features = FeatureSerializer(related_features, many=True).data
        prompt_lines.append(f"""\
Requirement: {h.requirement},
Work Breakdown: {serialized_features},
Estimated LOC: {h.estimated_total_loc}, Actual LOC: {h.actual_total_loc}
Estimated Hours: {h.estimated_total_hours}, Actual Hours: {h.actual_total_hours}
""")
    return "\n\n".join(prompt_lines)

def generate_prompt(requirement_text):
    history = Requirement.objects.order_by("-created_at")[:15]
    history_prompt = format_history_for_prompt(history)

    return f"""
You are a senior software engineer estimating development tasks.

Use the following historical examples to learn from past estimates:

{history_prompt}

Now, for the new requirement, return:

1. A list of development tasks required to implement it.
2. For each task:
   - A short description
   - Estimated **Lines of Code (LOC)** as an exact number (not a range)
   - Estimated **Time in hours** to implement (as a whole number, not a range)

Also include:
- Total LOC
- Total Time in hours

Respond ONLY in this JSON format:

{{
  "tasks": [
    {{
      "task": "Task Name",
      "description": "What this task is about",
      "loc": 100,
      "hours": 8
    }},
    ...
  ],
  "total_loc": 300,
  "total_hours": 24
}}

Requirement:
\"\"\"
{requirement_text}
\"\"\"
"""

class EstimateFromGroqAPIView(APIView):
    def post(self, request, *args, **kwargs):
        req_text = request.data.get("requirement", "")
        prompt = generate_prompt(req_text)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a senior software engineer with experience in software estimation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        result = response.choices[0].message.content.strip()
        if result.startswith("```"):
            result = result.replace("```", "").strip()

        try:
            parsed = json.loads(result)
        except json.JSONDecodeError:
            return Response({"error": "Failed to parse response"}, status=status.HTTP_400_BAD_REQUEST)

        req = Requirement.objects.create(
            requirement=req_text,
            estimated_total_loc=parsed["total_loc"],
            estimated_total_hours=parsed["total_hours"],
            actual_total_loc=0,
            actual_total_hours=0,
        )
        features = []
        for feature in parsed["tasks"]:
            ftr = Feature.objects.create(
                task = feature["task"],
                description = feature["description"],
                estimated_loc = feature["loc"],
                actual_loc = 0,
                estimated_hours = feature["hours"],
                actual_hours = 0,
            )
            features.append(ftr)
        req.features.set(features)

        return Response(parsed, status=status.HTTP_201_CREATED)


class RequirementListCreate(generics.ListCreateAPIView):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer

class RequirementRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer


class FeatureList(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class FeatureRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


