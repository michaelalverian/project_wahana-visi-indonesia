from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from wvi.models import *


class KaderView():
    def view(request):
        if request.user.is_authenticated:
            template_name = "kader.html"
            context = {
                "kaders" : Kader.objects.all()
            }
            return render(request, template_name, context)
        else:
            return redirect('login')
    
    def insert(request):
        if request.method == "POST":
            name = request.POST['name']
            number = request.POST['number']
            kelurahan = request.POST['kelurahan']

            kader=  Kader(name=name, phone_number=number, kelurahan=kelurahan)
            kader.save()
            return HttpResponseRedirect(reverse("kader"))
        else:
            return KaderView.view(request)
    
    def update(request):
        if request.method == "POST":
            id = request.POST['kader_id']
            name = request.POST['name']
            number = request.POST['number']
            kelurahan = request.POST['kelurahan']

            kader = Kader.objects.get(pk=id)
            kader.name = name
            kader.phone_number = number
            kader.kelurahan = kelurahan
            kader.save()
            return HttpResponseRedirect(reverse("kader"))
        else:
            return KaderView.view(request)

    def delete(request):
        if request.method == "POST":
            id = request.POST['kader_id']
           
            Kader.objects.get(pk=id).delete()
            return HttpResponseRedirect(reverse("kader"))
        else:
            return KaderView.view(request)