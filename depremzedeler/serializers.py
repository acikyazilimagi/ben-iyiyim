from rest_framework import serializers

from .models import Depremzede


class DepremzedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depremzede
        fields = "__all__"
