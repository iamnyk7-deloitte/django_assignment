
from cProfile import label
from functools import partial
from re import L
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core import serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager
from api.serializers.managerserializer import IssueSerializer,ProjectSerializer,IssueAssign,IssueStatus,CommentSerializer

from dropship.models import CommentIssue, Issue, Label,Project, User
from rest_framework import viewsets
from django.db.models import Q
from django.core import mail
from django.core.mail import EmailMessage,send_mass_mail,send_mail
import asyncio
from time import sleep

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
            print()

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

    def patch(self,request,pro=None,id=None):
        if pro== None or id==None:
            return JsonResponse({'data':"no"})
        else:  
            m=Issue.objects.filter(project=pro,pk=id).get()
           
            serial=IssueSerializer(m,request.data,partial=True)
            if serial.is_valid():
               serial.save()
               return JsonResponse({'data':"Updated"})
            return JsonResponse({'data':serial.errors})

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

# class LabelView(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes=[IsAuthenticated]

#     def get(self,request,id=None,labl=None):
#         try:
#           b=Label.objects.create(label="oje")
#           isu=Issue.objects.filter(pk=12).get()

#           isu.lables.add(b)
#           return JsonResponse({'data':"yes"})
       
          
#         except:

#          return JsonResponse({'data':"no"})
        