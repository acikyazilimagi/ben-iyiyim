from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import Depremzede
from .serializers import DepremzedeSerializer


class DepremzedeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = Depremzede.objects.all()
    serializer_class = DepremzedeSerializer
