from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    is_overdue = serializers.SerializerMethodField()
    remaining_time = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'user', 'user_username', 'title', 'description', 'image',
                  'status', 'created_at', 'deadline', 'completed_at', 'updated_at',
                  'is_overdue', 'remaining_time')
        read_only_fields = ('id', 'user', 'created_at', 'completed_at', 'updated_at')

    def get_is_overdue(self, obj):
        from django.utils import timezone
        if obj.status == 'pending' and obj.deadline < timezone.now():
            return True
        return False

    def get_remaining_time(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        if obj.status == 'completed':
            return None
        
        now = timezone.now()
        remaining = obj.deadline - now
        
        if remaining.total_seconds() <= 0:
            return '已过期'
        
        days = remaining.days
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        
        if days > 0:
            return f'{days}天{hours}小时'
        elif hours > 0:
            return f'{hours}小时{minutes}分钟'
        else:
            return f'{minutes}分钟'
