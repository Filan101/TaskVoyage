from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        sort = self.request.query_params.get('sort')
        if sort == 'name':
            queryset = queryset.order_by('title')
        elif sort == 'createdAt':
            queryset = queryset.order_by('-created_at')
        elif sort == 'status':
            queryset = queryset.order_by('status')
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': '任务创建成功',
            'task': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': '任务更新成功',
            'task': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': '任务删除成功'
        }, status=status.HTTP_200_OK)


class TaskStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.utils import timezone
        from datetime import timedelta
        
        user = request.user
        now = timezone.now()
        
        all_tasks = Task.objects.filter(user=user)
        completed_tasks = all_tasks.filter(status='completed')
        pending_tasks = all_tasks.filter(status='pending')
        overdue_tasks = pending_tasks.filter(deadline__lt=now)
        upcoming_tasks = pending_tasks.filter(deadline__gt=now).order_by('deadline')[:5]
        
        return Response({
            'total': all_tasks.count(),
            'completed': completed_tasks.count(),
            'pending': pending_tasks.count(),
            'overdue': overdue_tasks.count(),
            'completion_rate': round(completed_tasks.count() / all_tasks.count() * 100, 1) if all_tasks.count() > 0 else 0,
            'upcoming': TaskSerializer(upcoming_tasks, many=True).data
        })
