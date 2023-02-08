from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.contrib import messages
from html import escape
import json
import re

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Person
from .serializers import PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Person.objects.all().order_by('created_at')
    serializer_class = PersonSerializer


def telKontrol(input):
    if re.match("^[0-9]+$", input) and len(input) > 9:
        return True
    else:
        return False

def textKontrol(input):
    if len(input) > 2:
        return True
    else:
        return False

# Create your views here.
def index(request):
    return render(request, 'deprem.html')

def report(request):
    if request.method == 'POST':
        isim = escape(request.POST["isim"])
        sehir = escape(request.POST["sehir"])
        adres = escape(request.POST["adres"])
        durum = escape(request.POST["durum"])
        if "tel" in request.POST:
            tel = request.POST["tel"]
            if telKontrol(tel):
                tel = tel
            else:
                tel = "Yok"
        if textKontrol(isim) and textKontrol(sehir) and textKontrol(adres) and textKontrol(durum):
            p = Person(isim=isim, sehir=sehir, adres=adres, tel=tel, durum=durum)
            p.save()
            messages.success(request, 'Kaydedildi.')
            return HttpResponse("Kaydedildi.")
        else:
            return HttpResponseBadRequest("Giriş yapılan bilgilerde desteklenmeyen karakterler var.")
    return redirect('index')

def search(request):
    if request.method == "GET":
        if 'isim' in request.GET and "tel" in request.GET:
            isim = escape(request.GET.get('isim'))
            tel = escape(request.GET.get('tel'))
            if len(isim) > 2 and telKontrol(tel):
                reports = Person.objects.filter(isim__icontains=isim, tel__contains=tel)
            else:
                return HttpResponseBadRequest("Input hatalı.")
        else:
            if 'isim' in request.GET:
                isim = escape(request.GET.get('isim'))
                print(len(isim))
                if len(isim) > 2:
                    reports = Person.objects.filter(isim__icontains=isim).order_by('created_at')[:10]
                else:
                    return HttpResponseBadRequest('İsim 2 karakterden uzun olmalı.')
            elif 'tel' in request.GET:
                tel = escape(request.GET.get('tel'))
                if telKontrol(tel):
                    reports = Person.objects.filter(tel__contains=tel).order_by('created_at')[:10]
                else:
                    return HttpResponseBadRequest("Telefon numarası bilgileri hatalı.")
            else:
                return HttpResponse("Arama yapmak için veri girişi yapın.")
        rlist = serialize('json', reports, fields=["isim", "sehir", "adres", "durum", "created_at"], use_natural_primary_keys=True)
        robject = json.loads(rlist)
        for d in robject:
            del d['pk']
            del d['model']
        rlist = json.dumps(robject)
        return HttpResponse(rlist, content_type="application/json")
