from rest_framework.exceptions import NotFound

from apps.task.repositories import TaskRepository


class TaskService:
    @staticmethod
    def get_task_by_id(task_id):
        task = TaskRepository.get(task_id)
        if not task:
            raise NotFound('Task not found')
        return task

    @staticmethod
    def create_task(validated_data):
        task = TaskRepository.create(
            title=validated_data["title"],
            description=validated_data["description"]
        )
        return task

    def update_task(self, task_id, validated_data):
        task = self.get_task_by_id(task_id)

        task = (TaskRepository.update_task(
            task,
            title=validated_data.get("title"),
            description=validated_data.get("description")
        ))
        return task

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        TaskRepository.delete(task)

    def get_all_tasks(self):
        tasks = TaskRepository.all()
        return tasks
