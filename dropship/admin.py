from django.contrib import admin

from .models import User, Project, Issue,CommentIssue,Label,Sprint

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(CommentIssue)
admin.site.register(Label)
admin.site.register(Sprint)