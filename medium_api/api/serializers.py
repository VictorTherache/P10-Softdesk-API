from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import Projet, Issue, Contributor, Comments, User


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'password', 'password2', 'email')
        extra_kwargs = {
            'password': {'write_only': True},
        }


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


    def create(self, validated_data):
        """
        Register method, validates the date
        """
        user = User.objects.create(
            username=validated_data['first_name'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


    def update(self, instance, validated_data):
        """
        Update the current user
        """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


class IssueSerializer(serializers.ModelSerializer):
    """
    Issue Serializer
    """
    class Meta:
        model = Issue
        fields = ('id', 'title', 'projet', 'description',
                  'tag', 'priority', 'status', 'comments', 
                  'author_user_id', 'assigned_user')


class ContributorSerializer(serializers.ModelSerializer):
    """
    Contributor Serializer
    """
    def get_user(self, obj):
        """
        Display the user with his name
        """
        return f'{obj.user.first_name} {obj.user.last_name}'

    class Meta:
        model = Contributor
        fields = ('id', 'user', 'projet')


class ProjetSerializer(serializers.ModelSerializer):
    """
    Project Serializer
    """
    author = serializers.ReadOnlyField(source='author.first_name')
    issues = serializers.StringRelatedField(many=True)
    contributors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Projet
        fields = ('id', 'title', 'description', 'type',
                  'issues', 'author', 'contributors')


class CommentsSerializer(serializers.ModelSerializer):
    """
    Comment Serializer
    """
    author = serializers.ReadOnlyField(source='author.first_name')
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'description', 'issue', 'author', 'created_at')
