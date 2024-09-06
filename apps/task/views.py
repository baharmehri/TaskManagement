from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from apps.core.response import CustomResponse as response
from apps.task.serializers import TaskCreateInputSerializer, TaskOutputSerializer, TaskUpdateInputSerializer
from apps.task.services import TaskService


class TaskView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=TaskCreateInputSerializer,
        summary="Create a task",
        description="This endpoint creates a new task.",
        responses=TaskOutputSerializer
    )
    def post(self, request):
        data = TaskCreateInputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            task = TaskService.create_task(data.data)
        except Exception:
            return response.error_response("An internal error occurred.", status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response.data_response(TaskOutputSerializer(task).data, "Task created successfully.",
                                      status.HTTP_201_CREATED)

    @extend_schema(
        summary="Get list of tasks",
        description="This endpoint lists all tasks.",
        responses=TaskOutputSerializer(many=True)
    )
    def get(self, request):
        try:
            tasks = TaskService().get_all_tasks()
        except Exception:
            return response.error_response("An internal error occurred.", status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response.data_response(TaskOutputSerializer(tasks, many=True).data, "List of tasks.",
                                      status=status.HTTP_200_OK)


class TaskUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Get a task.",
        description="This endpoint get a task.",
        responses=TaskOutputSerializer
    )
    def get(self, request, pk):
        try:
            task = TaskService.get_task_by_id(pk)
        except NotFound as e:
            return response.error_response(str(e), status.HTTP_404_NOT_FOUND)

        return response.data_response(TaskOutputSerializer(task).data, "Task retrieved successfully.",
                                      status=status.HTTP_200_OK)

    @extend_schema(
        request=TaskUpdateInputSerializer,
        summary="Update a task.",
        description="This endpoint update a task.",
        responses=TaskOutputSerializer

    )
    def put(self, request, pk):
        data = TaskUpdateInputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            task = TaskService().update_task(pk, data.data)
        except NotFound as e:
            return response.error_response(str(e), status.HTTP_404_NOT_FOUND)

        return response.data_response(TaskOutputSerializer(task).data, "Task updated successfully.",
                                      status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete a task.",
        description="This endpoint delete a task.",
        responses={200: {"description": "Task deleted successfully."}},
    )
    def delete(self, request, pk):
        try:
            TaskService().delete_task(pk)
        except NotFound as e:
            return response.error_response(str(e), status.HTTP_404_NOT_FOUND)

        return response.data_response({}, "Task deleted successfully.", status=status.HTTP_200_OK)
