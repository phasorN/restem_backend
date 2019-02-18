from django.contrib.auth.models import User
from rest_framework import serializers
from main import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name' , 'groups', 'password')

    def validate_email(self, value):
        if User.objects.filter(email = value).count():
            raise serializers.ValidationError("Email Already Registered")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class ExpenseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = models.Expense
        fields = ('id', 'title', 'amount', 'description', 'date', 'owner')