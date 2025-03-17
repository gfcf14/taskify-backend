from rest_framework import generics
from rest_framework.decorators import api_view
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectListView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        sort_by = self.request.query_params.get('sort_by', None)

        if (sort_by == 'status'):
            queryset = queryset.order_by('status')

        return queryset

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        sort_by = self.request.query_params.get('sort_by', None)

        if  (sort_by == 'status'):
            queryset = queryset.order_by('status')

        return queryset

@api_view(['GET'])
def get_totals(request):
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()

    return JsonResponse({"total_projects": total_projects, "total_tasks": total_tasks})