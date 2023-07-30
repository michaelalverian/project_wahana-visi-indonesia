from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from wvi.models import *


class ChildView():
    def view(request):
        if request.user.is_authenticated:
            template_name = "child.html"
            context = {
                "childs": Child.objects.all()
            }
            return render(request, template_name, context)
        else:
            return redirect('login')
    
    def update(request):
        if request.method == "POST":
            id = request.POST['child_id']
            rt = request.POST['rt']
            child = Child.objects.get(pk=id)
            child.rt = rt
            child.save()
            return HttpResponseRedirect(reverse("child"))
        else:
            return ChildView.view(request)