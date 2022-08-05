
from operator import mod
from django.contrib.auth.models import AbstractUser
from django.db import models

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser,models.Model):
    # If there are any fields needed add here.
    
    is_manager = models.BooleanField(
        'manager status',
        default=False,
    )
    def __str__(self):
        return self.username


class Project(TimestampModel,models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    code = models.CharField(max_length=64, unique=True, null=False)

    def __str__(self):
        return "{0} {1}".format(self.code, self.title)


class Issue(TimestampModel,models.Model):
    BUG = "BUG"
    TASK = "TASK"
    STORY = "STORY"
    EPIC = "EPIC"
    TYPES = [(BUG, BUG), (TASK, TASK), (STORY, STORY), (EPIC, EPIC)]

    title = models.CharField(max_length=128)
    description = models.TextField()

    type = models.CharField(max_length=8, choices=TYPES, default=BUG, null=False)

    project= models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project", null=False
    )

    assigned=models.ForeignKey(User,on_delete=models.CASCADE,related_name=
        "assigned")
    
    watchers=models.ManyToManyField(User,related_name=
        "watchers")

    status=models.CharField(max_length=128)
    
    def __str__(self):
        # return "{0} -- {1}".format(self.project.code, self.title)
        return self.id


