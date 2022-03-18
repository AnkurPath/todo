
from django.urls import path
from tasks import views

urlpatterns = [
    path('home',views.home),
    path('add-task',views.add_task),
    path('update-task/<int:gid>',views.update_task),
    path('delete-task/<int:gid>',views.delete_task)
]