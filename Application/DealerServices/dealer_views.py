from Application import ProductServices
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

from Application.ProductServices.product_models import Product
from Application.PersonalDatas.personal_serializers import PhoneNumbersSerializer, PhoneNumbers as UserPhoneNumber

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
        state_query = request.GET.get('state', '').strip()
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
            if state_query:
                mains = mains.filter(district__state__name__iexact=state_query)

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
            if state_query:
                subs = subs.filter(state__iexact=state_query)

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
        data = request.data.copy()

        franchise_name = data.get('franchise')
        phone = data.get('phone')
        fullname = data.get('fullname')

        if phone and not UserPhoneNumber.objects.filter(phone_number=phone).exists():
            ph_serializer = PhoneNumbersSerializer(data={'phone_number': phone, 'name': fullname})
            if ph_serializer.is_valid():
                ph_serializer.save()

        sub_franchise = SubFranchaseModel.objects.filter(name=franchise_name).first()
        target_franchise = None
        
        if sub_franchise:
            data['franchise'] = sub_franchise.main_franchase.name
            target_franchise = sub_franchise
        else:
            main_franchise = MainFranchaseModel.objects.filter(name=franchise_name).first()
            if main_franchise:
                target_franchise = main_franchise
            
        serializer = WarrantyRegisterSerializers(data=data)
        if serializer.is_valid():
            warranty = serializer.save()
            
            if target_franchise:
                from Application.DealerServices.dealer_mails import send_warranty_registration_email
                send_warranty_registration_email(warranty, target_franchise)
                
            return Response({
                "massage": "Warranty registered successfully",
                "status": status.HTTP_200_OK,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductModelsAPIview(APIView):
    def get(self, request):
        search = request.GET.get('search', '').strip()
        if search:
            products = Product.objects.filter(name__icontains=search).values('name', 'warranty').distinct()
        else:
            products = Product.objects.values('name', 'warranty').distinct()
        
        return Response({"status": "success", "data": list(products)}, status=status.HTTP_200_OK)

class StateAPIview(APIView):
    def get(self, request):
        states = State.objects.prefetch_related('districts').all()
        data = {
            state.name: DistrictSerializerWarranty(state.districts.all(), many=True).data
            for state in states
        }
        return Response(data, status=status.HTTP_200_OK)