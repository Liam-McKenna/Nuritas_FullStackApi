from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.response import Response

from peptides.api.serializers import UserSerializer, PeptideSerializer, AssaySerializer
from peptides.models import Peptide, Assay


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None


class PeptideViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows peptides to be viewed.
    """
    queryset = Peptide.objects.all()
    serializer_class = PeptideSerializer
    pagination_class = None


class AssayViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows assays to be viewed or edited.
    """
    queryset = Assay.objects.all()
    serializer_class = AssaySerializer
    pagination_class = None

    @staticmethod
    def parse_data(data):
        peptides = data.get("peptides", [])
        del data["peptides"]

        return {
            "data": data,
            "peptides": peptides,
        }

    def create(self, request, *args, **kwargs):
        parsed_data = self.parse_data(request.data)

        serializer = AssaySerializer(data=parsed_data["data"])
        serializer.is_valid(raise_exception=True)
        assay = serializer.save()

        # Excercise 2 ADD-CODE-HERE
        for sequence in parsed_data['peptides']:
            pass

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
