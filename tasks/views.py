from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectView(generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        queryset = Project.objects.all()
        serializer_class = ProjectSerializer

        if 'pk' in kwargs:
            project_id = kwargs['pk']
            tasks = Task.objects.filter(project=project_id)
            serializer = TaskSerializer(tasks, many=True)
        else:
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = ProjectSerializer(project, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs['id'])
        project.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

@api_view(['GET'])
def get_totals(request):
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()

    return JsonResponse({"total_projects": total_projects, "total_tasks": total_tasks})