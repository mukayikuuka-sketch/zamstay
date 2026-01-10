from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

# Add a test endpoint
def test_api(request):
    return JsonResponse({"message": "API is working!"})

# Your existing views (simplified)
class ItemListView(APIView):
    def get(self, request):
        return Response({"items": []})

class ItemDetailView(APIView):
    def get(self, request, pk):
        return Response({"item": {"id": pk}})


