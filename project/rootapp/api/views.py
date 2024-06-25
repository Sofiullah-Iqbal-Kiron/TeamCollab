from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from ..models import User, Project, Task, Comment
from .serializers import UserSerializer, UserRegistrationSerializer, ProjectSerializer, TaskSerializer, CommentSerializer


class UserRegister(APIView):
    """
    Register as a new User.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        content = {
            'required fields': ['username', 'email', 'password', 'password_confirmation'],
            'optional fields': ['first_name', 'last_name']
        }

        return Response(content, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        registered_user = serializer.save()
        registered_user_serialize = UserSerializer(registered_user)

        return Response(registered_user_serialize.data, status=status.HTTP_201_CREATED)


class UserViewSet(ModelViewSet):
    """
    Retrieve, Update, Delete a single user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        content = {
            'detail': 'User creation or registration is not allowed via this endpoint.'
        }

        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProjectViewSet(ModelViewSet):
    """
    List, Retrieve, Create, Update, Delete projects.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True)
    def tasks(self, request, pk):
        project = get_object_or_404(self.get_queryset(), pk=pk)
        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskViewSet(ModelViewSet):
    """
    List, Retrieve, Create, Update and Delete tasks.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request):
        content = {
            'detail': "Listing tasks via that endpoint aren't allowed."
        }

        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def create(self, request):
        content = {
            'detail': "Creating task via that endpoint aren't allowed."
        }
        
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @action(detail=True)
    def comments(self, request, pk):
        task = get_object_or_404(self.get_queryset(), pk=pk)
        comments = Comment.objects.filter(task=task)
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request):
        content = {
            'detail': "Listing comments via that endpoint aren't allowed."
        }

        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def create(self, request):
        content = {
            'detail': "Making comments aren't allowed via that endpoint."
        }

        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
