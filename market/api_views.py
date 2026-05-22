from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Student, Course, Teacher, Enrollment
from .serializers import StudentSerializer, CourseSerializer, TeacherSerializer, EnrollmentSerializer, UserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().prefetch_related('enrollments__course')
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def filter_by_level(self, request):
        level = request.query_params.get('level')
        qs = self.get_queryset()
        if level:
            qs = qs.filter(level=level)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def filter_by_hours(self, request):
        hours = request.query_params.get('hours')
        qs = self.get_queryset()
        if hours:
            qs = qs.filter(hours=hours)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home_page')
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST.get('email', '')
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password, email=email)
        Token.objects.create(user=user)
        login(request, user)
        return redirect('home_page')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')
