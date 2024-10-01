import os
import requests
import json


from .models import Lead
from .schemas import LeadInputSchema
from .utils import prepare_data_to_brainy_soft, prepare_data_to_create_collateral, prepare_data_to_edit_app
from .tasks import create_files_on_file_system

#urls
bs_lead_url = os.getenv("BS_CREATE_LEAD_URL")
bs_auth_url = os.getenv("BS_AUTH_URL")
bs_file_system_url = os.getenv("BS_FILE_SYSTEM_URL")

bs_collateral_url = os.getenv("BS_COLLATERAL_URL")
bs_app_url = os.getenv("BS_APPLICATION_URL")

#credentials
bs_username = os.getenv("BS_USERNAME")
bs_password = os.getenv("BS_PASSWORD")
customer_key = os.getenv("CUSTOMER_KEY")


def start_integration_process(lead_object: Lead, handled_data: LeadInputSchema, partner_name: str) -> dict:
    """
    1. authorize
    2. create lead on brainy soft
    3. run check process to take client_id and app_id
    4. send files to brainy soft by client id
    5. create collateral 
    6. edit application
    7. returns info about created lead(start_integration_process, client_id, application_id)
    """
    
    token = authorize_on_bs()
    lead_id = create_lead_on_bs(lead_object=lead_object, token=token, data=handled_data)
    checked_succesfully = run_checks_on_a_lead(lead_id=lead_id, token=token)
    if checked_succesfully:
        client_id, application_id = get_lead_info_by_id(lead_id=lead_id, token=token)
        lead_object.client_id = client_id
        lead_object.app_id = application_id
        lead_object.save()
    else:
        raise Exception(f"Leads check process failed")
    
    collateral_id = create_collateral(lead_information=handled_data, 
                      client_id=client_id, 
                      partner_name=partner_name,
                      token=token), 

    edit_application(collateral_id=collateral_id, 
                     app_id=application_id, 
                     client_id=client_id, 
                     token=token)

    current_status = get_app_current_status(app_id=application_id)

    create_files_on_file_system.delay(
        client_id=client_id,
        token=token,
        front_side=handled_data.customer.document.photo_front,
        back_side=handled_data.customer.document.photo_back,
        doc_photo=handled_data.customer.photo,
        _id=lead_object.id
        )
    
    return lead_id, client_id, application_id, current_status, collateral_id


def authorize_on_bs() -> str:
    session = requests.Session()
    credentials_to_auth = {"userName":bs_username, "password":bs_password}
    auth_headers = {'Content-Type': 'application/json','customer-key':customer_key}  #TODO customer key не должен быть в  енвах надо позже исправить
    auth_response = session.post(url=bs_auth_url, json=credentials_to_auth, headers=auth_headers)
    if auth_response.status_code!=200:
        raise Exception(f"Authentication failed with status code: {auth_response.status_code}")
    
    token = auth_response.headers["bsauth"]
    return token


def create_lead_on_bs(lead_object: Lead, token: str, data: LeadInputSchema) -> int:
    """creates lead on BS and update lead id on local DB"""
    validated_data = prepare_data_to_brainy_soft(data)
    create_lead_headers = {'Content-Type': 'application/json', "bsauth":token}
    response = requests.post(url=bs_lead_url, headers=create_lead_headers, data=json.dumps(validated_data))
    if response.status_code != 200:
            raise Exception(f"Failed to create lead with status code: {response.status_code}")
    lead_id = response.json()["data"]
    lead_object.lead_id_on_bs = lead_id
    lead_object.save()
    return lead_id


def run_checks_on_a_lead(lead_id: int, token: str) -> None:
    """created client_id and app_id for this lead"""
    check_lead_url = bs_lead_url+"/"+str(lead_id)+"/check"
    response = requests.post(url=check_lead_url, headers={
             'Content-Type': 'application/json', 
             "bsauth":token
             })
    if response.status_code != 200:
        raise Exception(f"Failed to run process of creating app_id and client_id for lead: {response.status_code}")

    response = response.json()
    return True if response["status"]=="ok" else False


def get_lead_info_by_id(lead_id:int, token: str)-> tuple:
    lead_info_url = bs_lead_url+f"/{lead_id}"
    get_lead_header = {
             'Content-Type': 'application/json', 
             "bsauth":token
             }
    response_about_lead = requests.get(url=lead_info_url, headers=get_lead_header)
    if response_about_lead.status_code!=200:
        raise Exception(f"get lead information failed for lead with id {lead_id}  with response code {response_about_lead.status_code}")
    response = response_about_lead.json()
    client_id = response["data"]["clientId"]
    application_id = response['data']['loanApplicationId']
    return client_id, application_id


def get_app_current_status(app_id: int):
    token = authorize_on_bs()
    print("token", token)
    headers = {
        'Content-Type': 'application/json', 
        "bsauth": token,
        "customer-key":customer_key
    }
    get_app_url = bs_app_url + f"/{app_id}"
    response = requests.get(url=get_app_url, headers=headers)
    print()
    print(response.status_code)
    print()

    application = response.json()
    current_status = application["data"]["currentStatusId"]
    match current_status:
        case 101541:
            result = 'Ожидает'
        case 101542:
            result = 'Отказано'
        case 101543:
            result = 'Выдан'
        case 101544:
            result = 'К выдаче'
        case 101545:
            result = 'Ожидает рассмотрения'
        case 101546:
            result = 'В рассмотрении'
        case 101547:
            result = 'Автоматическая проверка'
        case 101548:
            result = "Отказ клиента"
        case _:
            result = "Неизвестно"
    return result
    
def get_lead_status_from_bs(lead_id: int) -> str:
    token = authorize_on_bs()
    lead_info_url = bs_lead_url + f"/{lead_id}"
    get_lead_header = {
        'Content-Type': 'application/json', 
        "bsauth": token
    }
    response_about_lead = requests.get(url=lead_info_url, headers=get_lead_header)
    if response_about_lead.status_code != 200:
        raise Exception(
            f"get lead information failed for lead with id {lead_id} with response code {response_about_lead.status_code}"
        )
    response = response_about_lead.json()
    current_status = response['data']['currentStatus']

    return current_status


def create_collateral(lead_information: LeadInputSchema, client_id: int, partner_name: str, token: str) -> int:
    "создает залог к клиенту"
    data = prepare_data_to_create_collateral(lead_information=lead_information, 
                                             client_id=client_id, 
                                             partner_name=partner_name)
    url = bs_collateral_url
    # url = "https://shinhantest-saas.brainysoft.ru/bs-core/main/collaterals"
    headers ={
        'Content-Type': 'application/json', 
        "bsauth": token
    }
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    if response.status_code!=200:
        raise Exception(f"Create collaterial failed with status code: {response.status_code}")
    response = response.json()
    print("create_collateral", response["data"]["id"])
    return response["data"]["id"]


def edit_application(collateral_id: int, app_id: int, client_id: int, token: int):
    """добавляет к сушествующей заявке данные по залогу"""
    headers = {
        'Content-Type': 'application/json', 
        "bsauth": token,
        "customer-key":"shinhantest"
    }
    get_app_url = bs_app_url + f"/{app_id}"
    response = requests.get(url=get_app_url, headers=headers)

    data = prepare_data_to_edit_app(app_data=response.text, collateral_id=collateral_id)

    edit_app_url = bs_app_url + f"/{app_id}"
    edit_app_response = requests.put(url=edit_app_url, data=json.dumps(data), headers=headers)
    if edit_app_response.status_code!=200:
        raise Exception(f"Editing application process failed with status: {edit_app_response.status_code}")
    print("edit_application, добавляет к сушествующей заявке данные по залогу, status_code=", edit_app_response.status_code)