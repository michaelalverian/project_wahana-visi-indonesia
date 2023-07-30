from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

from wvi.models import *

import pandas as pd
import os


class ParticipantView():
    def view(request):
        if request.user.is_authenticated:
            template_name = "participant.html"
            context = {
                "participants" : Participation.objects.all()
            }
            return render(request, template_name, context)
        else:
            return redirect('login')
    
    def insert_excel(request):
        if request.method == "POST":
            template_name = "participant.html"
            context = {
                "error" : "",
                "participants" : Participation.objects.all()
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
                    'Id', 'CommunityName',
                    'SdChildId', 'ChildName',
                    'Gender', 'AGE', 'ChildParticipation',
                    'FamilyParticipation', 'ChildSupport',
                    'FamilySupport', 'BenefitSupport'
                ]
                
                for column in important_column:
                    if(not column in column_list):
                        context['error'] += column +" not found !\n"

                if(context['error'] == ''):
                    Participation.objects.all().delete()
                    for i in range(len(datas)):
                        id = datas.loc[i,'SdChildId']
                        name = datas.loc[i, 'ChildName']
                        gender = datas.loc[i,'Gender']
                        community = datas.loc[i, 'CommunityName']
                        age = datas.loc[i, 'AGE']
                        child_participation = datas.loc[i, 'ChildParticipation']
                        family_participation = datas.loc[i, 'FamilyParticipation']
                        child_support = datas.loc[i, 'ChildSupport']
                        family_support = datas.loc[i, 'FamilySupport']
                        benefit_support = datas.loc[i, 'BenefitSupport']
                        total = child_participation + family_participation + child_support + family_support + benefit_support

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
                        participation = Participation(child_id = child, child_participation = child_participation, family_participation = family_participation, child_support = child_support, family_support = family_support, benefit_support = benefit_support, total=total)
                        participation.save()

            if(context['error'] == ''):
                return HttpResponseRedirect(reverse("participant"))
            else:
                return render(request, template_name, context)
        else:
            return ParticipantView.view(request)