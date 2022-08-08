from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
# get all project,particular
router.register('projectList', views.ProjectList,basename="proj")

# crud operation only manager (use/projectname to do crud on individual)
router.register('project',views.ProjectCrud,basename='project')

# get all issue and single on (id)
router.register('issueList', views.IssueList,basename="isL")

# crud on issue only manager (use /issueid to do crud on individual)
router.register('issue',views.IssueCrud,basename='issu')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    # get all issue under project
    path('projectsissue/<str:pro>/',views.ProjectIssue.as_view()),
    # get particular issue under partiular 
    path('projectsissue/<str:pro>/<int:id>/',views.IssueDetail.as_view()),
    
    # issue create under particular
    path('issuecreate/<str:pro>',views.IssueCreate.as_view()),
    # issue update,delete particular
    path('issueupdate/<str:pro>/<int:id>',views.IssueUpdate.as_view()),

    # assigntouser
    path('issueassign/<str:pro>/<int:id>',views.IssueAssign.as_view()),
  
    # user update status
    path('statusupdate/<str:pro>/<int:id>',views.StatusUpdate.as_view()),
   
    # search on title desc
    path('search/<str:key>',views.SearchIssue.as_view())
    
]