from rest_framework import generics
from rest_framework.decorators import api_view
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        project_id = self.request.query_params.get('id', None)

        return Task.objects.filter(project=project_id)

@api_view(['GET'])
def get_totals(request):
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()

    return JsonResponse({"total_projects": total_projects, "total_tasks": total_tasks})