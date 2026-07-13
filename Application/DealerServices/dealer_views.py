from Application.DealerServices.dealer_serializers import DistrictSerializer
from rest_framework.decorators import permission_classes
from rest_framework import generics
from .dealer_models import *
from .dealer_serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class CountryListCreate(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

@permission_classes([AllowAny])
class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class StateListCreate(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

@permission_classes([AllowAny])
class StateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class DistrictListCreate(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

@permission_classes([AllowAny])
class DistrictDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class FranchasiessList(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        search_query = request.GET.get('search', '').strip()
        district_query = request.GET.get('district', '').strip()
        franchise_type = request.GET.get('type', '').strip()

        franchises_data = []

        # Get Neo Premium (MainFranchaseModel)
        if not franchise_type or franchise_type == 'neo_premium':
            mains = MainFranchaseModel.objects.filter(is_available=True)
            
            if search_query:
                mains = mains.filter(
                    Q(name__icontains=search_query) | 
                    Q(address__icontains=search_query) |
                    Q(district__name__icontains=search_query)
                )
            if district_query:
                mains = mains.filter(district__name__iexact=district_query)

            for m in mains:
                franchises_data.append({
                    'id': m.id,
                    'type': 'neo_premium',
                    'type_label': 'Neo Premium',
                    'name': m.name,
                    'district_name': m.district.name if m.district else '',
                    'address': m.address,
                    'phone': m.phone,
                    'email': m.email,
                    'location_link': m.location_link,
                })

        # Get Neo Standard (SubFranchaseModel)
        if not franchise_type or franchise_type == 'neo_standard':
            subs = SubFranchaseModel.objects.filter(is_available=True)
            
            if search_query:
                subs = subs.filter(
                    Q(name__icontains=search_query) | 
                    Q(address__icontains=search_query) |
                    Q(district__icontains=search_query)
                )
            if district_query:
                subs = subs.filter(district__iexact=district_query)

            for s in subs:
                franchises_data.append({
                    'id': s.id,
                    'type': 'neo_standard',
                    'type_label': 'Neo Standard',
                    'name': s.name,
                    'district_name': s.district,  # CharField in SubFranchaseModel
                    'address': s.address,
                    'phone': s.phone,
                    'email': s.email,
                    'location_link': s.location_link,
                })

        return Response({"status": "success", "data": franchises_data}, status=status.HTTP_200_OK)

class WarrantyRegisterAPIvie(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = WarrantyRegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "massage": "Warranty registered successfully",
                "status": status.HTTP_200_OK,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

