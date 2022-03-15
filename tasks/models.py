from django.db import models

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    notes = models.TextField()
    start_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20)
    gid = models.TextField(null=True)