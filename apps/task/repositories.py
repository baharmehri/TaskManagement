from apps.base.repository import BaseRepository
from apps.task.models import Task


class TaskRepository(BaseRepository):
    model = Task

    @classmethod
    def update_task(cls, task: Task, **kwargs) -> Task:
        for key, value in kwargs.items():
            if value is not None:
                setattr(task, key, value)
        task.save()
        return task
