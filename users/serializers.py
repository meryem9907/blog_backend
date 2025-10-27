from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import Author

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = Author
        fields = ["username", "email", "password", "password2"]

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = Author(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    # object level validation
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        validate_password(data["password"])
        return data

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'email', 'username']

class WritableAuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=False, style={"input_type": "password"})

    class Meta:
        model = Author
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {'username': {'required': False}, 'email':{'required': False}}

