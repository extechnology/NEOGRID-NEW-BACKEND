from rest_framework import generics
from .dealer_models import Country, State, District, Dealers, WarrentyRegisterModel
from .dealer_serializers import (
    CountrySerializer, StateSerializer, DistrictSerializer, 
    DealersSerializer, WarrentyRegisterSerializer
)

class CountryListCreate(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class StateListCreate(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class StateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class DistrictListCreate(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class DistrictDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class DealersListCreate(generics.ListCreateAPIView):
    queryset = Dealers.objects.all()
    serializer_class = DealersSerializer

class DealersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dealers.objects.all()
    serializer_class = DealersSerializer

class WarrentyRegisterListCreate(generics.ListCreateAPIView):
    queryset = WarrentyRegisterModel.objects.all()
    serializer_class = WarrentyRegisterSerializer

class WarrentyRegisterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WarrentyRegisterModel.objects.all()
    serializer_class = WarrentyRegisterSerializer
