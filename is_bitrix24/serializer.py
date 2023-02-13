from rest_framework import serializers

from .models import IsBitrix

class CreateLeadSerializer(serializers.ModelSerializer):
    lead= serializers.CharField(read_only = True)
    applicationId = serializers.CharField(read_only = True)
    clientId = serializers.CharField(read_only = True)
    class Meta:
        model = IsBitrix
        fields = "__all__"