from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action


from ..models import User, Project, Task, Comment
from .serializers import UserSerializer, UserRegistrationSerializer, ProjectSerializer, TaskSerializer, TaskCreateSerializer, CommentSerializer, CommentCreateSerializer


class UserRegister(CreateAPIView):
    """
    Register as a new User.
    """

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        data = request.data
        serializer = UserRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        registered_user = serializer.save()
        registered_user_serializer = UserSerializer(registered_user)

        return Response(registered_user_serializer.data, status=status.HTTP_201_CREATED)


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


class TaskListCreate(ListCreateAPIView):
    """
    List and Create task for specified project.
    """

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    projects = Project.objects.all()

    def get(self, request, pk):
        project = get_object_or_404(self.projects, pk=pk)
        tasks = self.get_queryset().filter(project=project)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        project = get_object_or_404(self.projects, pk=pk)
        data = request.data
        serializer = TaskCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        new_task = Task.objects.create(**serializer.validated_data, project=project)
        new_serializer = TaskSerializer(new_task)

        return Response(new_serializer.data, status=status.HTTP_201_CREATED)


class TaskViewSet(ModelViewSet):
    """
    List, Retrieve, Create, Update and Delete tasks.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, pk):
        projects = Project.objects.all()
        project = get_object_or_404(projects, pk=pk)
        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentListCreate(ListCreateAPIView):
    """
    List and Create comment for specified task.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    tasks = Task.objects.all()

    def get(self, request, pk):
        task = get_object_or_404(self.tasks, pk=pk)
        comments = self.get_queryset().filter(task=task)
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        task = get_object_or_404(self.tasks, pk=pk)
        data = request.data
        serializer = CommentCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        new_comment = Comment.objects.create(**serializer.validated_data, task=task)
        new_serializer = CommentSerializer(new_comment)

        return Response(new_serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
