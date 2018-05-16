from sdp.models.configTenda import ConfigTenda
from rest_framework import viewsets
from sdp.serializers.configTenda import ConfigTendaSerializer

class ConfigTendaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ConfigTenda.objects.all().order_by('-id')
    serializer_class = ConfigTendaSerializer