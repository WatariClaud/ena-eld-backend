from rest_framework import serializers
from .models import STATUS_CHOICES, DailyLog, Driver, StatusChange
from django.contrib.auth.models import User

from rest_framework import serializers
from .models import StatusChange, STATUS_CHOICES

class StatusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusChange
        fields = ['status', 'timestamp', 'location', 'remarks']

    def validate_status(self, value):
        valid_choices = [choice[0] for choice in STATUS_CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"Invalid status '{value}'. Must be one of: {valid_choices}"
            )
        return value

    def validate(self, attrs):
        status = attrs.get("status")
        remarks = attrs.get("remarks", "").strip()

        # If status is ON, remarks must be provided
        if status == "ON" and not remarks:
            raise serializers.ValidationError({
                "remarks": "Remarks are required when status is 'On Duty (Not Driving)'."
            })

        return attrs

class DailyLogSerializer(serializers.ModelSerializer):
    status_changes = StatusChangeSerializer(many=True, read_only=True)

    class Meta:
        model = DailyLog
        fields = ['id', 'date', 'status_changes']
        read_only_fields = ['status_changes']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']  # ignoring password field, otherwise just add 'password' to fields list

class DriverSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Driver
        fields = ('id', 'car_registration_number', 'username', 'password')

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User.objects.create_user(username=username, password=password)

        # 3. Create the Driver object, now including the required 'user' field
        driver = Driver.objects.create(user=user, **validated_data)
        return driver
    
class DriverLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)