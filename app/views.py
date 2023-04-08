from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# Create your views here.
from rest_framework import status,generics, permissions
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from . models import HolidayHomes, Rooms, HomeImages
from . serializers import (UserSerializer, RegisterSerializer, SerialLogin, CreateHomeSerializer, RoomSerializer, EditRoomSerializer,
                          ViewOwnersSerializer, ViewHomesSerializers, ViewRoomsSerializers, ImageListSerializers)

@api_view(['GET'])
def index(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        return Response({
            "base" : "http://127.0.0.1:8000/api",
            "register": "http://127.0.0.1:8000/register",
            "testing": "http://127.0.0.1:8000/testing",
            "login": "http://127.0.0.1:8000/login",
            "create_home": "http://127.0.0.1:8000/create_home",
            "home/<home_name>": "http://127.0.0.1:8000/home/<home_name>",
            'add_room/<home_name>': "http://127.0.0.1:8000/add_room/<home_name>",
            'room/<home_name>/<room_id>': "http://127.0.0.1:8000/room/<home_name>/<room_id>",
            'list_owners/': "http://127.0.0.1:8000/list_owners",
            'list_homes/<owner>': "http://127.0.0.1:8000/list_homes/<owner>",
            'list_rooms/<owner>/<homes>': "http://127.0.0.1:8000/list_rooms/<owner>/<homes>",
            'add_images/<home_name>': "http://127.0.0.1:8000/add_images/<home_name>",
            'list_images/<owner>/<home>': "http://127.0.0.1:8000/list_images/<owner>/<home>"})
@api_view(['GET'])
def list_owners(request):
    receivers = User.objects.all()
    serializer = ViewOwnersSerializer(receivers, many = True)

    return Response({"status":200, "payload": serializer.data})

@api_view(['GET','POST'])
def list_rooms(request, owner, homes):

    try:
        user_obj = User.objects.get(username=owner)
        homes_objs = HolidayHomes.objects.get(user_name = user_obj, home_name = homes)

        rooms_obj = Rooms.objects.filter(holiday_homes = homes_objs)
        serializer = ViewRoomsSerializers(rooms_obj, many = True)
        return Response({"status":200, "payload": serializer.data})
    except:
        return Response({"status":500, "payload": "no matching query "})

@api_view(['GET','POST'])
def list_images(request, owner, home):
    try:
        user_obj = User.objects.get(username=owner)
        homes_objs = HolidayHomes.objects.get(user_name = user_obj, home_name = home)

        img_obj = HomeImages.objects.filter(holiday_homes = homes_objs)
        serializer = ImageListSerializers(img_obj, many = True)
        return Response({"status":200, "payload": serializer.data})
    except:
        return Response({"status":500, "payload": "no matching query "})

@api_view(['GET','POST'])
def list_homes(request, owner):
    print(owner)

    try:
        user_obj = User.objects.get(username=owner)
        homes_objs = HolidayHomes.objects.filter(user_name = user_obj)
        serializer = ViewHomesSerializers(homes_objs, many = True)
        return Response({"status":200, "payload": serializer.data})
    except:
        return Response({"status":500, "payload": "no matching query "})

class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        Token.objects.get_or_create(user=user)
        return Response({
            "status":200,
            "meaasge" : "user created"
        })

@api_view(['GET','POST'])
def login(request):
    if request.method == 'GET':
        return Response({"status":500,'message':"This api has only POST method"})

    elif request.method == 'POST':
        serializer = SerialLogin(data=request.data)
        print(request.data)
        if serializer.is_valid():
            print(serializer.data['username'])
            user = authenticate(request, username = serializer.data['username'], password = serializer.data['password'])
            if user is not None:
                print('user valid')
                token= Token.objects.get(user=user)
                print(token)
                return Response({"status":200,'token':str(token),'status':'success'}, status=status.HTTP_201_CREATED)
            return Response({"status":500,'message':'wrong cradentials'}, status=status.HTTP_201_CREATED)
            print(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def testing(request):
    return Response({
            "logged in as" : str(request.user)
        })

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def register_home(request):
    if request.method == 'POST':
        serializer = CreateHomeSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data['home_name'])

            try :
                HolidayHomes.objects.create(user_name = request.user, home_name = serializer.data['home_name'], city = serializer.data['city'], no_rooms=serializer.data['noumber_of_rooms'])
                return Response({"status":200,'message': "holiday home " +serializer.data['home_name']+' created'})
            except:
                return Response({"status":200,"error":"holiday home "+serializer.data['home_name']+' already exists'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def home(request,home_name):
    if request.method == 'GET':
        if HolidayHomes.objects.filter(user_name = request.user, home_name = home_name).exists():
            homeobj = HolidayHomes.objects.get(user_name = request.user, home_name = home_name)

            return Response({"status":200,'holiday home name': homeobj.home_name, 'city':homeobj.city, 'number of rooms':homeobj.no_rooms})
        else :
            return Response({'no holiday home with name '+home_name+' under '+str(request.user)})
    if request.method == 'DELETE':
        if HolidayHomes.objects.filter(user_name = request.user, home_name = home_name).exists():
            homeobj = HolidayHomes.objects.get(user_name = request.user, home_name = home_name)
            homeobj.delete()
            return Response({"status":200,'holiday home name': homeobj.home_name + ' city deleated'})
        else :
            return Response({"status":500,"message":'no holiday home with name '+home_name+' under '+str(request.user)})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_room(request,home_name):
    if len(HolidayHomes.objects.filter(user_name = request.user, home_name = home_name))<1:
        print("this should not happen")
        return Response({"status":500,"message":'no holiday home with name '+home_name+' under '+str(request.user)})

    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        home_obj = HolidayHomes.objects.get(user_name = request.user, home_name = home_name)
        if len(Rooms.objects.filter(holiday_homes = home_obj)) == home_obj.no_rooms:
            return Response({"status":500,'Error': "All rooms have been created"})
        if Rooms.objects.filter(holiday_homes = home_obj, rooom_id = serializer.data['rooom_id']).exists():
            return Response({"status":500,'Error': "room already exists"})
        else:
            Rooms.objects.create(holiday_homes = home_obj
                                ,rents = serializer.data['rents']
                                ,rooom_id = serializer.data['rooom_id']
                                ,availibility = serializer.data['availibility']
                                ,check_in = serializer.data['check_in']
                                ,check_out =serializer.data['check_out']
                                ,rules = serializer.data['rules'])
            return Response({'Message': "room added"})
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET','DELETE','PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def room(request,home_name,room_id):
    if len(HolidayHomes.objects.filter(user_name = request.user, home_name = home_name))<1:
        print("this should not happen")
        return Response({"status":500,'error':'no holiday home with name '+home_name+' under '+str(request.user)})
    else:
        home_obj = HolidayHomes.objects.get(user_name = request.user, home_name = home_name)
        if not Rooms.objects.filter(holiday_homes = home_obj, rooom_id = room_id).exists():
            return Response({"status":500,'error':'no room with is '+room_id+' in '+home_name})
        if request.method == 'GET':
            room_obj = Rooms.objects.get(holiday_homes = home_obj, rooom_id = room_id)
            return Response({
                "status":200,
                'rooom_id':room_obj.rooom_id,
                'rents':room_obj.rents,
                'availibility':room_obj.availibility,
                'check_in':room_obj.check_in,
                'check_out':room_obj.check_out,
                'rules':room_obj.rules
            })
        if request.method == "DELETE":
            room_obj = Rooms.objects.get(holiday_homes = home_obj, rooom_id = room_id)
            room_obj.delete()
            return Response({"status":500,"message":"room deleated"})
        if request.method == "PUT":
            serializer = EditRoomSerializer(data = request.data)
            if serializer.is_valid():
                room_obj = Rooms.objects.get(holiday_homes = home_obj, rooom_id = room_id)
                room_obj.rents = serializer.data['rents']
                room_obj.availibility = serializer.data['availibility']
                room_obj.check_in = serializer.data['check_in']
                room_obj.check_out = serializer.data['check_out']
                room_obj.rules = serializer.data['rules']
                room_obj.save()
                return Response({"status":200,"message":"Details updated"})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_images(request,home_name):

    try:
        home_obj = HolidayHomes.objects.get(user_name = request.user, home_name = home_name)
        file = request.data['image']
        home_obj = HomeImages.objects.create(holiday_homes = home_obj, image = file)
        return Response({"status":200, "message": "image uploaded"})
    except:
        return Response({"ststus":500, "message": "Bad request"})
