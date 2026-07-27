from agents.models import Task


def get_tasks():

    tasks = Task.objects.all().order_by("-created_at")

    data = []

    for task in tasks:
        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "created_at": task.created_at
        })

    return data