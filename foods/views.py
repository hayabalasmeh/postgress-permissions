from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Food
from .serializers import FoodSerializer
from .permissions import IsOwnerOrReadOnly

class FoodsList(ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    

class FoodsDetail(RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes= (IsOwnerOrReadOnly,)
