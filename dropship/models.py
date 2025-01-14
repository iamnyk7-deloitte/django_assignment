
from cmath import pi
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
    username=models.CharField(max_length=30,primary_key=True)
    is_manager = models.BooleanField(
        'manager status',
        default=False,
    )
    def __str__(self):
        return self.username


class Project(TimestampModel,models.Model):
   
    title = models.CharField(max_length=128,primary_key=True)
    description = models.TextField()
    creator=models.ForeignKey(User,on_delete=models.CASCADE,related_name=
        "creator")
    

    def __str__(self):
        return  self.title

class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project', null=False)
    sprint_title = models.CharField(max_length=30)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True, null=True)
    sprint_status = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return  self.sprint_title


class Label(models.Model):
    label = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return  self.label

class Issue(TimestampModel,models.Model):
    BUG = "BUG"
    TASK = "TASK"
    STORY = "STORY"
    EPIC = "EPIC"
    TYPES = [(BUG, BUG), (TASK, TASK), (STORY, STORY), (EPIC, EPIC)]

    OPEN = 'open'
    INPRGRESS = 'in progress'
    INREVIEW = 'in review'
    CodeComplete = 'code complete '
    QATesting = 'qa testing'
    DONE = 'done'
    STATUS = [(OPEN, OPEN), (INPRGRESS, INPRGRESS), (INREVIEW, INREVIEW), (CodeComplete, CodeComplete),
              (QATesting, QATesting), (DONE, DONE)]

    title = models.CharField(max_length=128)
    description = models.TextField()

    type = models.CharField(max_length=8, choices=TYPES, default=BUG, null=False)

    project= models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issue", null=False
    )

    assigned=models.ForeignKey(User,on_delete=models.CASCADE,related_name=
        "assigned")
    
    watchers=models.ManyToManyField(User,related_name=
        "watchers")

    status=models.CharField(max_length=128,choices=STATUS)
    labels = models.ManyToManyField(Label,related_name="labels" )
    sprint = models.ForeignKey(Sprint, blank=True, related_name='sprint', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return "{0} -- {1}".format(self.project.creator, self.title)
        
        


class CommentIssue(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user', null=False)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue', null=False)

    def __str__(self):
        return "{0} -- {1}".format(self.user.username, self.comment)
        