from rest_framework import serializers

from apps.task.models import Task


class TaskCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class TaskUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)


class TaskOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
