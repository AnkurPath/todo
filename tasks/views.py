from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

import requests
import json
from pathlib import Path

def home(request):
    config = get_config()

    endpoint = f"https://app.asana.com/api/1.0/tasks?opt_fields=name,notes,due_on,start_on,gid,status&project={config['gid']}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {config['bearer-token']}"
    }

    res = requests.get(endpoint, headers=headers).json()

    return render(request, 'home.html', {'tasks':res})

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

        config = get_config()

        endpoint = "https://app.asana.com/api/1.0/tasks"
        headers = {"Authorization": "Bearer "+config['bearer-token'],
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
                    config["gid"]
                ],
                "start_on": data['start_date']
            }
        }

        res = requests.post(endpoint, headers=headers, data=json.dumps(task))

        if res.status_code==200:
            messages.success(request, "Task added")
        else:
            messages.error(request, "Task could not be added")
        
    return redirect(home)

@csrf_exempt
def update_task(request, gid):
    config = get_config()
    
    endpoint = f"https://app.asana.com/api/1.0/tasks/{gid}"
    
    headers = {"Authorization": "Bearer "+config['bearer-token'],
    "Content-Type": "application/json",
    "Accept": "application/json"}

    data = {
        "title": request.POST.get('title'),
        "notes": request.POST.get('notes'),
        "start_date": request.POST.get('start_Date'),
        "due_date": request.POST.get('due_Date'),
        "status": request.POST.get('status')
    }

    task = {
        "data": {
            "assignee": "me",
            "assignee_status": data["status"],
            "due_on": data["due_date"],
            "name": data["title"],
            "notes": data["notes"],
            "start_on": data['start_date']
        }
    }
    
    res = requests.put(endpoint, headers=headers, data=json.dumps(task))
    
    if res.status_code==200:
        messages.success(request, "Task edited successfully")
    else:
        messages.error(request, "Task could not be edited")

    return redirect(home)

@csrf_exempt
def delete_task(request, gid):
    config = get_config()

    endpoint = f"https://app.asana.com/api/1.0/tasks/{gid}"
    headers = {"Authorization": "Bearer "+config['bearer-token'],
    "Accept": "application/json"}

    res = requests.delete(endpoint, headers=headers)

    if res.status_code==200:
        messages.success(request, "Task deleted")
    else:
        messages.error(request, "Delete request failed")

    return redirect(home)

def get_config():
    BASE_DIR = Path(__file__).resolve().parent.parent

    with open(BASE_DIR / "configuration.json", "r") as f:
            configs = json.load(f)
    
    return configs