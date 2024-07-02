from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

from ..models import Project
from .serializers import ProjectSerializer


class ProjectList(ListAPIView):
    '''
    List all projects where this user is owner.
    '''

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [SearchFilter]
    search_fields = ['owner__id']
