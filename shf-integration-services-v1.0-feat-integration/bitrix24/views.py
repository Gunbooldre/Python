
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from allur import schemas
from allur import serializers
from allur.models import Lead
from allur.services import start_integration_process, get_lead_status_from_bs




class BitrixViewSet(GenericViewSet):
    authentication_classes = ()
    permission_classes = ()

    @action(methods=["POST"], detail=False)
    def application_create(self, request, *args, **kwargs):
        lead_name = "bitrix"
        lead_object = Lead.objects.create(request_from_partner=dict(request.data), lead_name=lead_name)# just for log any request without validation
        serializer = serializers.LeadInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        information_from_partner = schemas.LeadInputSchema(**request.data)

        lead_id, client_id, app_id, current_status, collateral_id = start_integration_process(
             lead_object=lead_object,
               handled_data=information_from_partner
               )
    
        return Response({"leadID": lead_id,"applicationId":app_id,"clientId":client_id,
                         
                                                "status":current_status,
                                                "car price":information_from_partner.car.price,
                                                "durations":information_from_partner.duration,
                                                "insurance":information_from_partner.insurance,
                                                "downpayment":information_from_partner.downpayment}, status=status.HTTP_200_OK)
    

    @action(methods=["get"], detail=False, url_path="app-status/(?P<id>\d+)")
    def get_application_status(self, request, id=None):
        lead_id = int(id)
        lead_exist = Lead.objects.filter(lead_id_on_bs=lead_id).exists()
        if lead_exist:
            current_status = get_lead_status_from_bs(lead_id=lead_id)
            match current_status:
                    case 'CHECK':
                        result = 'На проверке'
                    case _:
                        result = "Неизвестно"
            return Response({"status": result})
        return Response("lead с таким id не существует")
        
