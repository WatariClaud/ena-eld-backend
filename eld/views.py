from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .serializers import DriverLoginSerializer, DriverSerializer, StatusChangeSerializer, DailyLogSerializer
from .models import DailyLog, StatusChange, Driver
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.views import APIView

class EldLogViewSet(viewsets.ModelViewSet):
    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        driver = Driver.objects.filter(user=self.request.user).first()
        if driver:
            return DailyLog.objects.filter(driver=driver).prefetch_related('status_changes')
        return DailyLog.objects.none()

    def create(self, request):
        driver = Driver.objects.filter(user=request.user).first()
        if not driver:
            return Response(
                {"error": "Driver profile not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        log_date = request.data.get("date") or timezone.localdate().isoformat()
        
        print(f"Driver found: {driver}") # Will print the Driver object
        print(f"Log date to be used: {log_date}")
        data = {**request.data, "date": log_date}
        serializer = self.get_serializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save(driver=driver)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='update-status')
    def update_driver_status(self, request):
        try:
            driver = Driver.objects.get(user=request.user)
        except Driver.DoesNotExist:
            return Response(
                {"error": "Driver profile not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        log_date = timezone.localdate(timezone.now())

        daily_log, created = DailyLog.objects.get_or_create(
            driver=driver,
            date=log_date
        )

        serializer = StatusChangeSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                {"error": "Invalid request data", "details": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        status_change = serializer.save(log=daily_log)

        return Response(
            StatusChangeSerializer(status_change).data,
            status=status.HTTP_201_CREATED
        )

class DriverViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]  # no auth for create
        return [IsAuthenticated()] 

    def create(self, request, *args, **kwargs):
        if Driver.objects.filter(user__username=request.data.get("name")).exists():
            return Response(
                {"error": "Driver with this name already exists."},
                status=400
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        driver = serializer.save()
        print(driver)
        if(driver):
            return Response(
                {
                    "id": driver.id,
                    "name": driver.user.username,
                    "car_registration_number": driver.car_registration_number
                },
                status=201
            )
        
        return Response(
            {
                "error": "driver does not exist",
            },
            status=400
        )

class DriverLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DriverLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            driver = Driver.objects.get(user=user)
        except Driver.DoesNotExist:
            return Response({"error": "Driver profile not found"}, status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "id": driver.id,
            "name": user.username,
            "car_registration_number": driver.car_registration_number,
            "token": token.key
        })
