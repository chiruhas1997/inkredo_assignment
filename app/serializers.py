from rest_framework import serializers
from django.contrib.auth.models import User
from .models import HolidayHomes, Rooms, HomeImages

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class SerialLogin(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=200)


class CreateHomeSerializer(serializers.Serializer):
    home_name = serializers.CharField()
    city = serializers.CharField()
    noumber_of_rooms = serializers.IntegerField()

class RoomSerializer(serializers.Serializer):
    rents = serializers.CharField()
    availibility = serializers.BooleanField()
    rooom_id = serializers.CharField()
    check_in = serializers.DateTimeField()
    check_out = serializers.DateTimeField()
    rules = serializers.CharField()

class EditRoomSerializer(serializers.Serializer):
    rents = serializers.CharField()
    availibility = serializers.BooleanField()
    check_in = serializers.DateTimeField()
    check_out = serializers.DateTimeField()
    rules = serializers.CharField()

class ViewOwnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class ViewHomesSerializers(serializers.ModelSerializer):
    class Meta:
        model = HolidayHomes
        fields = ('home_name','city','no_rooms')

class ViewRoomsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        #fields = '__all__'
        exclude = ('holiday_homes','id')

class ImageListSerializers(serializers.ModelSerializer):
    class Meta:
        model = HomeImages
        fields = ('image',)