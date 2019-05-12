from django.shortcuts import render
from rest_framework import viewsets
from .models import DataAggregator
from .serializers import DataAggregatorSerializer

class DataAggregatorView(viewsets.ModelViewSet):
    queryset = DataAggregator.objects.all()
    serializer_class = DataAggregatorSerializer