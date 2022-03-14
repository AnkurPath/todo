
from django.urls import path
from tasks import views

urlpatterns = [
    path('home',views.home),
    path('add-task',views.add_task),
    path('update-task/<int:id>',views.update_task),
    path('delete-task/<int:id>',views.delete_task)
]