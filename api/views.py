
from cProfile import label
from functools import partial
from re import L
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from requests import delete
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager
from api.serializers.managerserializer import IssueSerializer, LableSerializer,ProjectSerializer,IssueAssign,IssueStatus,CommentSerializer, SprintSerializer

from dropship.models import CommentIssue, Issue, Label,Project, Sprint, User
from rest_framework import viewsets,generics
from django.db.models import Q
from django.core import mail
from django.core.mail import EmailMessage,send_mass_mail,send_mail
from .paginationclass import custompaginate

from time import sleep
import datetime
from django_filters.rest_framework import DjangoFilterBackend

class ProjectList(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer

   

class ProjectCrud(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated,IsManager]
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer


class IssueList(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Issue.objects.all()
    serializer_class=IssueSerializer

   

class IssueCrud(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated,IsManager]
    queryset=Issue.objects.all()
    serializer_class=IssueSerializer


class ProjectIssue(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request,pro=None):
  
        if pro==None:
            return JsonResponse({'data':"enter"})
        else:
            
            p=Issue.objects.filter(project=pro)
           

            if len(p)>0:
                serializer = IssueSerializer(p,many=True)
                return JsonResponse({'data':serializer.data})
            else:
                return JsonResponse({'data':'doesnot exist'})

def send_email(mailu,pro,id,message):

    mails=[]
    for i in mailu:
      user_mail=User.objects.filter(pk=i).values('email').get()
      mails.append(user_mail['email'])
  
    issue_name=Issue.objects.filter(pk=id).values('title').get()
    title_mail="An Updated happend in the "+issue_name['title']+"ticket of the project :"+pro
                
    try: 
        
        send_mail(title_mail,message,'santu.nyk7@gmail.com',mails)
        print("yes")
       
       
    except Exception as e:
        print(e)
        
   

            
class IssueDetail(APIView):

    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated]

  
    def get(self, request,pro=None,id=None):
        if pro==None or id==None:
             return JsonResponse({'data':"enter"})
        else:
            p=Issue.objects.filter(project=pro,pk=id)
            print(serializers.serialize('json',p))
            if len(p)>0:
                serializer = IssueSerializer(p,many=True)
                return JsonResponse({'data':serializer.data})
            else:
                return JsonResponse({'data':'doesnot exist'})

class IssueCreate(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated,IsManager]

    def post(self,request,pro=None):
        if pro== None:
            return JsonResponse({'data':"enter"})
        else:
            p=Project.objects.filter(pk=pro)

            if len(p)>0: 
                datai=request.data
                datai['project']=pro
                serial=IssueSerializer(data=datai)
                if serial.is_valid():
                    serial.save()
                    return JsonResponse({'msg':"save"})
               
            else:
                 return JsonResponse({'data':"Project doest exist"})

class IssueUpdate(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated,IsManager]

    def patch(self,request,pro=None,id=None):
       
        if pro== None or id==None:
            return JsonResponse({'data':"enter"})
        else:  
            p=Issue.objects.get(project=pro,pk=id)
            serial=IssueSerializer(p,request.data,partial=True)
            if p:
                if serial.is_valid():
                    serial.save()
                    return JsonResponse({'Message':"Updated"})
                else:
                    return JsonResponse({'Message':"Enter Data properly"})
            else:
               return JsonResponse({'Message':"Doesnot exist"})
    
    def delete(self,request,pro=None,id=None):
        if pro== None or id==None:
            return JsonResponse({'data':"enter"})
        else:  
            try:
                p=Issue.objects.get(project=pro,pk=id)
                p.delete()
                return JsonResponse({'Message':"deleted"})
            except:
                return JsonResponse({'Message':"errror"})
    
class IssueAssign(APIView):
    
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated,IsManager]

    def patch(self,request,pro=None,id=None):
       
        if pro== None or id==None:
            return JsonResponse({'data':"enter"})
        else:  
            p=Issue.objects.get(project=pro,pk=id)
            mails=Issue.objects.filter(project=pro,pk=id).values_list('watchers').all()
            mailu=list(map(lambda x: x[0],list(mails)))
       
            serial=IssueSerializer(p,request.data,partial=True)
            if p:
                if serial.is_valid():
                    msg="New Assignee has been added to issue no"+id+"of project"+pro     
                    serial.save()
                    send_email(mailu,pro,id,message=msg)
                    return JsonResponse({'Message':"Updated"})
                else:
                    return JsonResponse({'Message':'user doesnot exits'})
            else:
               return JsonResponse({'Message':"Doesnot exist"})

class StatusUpdate(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated]
    
    def patch(self,request,pro=None,id=None):
       
        if pro== None or id==None:
            return JsonResponse({'data':"enter"})
        else:  
            p=Issue.objects.get(project=pro,pk=id)
            q=Issue.objects.filter(project=pro,pk=id).values_list('assigned').get()
            mails=Issue.objects.filter(project=pro,pk=id).values_list('watchers').all()
            mailu=list(map(lambda x: x[0],list(mails)))
           
            if q[0]== str(request.user) :  
               
                serial=IssueSerializer(p,request.data,partial=True)
                if p:
                    if serial.is_valid():
                        serial.save()
                        msg="Status Updated to "+request.data['status']

                        
                        send_email(mailu,pro,id,message=msg)
                    
                        return JsonResponse({'Message':"Updated"})
                    else:
                        return JsonResponse({'Message':serial.error_messages})
                else:
                  return JsonResponse({'Message':"Doesnot exist"})
            else:
                return JsonResponse({'Message':" Not allowed"},status=403)
    
   

class SearchIssue(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated]

    def get(slef,request,key=None):
        if key:
            d=Issue.objects.filter(Q(title__icontains=key) | Q(description__contains=key)).all()
            if len(d)>0:
                    
                serail=IssueSerializer(d,many=True)
                return JsonResponse({'data':serail.data})
            else:
                return JsonResponse({'Message':"Not exist"})

        else:
            return JsonResponse({'Message':"enter key"})

class WatcherCurd(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated]

    def patch(self,request,pro,id):
        watcher = request.query_params.get('watcher')

        if (Issue.objects.filter(pk=id).exists() and Project.objects.filter(pk=pro).exists()):
            try:
                issue = Issue.objects.get(pk=id,project=pro)
                try:
                    issue.watchers.add(watcher)
                    issue.save()
                    return JsonResponse({'data':"Watcher Added"})
                except:
                
                    return JsonResponse({'data':"User doesnt exist and valid user"})
            except:
                 return JsonResponse({'data':"Issue And Project doesnt match"})
    
        else:
           return JsonResponse({'data':'Enter Valid project and '})

    def delete(self,request,pro,id):
        watcher = request.query_params.get('watcher')

        if (Issue.objects.filter(pk=id).exists() and Project.objects.filter(pk=pro).exists()):
            try:
                issue = Issue.objects.get(pk=id,project=pro)
                isl=issue.watchers.values_list()
                a=list(map(lambda x: x[0],list(isl)))
                print(a)
                try:
                    if watcher in a:
                        issue.watchers.remove(watcher)
                        issue.save()
                        return JsonResponse({'data':"Watcher Deleted"})
                    else:
                        return JsonResponse({'data':"Watcher was not present in this issue"})
                except:
                    return JsonResponse({'data':"User doesnt exist"})
            except:
                 return JsonResponse({'data':"Issue And Project doesnt match"})
    
        else:
           return JsonResponse({'data':'Enter Valid project and '})

class CommentView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request,id=None):
        try:
            d=CommentIssue.objects.filter(issue=id)
            serial=CommentSerializer(d,many=True)
            return JsonResponse({'da':serial.data})
        except:
            return JsonResponse({'d':'s'})

    def post(self,request,id=None):
        if id==None:
            return JsonResponse({'data':'enter'})
        
        datai=request.data
        datai['issue']=id
        datai['user']=request.user

        serial=CommentSerializer(data=request.data)
        

        if serial.is_valid():
             
             serial.save()
             return JsonResponse({'data':'comment added'})
        return JsonResponse({'data':serial.errors})
    
    def patch(self,request,id=None):
        try:
            com=CommentIssue.objects.filter(pk=id).get()
            
            if com.user== request.user:
                data=request.data

                serial=CommentSerializer(com,data=data,partial=True)

                if serial.is_valid():
                    serial.save()
                    return JsonResponse({'data':'comment added'})
                return JsonResponse({'data':serial.errors})
            else:
                return JsonResponse({'data':'user not allowed'})
        except :
            return JsonResponse({'data':'comment doesnr exit'})
    
    def delete(self,request,id=None):
        try:
            com=CommentIssue.objects.filter(pk=id).get()
            
            if com.user== request.user:
                CommentIssue.objects.filter(pk=id).delete()
                return JsonResponse({'data':'Deleted'})
  
            else:
                return JsonResponse({'data':'user not allowed'})
        except :
            return JsonResponse({'data':'comment doesnr exit'})

class LabelView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated]

    def patch(self,request,id):
        label = request.data['label']
       
        if Issue.objects.filter(pk=id).exists():
            issue = Issue.objects.get(pk=id)
            try:
                issue.labels.add(label)
                issue.save()
                return JsonResponse({'data':"Lable Added"})
            except:
                serial= LableSerializer(data=request.data)
                if serial.is_valid():
                    serial.save()
                    issue.labels.add(label)
               
                return JsonResponse({'data':"Lable created and Added"})
        else:
            return JsonResponse({'data':"issue Doesnt Exist"})

    def delete(self,request,id):
        label = request.query_params.get('label')
       
        if Issue.objects.filter(pk=id).exists():
            issue = Issue.objects.get(pk=id)
            isl=issue.labels.values_list()
            a=list(map(lambda x: x[0],list(isl)))
            print(a)
            try: 
                if label in a:
                    issue.labels.remove(label)
                    return JsonResponse({'data':"Lable deleted"})
                else:
                    return JsonResponse({'data':"Lable doesnt exist"})
            except Exception as e:
                return JsonResponse({'data':e})
        else:
            return JsonResponse({'data':"issue Doesnt Exist"})


class FilterView(generics.ListAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'assigned','type','status','watchers','sprint','labels']
    pagination_class = custompaginate


class SprintCreate(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated,IsManager]


    def post(self,request,pro=None):
        try:
            if (Project.objects.filter(pk=pro).exists()):
                datai=request.data
                datai['project']=pro

                serial=SprintSerializer(data=datai)

                if serial.is_valid():
                    serial.save()
                    return JsonResponse({'data':"Sprint Created"})
                else:
                    return JsonResponse({'data':serial.errors})
            else:
                return JsonResponse({'data':"Project Doesnt exist"})

        except Exception as e:
            return JsonResponse({'data':e})
    
class SprintStartStop(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes=[IsAuthenticated,IsManager]

    def patch(self,request,id=None):
        try:
            if (Sprint.objects.filter(pk=id).exists()):
                sprint = Sprint.objects.get(pk=id)
                if sprint.sprint_status == None:
                        sprint.sprint_status = True
                        sprint.start_date = datetime.date.today()
                        sprint.save()
                        return JsonResponse({'data':"Sprint Started"})
                elif sprint.sprint_status == True:
                        sprint.sprint_status = False
                        sprint.end_date = datetime.date.today()
                        response = "Sprint stoped"
                        sprint.save()
                        return JsonResponse({'data':"Sprint Stopped"})
                else:
                    return JsonResponse({'data':"Sprint Cant be stopped/Started"})

            else:
                return JsonResponse({'data':"Sprint Doesnt exist"})

        except Exception as e:
            return JsonResponse({'data':e})
    
    def delete(self,request,id=None):
        try:
            if (Sprint.objects.filter(pk=id).exists()):
                Sprint.objects.get(pk=id).delete()
                return JsonResponse({'data':"Sprint Delete"})
            else:
                return JsonResponse({'data':"Sprint Doesnt exist"})

        except Exception as e:
            return JsonResponse({'data':e})

class SprintAddIssue(APIView):

    def patch(self,request,sp):
        isu=request.query_params.get('issue')
        try:
            if (Sprint.objects.filter(pk=sp).exists()):

                if(Issue.objects.filter(pk=isu).exists()):
                    issuep=Issue.objects.get(pk=isu)
                    sprintp=Sprint.objects.get(pk=sp)
                    if issuep.project_id==sprintp.project_id:
                         issuep.sprint_id=sp    
                         issuep.save()
                         return JsonResponse({'data':"Sprint Added to issue"})
                    else:
                         return JsonResponse({'data':"Sprint Not allowed to add to  issue"})

                else:
                    return JsonResponse({'data':"Enter Valid Issue ID"})
            else:
                return JsonResponse({'data':"Enter Valid sprint"})
        except Exception as e:
            return JsonResponse({'data':e})
    
    def delete(self,request,sp):
        isu=request.query_params.get('issue')
        try:
            if (Sprint.objects.filter(pk=sp).exists()):

                if(Issue.objects.filter(pk=isu).exists()):
                    issuep=Issue.objects.get(pk=isu)
                    if issuep.sprint_id!=None:
                        sprintp=Sprint.objects.get(pk=sp)
                        if issuep.project_id==sprintp.project_id:
                            issuep.sprint_id=None  
                            issuep.save()
                            return JsonResponse({'data':"Sprint Deleted to issue"})
                        else:
                            return JsonResponse({'data':"Sprint Not allowed to delete   issue"})
                    else:
                        return JsonResponse({'data':"No sprint present "})

                else:
                    return JsonResponse({'data':"Enter Valid Issue ID"})
            else:
                return JsonResponse({'data':"Enter Valid sprint"})
        except Exception as e:
            return JsonResponse({'data':e})