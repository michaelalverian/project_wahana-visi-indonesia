from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

from wvi.models import *

import datetime
import pandas as pd
import os


class CorrespondenceView():
    def view(request):
        if request.user.is_authenticated:
            template_name = "correspondence.html"
            for correspondence in Correspondence.objects.all():
                correspondence.days_before_due_date_field = (correspondence.due_date_field - datetime.datetime.now().date() ).days
                correspondence.days_before_due_date_system= (correspondence.due_date_system - datetime.datetime.now().date() ).days
                correspondence.save()
            context = {
                "correspondences" : Correspondence.objects.all(),
                "kaders" : Kader.objects.all(),
                "param" : Parameters.objects.get(pk=1).deadline_due_date_field
            }
            return render(request, template_name, context)
        else:
            return redirect('login')
    
    def insert_excel(request):
        if request.method == "POST": 
            template_name = "correspondence.html"
            context = {
            "error" : "",
            "correspondences" : Correspondence.objects.all(),
            "kaders" : Kader.objects.all(),
            "param" : Parameters.objects.get(pk=1).deadline_due_date_field
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
                    'Child ID', 'Child Name', 'Community',
                    'Correspondence Type', 'Creation Date',
                    'Mail Action and Route', 'Due Date Field',
                    'Due Date System', 'Days Before Due Date field',
                    'Days Before Due Date System', 'Status'
                ]

                for column in important_column:
                    if(not column in column_list):
                        context['error'] += column +" not found !\n"

                if(context['error'] == ''):
                    Correspondence.objects.all().delete()
                    for i in range(len(datas)):
                        id = datas.loc[i,'Child ID']
                        name = datas.loc[i, 'Child Name']
                        community = datas.loc[i, 'Community']
                        type = datas.loc[i, 'Correspondence Type']
                        creation_date = datetime.datetime.strptime(datas.loc[i, 'Creation Date'], '%d-%b-%Y')
                        mail_action = datas.loc[i, 'Mail Action and Route']
                        due_date_field =  creation_date + datetime.timedelta(days=Parameters.objects.get(pk=1).deadline_due_date_field)
                        due_date_system = datetime.datetime.strptime(datas.loc[i, 'Due Date System'], '%d-%b-%Y')
                        days_before_due_date_field = (due_date_field - datetime.datetime.now() ).days
                        days_before_due_date_system = (due_date_system - datetime.datetime.now()).days
                        status = datas.loc[i, 'Status']

                        if(Child.objects.filter(pk=id).exists()):
                            child = Child.objects.get(pk=id)
                            child.name = name
                            child.community = community
                            child.save()
                        else:
                            child = Child(id=id, name=name, community=community)
                            child.save() 
                        correspondence = Correspondence(child_id = child, type = type, creation_date=creation_date, mail_action=mail_action, due_date_field=due_date_field, due_date_system=due_date_system, days_before_due_date_field=days_before_due_date_field, days_before_due_date_system=days_before_due_date_system, status=status)
                        correspondence.save()

            if(context['error'] == ''):
                return HttpResponseRedirect(reverse("correspondence"))
            else:
                return render(request, template_name, context)
        else:
            return CorrespondenceView.view(request)

    def update_kader(request):
        if request.method == "POST":
            id = request.POST['correspondence_id']
            kader_id = request.POST['kader_id']
            corr = Correspondence.objects.get(pk=id) 
            if(kader_id != 'NULL'):
                kader = Kader.objects.get(pk=kader_id)
                corr.kader_id = kader
            else:
                corr.kader_id = None
            corr.save()
            return HttpResponseRedirect(reverse("correspondence"))
        else:
            return CorrespondenceView.view(request)

    def update_due_date(request):
        if request.method == "POST": 
            template_name = "correspondence.html"
            due_date = request.POST['due_date']

            param = Parameters.objects.get(pk=1)
            param.deadline_due_date_field = due_date
            param.save()

            for correspondence in Correspondence.objects.all():
                correspondence.due_date_field = correspondence.creation_date +  datetime.timedelta(days=Parameters.objects.get(pk=1).deadline_due_date_field)
                correspondence.save()
            return HttpResponseRedirect(reverse("correspondence"))
        else:
            return CorrespondenceView.view(request)