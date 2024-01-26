from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
            'email',
            'first_name',
            'last_name',
            'created_time',
        ]
        extra_kwargs = {
            'age': {'format': '%Y-%m-%d'},
            'password': {'write_only': True},
        }


class UserDetailSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    can_be_contacted = serializers.SerializerMethodField()
    can_data_be_shared = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
            'email',
            'first_name',
            'last_name',
            'created_time',
        ]

    def get_age(self, instance):
        return instance.age

    def get_can_be_contacted(self, instance):
        return instance.can_be_contacted

    def get_can_data_be_shared(self, instance):
        return instance.can_data_be_shared

    def get_created_time(self, instance):
        return instance.created_time
