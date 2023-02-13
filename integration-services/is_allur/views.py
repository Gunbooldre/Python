# Created by Muratbayev Dias
# 09.11.22
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from .serializer import CreateLeadSerializer
from .models import IsAllur
from config.settings import USER_LOGIN, USER_PASSWORD, CUSTOMER_KEY


import requests
import datetime
import json


def mainPage(request):
    return render(request, 'is_allur/index.html')


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
        lastname = data['customer']['lastname']
        firstname = data['customer']['firstname']
        gender = data['customer']['gender']
        patronymic = data['customer']['patronymic']
        iin = data['customer']['iin']
        birthDate = data['customer']['birthDate']
        birthPlace = data['customer']['birthPlace']
        number = data['customer']['document']['number']
        issuedDate = data['customer']['document']['issuedDate']
        expirationDate = data['customer']['document']['expirationDate']
        photoBack = data['customer']['document']['photoBack']
        photoFront = data['customer']['document']['photoFront']
        issuer = data['customer']['document']["issuer"]
        photo = data['customer']['photo']
        regionName = data['customer']['registrationAddress']['region']
        settlement = data['customer']['registrationAddress']['settlement']
        street = data['customer']['registrationAddress']['street']
        house = data['customer']['registrationAddress']['house']
        contactPersonPhone = data['customer']['contactPersonPhone']
        mobilePhone = data['customer']['mobilePhone']
        price = data['car']['price']
        duration = data['duration']
        officialIncome = data['customer']['officialIncome']
        residencyStatus = data['customer']['residencyStatus']
        maritalStatus = data['customer']['maritalStatus']

        match maritalStatus:
            case 'SINGLE':
                maritalStatus = '101151'
            case 'MARRIED':
                maritalStatus = '101152'

        match issuer:
            case 'MINISTRY_OF_THE_INTERIOR':
                issuer = 'МВД РК'
            case 'MINISTRY_OF_JUSTICE':
                issuer = 'МЮ РК'

        match residencyStatus:
            case 'NOT_RESIDENT':
                residencyStatus = 'Нерезидент'
            case 'RESIDENT':
                residencyStatus = 'Резидент'

        match gender:
            case 'MALE':
                gender = '101251'
            case 'FEMALE':
                gender = '101252'
        resp = {
            "channel": "GENERATOR",
            "subdivisionId": 101791,
            'lastName': lastname,
            'firstName': firstname,
            'patronymic': patronymic,
            "inn": iin,
            "birthDate": birthDate,
            "sexId": gender,
            "birthCountryId": 101041,
            "amount": price,
            "period": duration,
            "birthPlace": birthPlace,
            "passport": {
                'no': number,
                'issueDate': issuedDate,
                'closeDate': expirationDate,
                "seria": "0001"
            },
            "registrationAddressData": {
                "regionName": regionName,
                "housingType": settlement,
                "localityName": "",
                "streetName": street,
                "houseNo": house,
                "apartmentNo": "",
                "buildingNo": "",
                "telephone": contactPersonPhone,
                "additionalPhone": contactPersonPhone,
                "countryId": 101041
            },
            "addressData": {
                "regionName": regionName,
                "housingType": settlement,
                "localityName": "",
                "streetName": street,
                "houseNo": house,
                "apartmentNo": "",
                "buildingNo": "",
                "telephone": contactPersonPhone,
                "additionalPhone": contactPersonPhone,
                "countryId": 101041,
                "managerId": 1010861
            },
            "mobilePhone": mobilePhone,
            "email": "-",
            "creditProductId": 101339,  # 101339 - test 10133793 - prod
            # "relatives": [
            #     {
            #     "lastName": lastName,
            #     "firstName": firstName,
            #     "patronymic": "",
            #     "telephone": employerPhone,
            #     "collateralRelId": 1021415
            #     }
            #               ],
            "extraFields": [
                {
                    "key": "client.rnn",
                    "value": iin
                },
                {
                    "key": "client.education.id",
                    "value": "1011010"
                },
                {
                    "key": "client.Resident",
                    "value": residencyStatus
                },
                {
                    "key": "client.DocIssueMan",
                    "value": issuer
                },
                {
                    "key": "client.maritalStatus.id",
                    "value": maritalStatus
                },
                {
                    "key": "client.workPlaceData.workPlace",
                    "value": "-"
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
                    "value": "-"
                },
                {
                    "key": "client.workPlaceData.website",
                    "value": "-"
                },
                {
                    "key": "client.workPlaceData.workAge",
                    "value": "-"
                },
                {
                    "key": "client.monthlyIncome2NDFL",
                    "value": "-"
                },
                {
                    "key": "client.meanIncome",
                    "value": officialIncome
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
        resp['birthDate'] = datetime.datetime.strptime(resp['birthDate'], '%d.%m.%Y').strftime('%Y-%m-%d')
        resp["passport"]['closeDate'] = datetime.datetime.strptime(resp["passport"]['closeDate'], '%d.%m.%Y').strftime('%Y-%m-%d')
        resp["passport"]['issueDate'] = datetime.datetime.strptime(resp["passport"]['issueDate'] , '%d.%m.%Y').strftime('%Y-%m-%d')
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
                        if sendDocs(dataClient, photoBack, photoFront, photo) == 400:
                            return Response("Files not uploaded", status=status.HTTP_204_NO_CONTENT)
                        else:
                            serializer.save(lead=dataLead, applicationId=dataApp,
                                            clientId=dataClient, jsonRequest=dict((request.data)))
                            return Response({"leadID": dataLead,"applicationId":dataApp,"clientId":dataClient,
                                             "status":secondRes['data']['currentStatus'],
                                             "car price":price,
                                             "durations":duration,
                                             "insurance":data['insurance'],
                                             "downpayment":data['downpayment']}, status=status.HTTP_200_OK)
                    else:
                        return Response("Приложение не создано", status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"lead не создался"}, status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({"Ошибка в отправке запроса, неверные данные"}, status.HTTP_204_NO_CONTENT)
        else:
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
            id = IsAllur.objects.get(lead = leadId)
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
