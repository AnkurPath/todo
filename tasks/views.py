from django.shortcuts import redirect, render
from tasks.models import Post
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import Post

import requests
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

def home(request):
    tasks = Post.objects.all()
    return render(request, 'home.html', {'tasks':tasks})

@csrf_exempt
def add_task(request):
 
    data = {
        "title": request.POST.get('title'),
        "notes": request.POST.get('notes'),
        "start_date": request.POST.get('start_Date'),
        "due_date": request.POST.get('due_Date'),
        "status": request.POST.get('status')
    }

    
    if request.method=="POST":

        task = app_sync(data)

        form = Post(title=data['title'], notes=data['notes'], start_date=data['start_date'], 
                due_date=data['due_date'], status=data['status'],gid = task['data']['gid'])

        form.save()

        messages.success(request, "Task added")
        return redirect(home)
    
    messages.error(request, "Task could not be added")
    return redirect(home)

def update_task(request, id):
    task = Post.objects.get(id=id)
    form = Post(request.POST, instance=task)

    if form.is_valid():
        form.save()
        messages.success(request, "Task edited successfully")
        return redirect("home")
    
    messages.error(request, "Task could not be edited")
    return redirect("home")

def delete_task(request):
    task = Post.objects.get(id=id)
    task.delete()
    messages.success(request, "Task deleted")
    return redirect("home")

def app_sync(data):
    with open(BASE_DIR / "configuration.json", "r") as f:
            configs = json.load(f)

    endpoint = "https://app.asana.com/api/1.0/tasks"
    headers = {"Authorization": "Bearer "+configs['bearer-token'],
    "Content-Type": "application/json",
    "Accept": "application/json"}

    task = {
        "data": {
            "assignee": "me",
            "assignee_status": data["status"],
            "due_on": data["due_date"],
            "name": data["title"],
            "notes": data["notes"],
            "projects": [
                configs["gid"]
            ],
            "start_on": data['start_date']
        }
    }

    return requests.post(endpoint, headers=headers, data=json.dumps(task)).json()