from django.shortcuts import render
from rest_framework import viewsets
from .models import Nofluff_data
from .serializers import Nofluff_dataSerializer

class NofluffView(viewsets.ModelViewSet):
    queryset = Nofluff_data.objects.all()
    serializer_class = Nofluff_dataSerializer