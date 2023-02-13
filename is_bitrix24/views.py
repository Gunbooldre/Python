# Created by Muratbayev Dias
# 09.11.22
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from .serializer import CreateLeadSerializer
from .models import IsBitrix
from config.settings import USER_LOGIN, USER_PASSWORD, CUSTOMER_KEY


import requests
import datetime
import json


def mainPage(request):
    return render(request, 'is_bitrix/index.html')


class CreateLeadViewSet(APIView):
    #Класс создан для создания нового Lead ID для парнтнеров

    def __init__(self):
        # ================================================================= Test version === start
        self.url = 'https://shinhantest-saas.brainysoft.ru/bs-core/main/'
        self.urlAuth = 'https://shinhantest-saas.brainysoft.ru/bs-core/main/login'
        bodyResp = {"userName": USER_LOGIN,
                    "password": USER_PASSWORD}
        headerAuth = {'Content-Type': 'application/json;',
                      'customer-key': CUSTOMER_KEY}
        authReq = requests.post(self.urlAuth, data=json.dumps(
            bodyResp), headers=headerAuth)
        # ================================================================= Test version === end
        # ================================================================= Prodution version === start
        #Ниже находятся  параментры для переключения на бой
        # self.url  = 'https://bs.shinhanfinance.kz/bs-core/main/'
        # urlAuth      = f'https://bs.shinhanfinance.kz/bs-core/main/login/user/{USER_LOGIN}/password/{USER_PASSWORD}?customer-key={CUSTOMER_KEY}'
        # authReq = requests.get(urlAuth)
        # ================================================================= Prodution version === end
        self.headers = {'Content-Type': 'application/json;',
                        'bsauth': authReq.headers['bsauth']}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def post(self, request):
        serializer = CreateLeadSerializer(data=request.data)
        data = dict(request.data)
        gender = data['user_info']['sexId']
        price = data['deal_info']['loanAmount']
        duration = data['deal_info']['creditFieldReq.trancheCount']
        maritalStatus = data['user_info']['maritalStatusId']
        match gender:
            case 'Мужчина':
                gender = '101251'
            case 'Женщина':
                gender = '101252'
        resp = {
            "channel": "GENERATOR",
            "subdivisionId": 101791,
            'lastName': data['user_info']['lastName'],
            'firstName': data['user_info']['firstName'],
            'patronymic': data['user_info']['patronymic'],
            "inn": data['user_info']['iin'],
            "birthDate": data['user_info']['birthDate'],
            "sexId": gender,
            "birthCountryId": 101041,
            "amount": price,
            "period":duration,
            "birthPlace": data['user_info']['birthPlace'],
            "passport": {
                'no': data['user_info']['passport.no'],
                'issueDate': data['user_info']['passport.issueDate'],
                'closeDate': data['user_info']['passport.closeDate'],
                "seria": "0001"
            },
            "registrationAddressData": {
                "regionName": '',
                "housingType": '',
                "localityName": "",
                "streetName": '',
                "houseNo": '',
                "apartmentNo": "",
                "buildingNo": "",
                "telephone": '',
                "additionalPhone": '',
                "countryId": 101041
            },
            "addressData": {
                "regionName": data['user_info']['addressData.oldAddressText'],
                "housingType": "",
                "localityName": "",
                "streetName": "",
                "houseNo": "",
                "apartmentNo": "",
                "buildingNo": "",
                "telephone": "",
                "additionalPhone": "",
                "countryId": 101041,
                "managerId": 1010861
            },
            "mobilePhone": data['user_info']['workPlaceData.workPhone'],
            "email": "-",
            "creditProductId": 101339,  # 101339 - test 10133793 - prod
            "extraFields": [
                {
                    "key": "client.rnn",
                    "value": data['user_info']['iin']
                },
                {
                    "key": "client.education.id",
                    "value": "1011010"
                },
                {
                    "key": "client.Resident",
                    "value": data['user_info']['extraField_Resident']
                },
                {
                    "key": "client.DocIssueMan",
                    "value": data['user_info']['extraField_DocIssueMan']
                },
                {
                    "key": "client.maritalStatus.id",
                    "value": maritalStatus
                },
                {
                    "key": "client.workPlaceData.workPlace",
                    "value": data['user_info']["personRelatives.0.workPlace"] 
                },
                {
                    "key": "client.businessAddressData.country.id",
                    "value": "101041"
                },
                {
                    "key": "client.businessAddressData.country.id",
                    "value": "101041"
                },
                {
                    "key": "client.businessAddressData.regionName",
                    "value": "г.Алматы"
                },
                {
                    "key": "client.businessAddressData.streetName",
                    "value": "-"
                },
                {
                    "key": "client.businessAddressData.houseNo",
                    "value": "-"
                },
                {
                    "key": "client.businessAddressData.apartmentNo",
                    "value": ""
                },
                {
                    "key": "client.workPlaceData.workPosition",
                    "value": data['user_info']["workPlaceData.workPosition"] 
                },
                {
                    "key": "client.workPlaceData.website",
                    "value": data['user_info']["workPlaceData.website"] 
                },
                {
                    "key": "client.workPlaceData.workAge",
                    "value":data['user_info']["workPlaceData.workAge"] 
                },
                {
                    "key": "client.monthlyIncome2NDFL",
                    "value": data['user_info']["monthlyIncome2NDFL"] 
                },
                {
                    "key": "client.meanIncome",
                    "value": data['user_info']["meanIncome"] 
                },
                {
                    "key": "loanApplication.currency.id",
                    "value": "101011"
                },
                {
                    "key": "loanApplication.creditPurpose.id",
                    "value": "101683"
                }
            ]
        }

        if serializer.is_valid():
            try:
                url = self.url + 'leads'
                data1 = json.dumps(resp)
                firstPost = self.session.post(url, data=data1)
                firstRes = firstPost.json()
                if firstRes['status'] == 'ok':
                    dataLead = firstRes["data"]
                    url = self.url+f'leads/{dataLead}/check'
                    secPost = self.session.post(url)
                    firstGet = self.session.get(self.url+f'leads/{dataLead}')
                    firstGetRes = firstGet.json()
                    if firstGetRes['status'] == 'ok':
                        secondRes = firstGet.json()
                        dataApp = secondRes['data']['loanApplicationId']
                        dataClient = secondRes['data']['clientId']
                        serializer.save(lead=dataLead, applicationId=dataApp,
                                            clientId=dataClient, jsonRequest=dict((request.data)))
                        return Response({"leadID": dataLead,"applicationId":dataApp,"clientId":dataClient,
                                             "status":secondRes['data']['currentStatus'],
                                             "car price":price,
                                             "durations":duration}, status=status.HTTP_200_OK)
                    else:
                        return Response("Приложение не создано", status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"lead не создался"}, status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({"Ошибка в отправке запроса, неверные данные"}, status.HTTP_204_NO_CONTENT)
        else:
            #print(firstPost.text)
            return Response({"Ошибка в отправке запроса, не поддерживается формат запроса"}, status.HTTP_204_NO_CONTENT)


class GetStatusViewSet(APIView):
    # Класс создан для запроса  Lead ID для парнтнеров
    def __init__(self):
        # ================================================================= Test version === start
        self.url = 'https://shinhantest-saas.brainysoft.ru/bs-core/main/'
        self.urlAuth = 'https://shinhantest-saas.brainysoft.ru/bs-core/main/login'
        bodyResp = {"userName": USER_LOGIN,
                    "password": USER_PASSWORD}
        headerAuth = {'Content-Type': 'application/json;',
                      'customer-key': CUSTOMER_KEY}
        authReq = requests.post(self.urlAuth, data=json.dumps(
            bodyResp), headers=headerAuth)
        # ================================================================= Test version === end
        
        # ================================================================= Prodution version === start
        # self.url  = 'https://bs.shinhanfinance.kz/bs-core/main/'
        # urlAuth      = f'https://bs.shinhanfinance.kz/bs-core/main/login/user/{USER_LOGIN}/password/{USER_PASSWORD}?customer-key={CUSTOMER_KEY}'
        # authReq = requests.get(urlAuth)
        # ================================================================= Prodution version === end
        
        self.headers = {'Content-Type': 'application/json;',
                        'bsauth': authReq.headers['bsauth']}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get(self, request, *args, **kwargs):
        try:
            leadId = self.kwargs['leadId']
            id = IsBitrix.objects.get(lead = leadId)
            if id:
                url = self.url + f'leads/{leadId}'
                firstGet = self.session.get(url)
                firstRes = firstGet.json()
                match firstRes['data']['currentStatus']:
                    case 'CHECK':
                        firstRes = 'Проверка'
                return Response({"status": firstRes}, status=status.HTTP_200_OK)
        except:
            return Response({"Такого leadId не существует":leadId}, status.HTTP_204_NO_CONTENT)


def sendDocs(cliCode, photoBack, photoFront, photo):
    import base64
    photoBack = base64.b64decode((photoBack))
    photoFront = base64.b64decode((photoFront))
    photo = base64.b64decode((photo))
    arr = [photoBack, photoFront]
    
    # ================================================================= Test version === start
    urlAuth = 'https://shinhantest-saas.brainysoft.ru/bs-core/main/login'
    bodyResp = {"userName": USER_LOGIN, "password": USER_PASSWORD}
    headerAuth = {'Content-Type': 'application/json;', 'customer-key': CUSTOMER_KEY}
    authReq = requests.post(urlAuth, data=json.dumps(bodyResp), headers=headerAuth)
    url = f'https://shinhantest-api-stage.brainysoft.ru/file-storage/files/{CUSTOMER_KEY}/add?client={cliCode}'
    # ================================================================= Test version === end

    # ================================================================= Prodution version === start
    # urlAuth =  f'https://bs.shinhanfinance.kz/bs-core/main/login/user/{USER_LOGIN}/password/{USER_PASSWORD}?customer-key={CUSTOMER_KEY}'
    # authReq = requests.get(urlAuth)
    # url = f"https://file.shinhanfinance.kz/files/shinhanfinance/add?client={cliCode}"
    # ================================================================= Prodution version === end
    
    # Ниже находится процесс по отправке файлов к определенному клиенту
    header = {'bsauth': authReq.headers['bsauth']}
    payload = {}
    for i in range(len(arr)):
        files = [('file', ('IDCARD.pdf', arr[i], 'application/pdf'),)]
        response = requests.request(
            "POST", url+'&tags=4', headers=header, data=payload, files=files)
    files = [('file', ('photo.jpeg', photo, 'image/jpeg'),)]
    response = requests.request(
        "POST", url+'&tags=1', headers=header, data=payload, files=files)
    return (response.status_code)
