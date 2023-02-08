from html import escape

from django.shortcuts import redirect, render
from django.views import View
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import Depremzede
from .serializers import DepremzedeSerializer


class DepremzedeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = Depremzede.objects.all()
    serializer_class = DepremzedeSerializer


class DepremzedeSearch(View):
    def get(self, request, *args, **kwargs):
        return render(request, "search.html")

    def post(self, request, *args, **kwargs):
        isim = escape(request.GET.get("isim"))
        il = escape(request.GET.get("il"))
        telefon = escape(request.GET.get("telefon"))
        if il:
            if len(isim) > 5 and not len(telefon) > 10:
                rlist = Depremzede.objects.filter(isim__icontains=isim, il=il)
                render(request, "search.html", {"rlist": rlist})
            elif len(telefon) > 10 and not len(isim) > 5:
                rlist = Depremzede.objects.filter(telefon__icontains=telefon, il=il)
                render(request, "search.html", {"rlist": rlist})
            elif len(isim) > 5 and len(telefon) > 10:
                rlist = Depremzede.objects.filter(
                    isim__icontains=isim, telefon__icontains=telefon, il=il
                )
                render(request, "search.html", {"rlist": rlist})
            else:
                context = {
                    "error": "Sorgu yapılabilmesi için en az 5 karakterli bir isim veya telefon numarası girmelisiniz."
                }
                return redirect("DepremzedeSearch", context)


class DepremzedeAdd(View):
    def get(self, request, *args, **kwargs):
        return render(request, "add.html")

    def post(self, request, *args, **kwargs):
        isim = request.POST.get("isim")
        il = request.POST.get("il")
        adres = request.POST.get("adres")
        tarif = request.POST.get("tarif")
        telefon = request.POST.get("telefon")
        cikarildi = request.POST.get("cikarildi")
        durum = request.POST.get("durum")

        depremzede = Depremzede(
            isim=isim,
            il=il,
            adres=adres,
            tarif=tarif,
            telefon=telefon,
            cikarildi=cikarildi,
            durum=durum,
        )
        depremzede.save()
        return redirect("/add/")
