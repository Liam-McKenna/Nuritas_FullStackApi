from django.contrib.auth.models import User
from rest_framework import serializers

from peptides.models import Peptide, Assay

class UserSerializer(serializers.ModelSerializer):
    groups_list = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'groups_list']

    def get_groups_list(self, user):
        return [g.name for g in user.groups.all()]

    def get_full_name(self, user):
        return user.get_full_name()


class PeptideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Peptide
        fields = "__all__"


class AssaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Assay
        fields = "__all__"
