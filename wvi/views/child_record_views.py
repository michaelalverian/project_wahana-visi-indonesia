from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

from wvi.models import *

import pandas as pd
import os


class ChildRecordView():
    def view(request):
        if request.user.is_authenticated:
            template_name = "child_record.html"
            context = {
                "child_records" : ChildRecord.objects.all(),
                "kaders" : Kader.objects.all(),
                "count_avail":  ChildRecord.objects.filter(status="1 - Available").count() ,
                "count_sponsored": ChildRecord.objects.filter(status="2 - Sponsored").count(),
                "count_hold": ChildRecord.objects.filter(status="3 - Hold").count(),
                "count_left":ChildRecord.objects.filter(status="4 - Left Program").count(),
                "param": Parameters.objects.get(pk=1).target_child
            }
            return render(request, template_name, context)
        else:
            return redirect('login')
    
    def insert_excel(request):
        if request.method == "POST":
            template_name = "child_record.html"
            context = {"error" : "",
                        "child_records" : ChildRecord.objects.all(),
                         "kaders" : Kader.objects.all(),
            "count_avail":  ChildRecord.objects.filter(status="1 - Available").count() ,
            "count_sponsored": ChildRecord.objects.filter(status="2 - Sponsored").count(),
            "count_hold": ChildRecord.objects.filter(status="3 - Hold").count(),
            "count_left":ChildRecord.objects.filter(status="4 - Left Program").count(),
            "param": Parameters.objects.get(pk=1).target_child
                        }
            file = request.FILES['file_excel']
            if(not('.xlsx' in file.name or '.csv' in file.name)):
                context ['error'] = "file type incorrect" 
            else:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                datas = pd.read_excel(filename)
                os.remove(filename)
                column_list = list(datas)

                important_column = [
                    'Child ID', 'Child Name', 'Gender',
                    'Project Number and Name', 'Community',
                    'RC Status', 'Age'
                ]
                
                for column in important_column:
                    if(not column in column_list):
                        context['error'] += column +" not found !\n"

                if(context['error'] == ''):
                    ChildRecord.objects.all().delete()
                    for i in range(len(datas)):
                        id = datas.loc[i,'Child ID']
                        name = datas.loc[i, 'Child Name']
                        gender = datas.loc[i,'Gender']
                        community = datas.loc[i, 'Community']
                        age = datas.loc[i, 'Age']
                        project_number = datas.loc[i,'Project Number and Name']
                        status = datas.loc[i, 'RC Status']

                        if(Child.objects.filter(pk=id).exists()):
                            child = Child.objects.get(pk=id)
                            child.name = name
                            child.gender = gender
                            child.community = community
                            child.age = age
                            child.save()
                        else:
                            child = Child(id=id, name=name, gender=gender, community=community, age=age)
                            child.save()
                        childrecord = ChildRecord(child_id = child, project_number = project_number, status=status)
                        childrecord.save()

            if(context['error'] == ''):
                return HttpResponseRedirect(reverse("childrecord"))
            else:
                return render(request, template_name, context)
        else:
            return ChildRecordView.view(request)

    def update(request):
        if request.method == "POST":
            id = request.POST['childrecord_id']
            kader_id = request.POST['kader_id']
            childrecord = ChildRecord.objects.get(pk=id) 
            if(kader_id != 'NULL'):
                kader = Kader.objects.get(pk=kader_id)
                childrecord.kader_id = kader
            else:
                childrecord.kader_id = None
            childrecord.save()
            return HttpResponseRedirect(reverse("childrecord"))
        else:
            return ChildRecordView.view(request) 
        
    def update_target(request):
        if request.method == "POST": 
            target = request.POST['target']

            param = Parameters.objects.get(pk=1)
            param.target_child = target
            param.save()

            return HttpResponseRedirect(reverse("childrecord"))
        else:
            return ChildRecordView.view(request)