
#Models
from sdp.models.estrutura.componentes.componente import Componente
from sdp.models.estrutura.componentes.familiaComponentes import FamiliaComponentes
from sdp.models.tendas.configTenda import ConfigTenda
from sdp.models.estrutura.listaComponentes import ListaDeComponentes
from rest_framework import viewsets
from sdp.serializers.componentes.componentes import ComponentesSerializer
from SdpREST.helpers.HttpException import HttpException
from SdpREST.helpers.HttpResponseHandler import HTTP
from SdpREST.helpers.SchemaValidator import SchemaValidator


class ComponentesViewModel(viewsets.ModelViewSet):

    @staticmethod
    def list(self):
        try:
            queryset = Componente.objects.all()
            data = ComponentesSerializer(queryset, many=True).to_representation(queryset)
        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, 'Familia de Componentes' ,data)

    @staticmethod
    def create(request):
        try:
            data = request.data
            # 1. Check schema
            SchemaValidator.validate_obj_structure(data, 'componentes/componentes.json')

            # 2. Validate
            if(FamiliaComponentes.objects.familia_exist(data['familia']) == False):
                return HTTP.response(400, 'Wrong Family')

            familia = FamiliaComponentes.objects.get(pk=data['familia'])
            genCodigo = Componente.objects.count_familia(data['familia']) + 1

            genCodigo = str(familia.id) + '.' + str(genCodigo)

            novoComponente = Componente(
                nome=data['nome'] if 'nome' in data else None,
                descricao=data['descricao'] if 'descricao' in data else None,
                tag=data['tag'] if 'tag' in data else None,
                familia=familia,
                genCodigo=genCodigo
            )
            novoComponente.save()

            for tenda_id in data['tenda']:
                tipoTenda = ConfigTenda.objects.get(pk=tenda_id)
                ListaDeComponentes(
                    componente=novoComponente,
                    tenda=tipoTenda
                ).save()

        except HttpException as e:
            return HTTP.response(e.http_code, e.http_detail)
        except Exception as e:
            return HTTP.response(400, 'Some error occurred. {}. {}.'.format(type(e).__name__, str(e)))

        return HTTP.response(200, 'Novo Componente Registado')