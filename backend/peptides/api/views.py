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

     # get all current peps
        existingPepsData = Peptide.objects.all()
        newAssayPeps = []
        # for each new sequence in post
        for sequence in parsed_data['peptides']:
            # for each exiting pep, check if it exists
            for existingPep in existingPepsData:
                if existingPep.sequence == sequence:
                    existingPepId = existingPep.id
                    break  # take existing pep's id and add it to Assay list.
                else:
                    existingPepId = False
            if(existingPepId):
                newAssayPeps.append(existingPepId)
            else:
                # If existing is false: create a new pep item with the new sequence, and add the new id to the Assay list.
                latestPepData = (existingPepsData.latest('id'))
                latestPepNumber = (int(latestPepData.name.split("_", 1)[1]))
                newPepNumber = ("pep_"+str(latestPepNumber+1))
                newPepData = {'sequence': sequence, 'name': newPepNumber}
                # create new pep item, then take the new id and add it to newAssayPeps
                #################################################
                pepSerializer = PeptideSerializer(data=newPepData)
                pepSerializer.is_valid(raise_exception=True)
                pep = pepSerializer.save()
                headers = self.get_success_headers(pepSerializer.data)
                NewPep = Response(
                    pepSerializer.data, status=status.HTTP_201_CREATED, headers=headers)
                newAssayPeps.append(NewPep.data['id'])
                ##################################################
        # add Assay's to data
        serializer.save(peptides=newAssayPeps)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
