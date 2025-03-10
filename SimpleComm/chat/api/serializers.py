from rest_framework import serializers

from chat.models import User, Room, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name',]

    def create(self, validated_data):
        print('validated_data: ', validated_data)
        return Room.objects.create(**validated_data)


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['user', 'text', 'room']

    def create(self, validated_data):
        return Message.objects.create(**validated_data)
