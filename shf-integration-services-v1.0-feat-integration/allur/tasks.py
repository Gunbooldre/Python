from celery import shared_task
import os
import base64
import requests

from .models import Lead
from .schemas import LeadInputSchema

#urls
bs_lead_url = os.getenv("BS_CREATE_LEAD_URL")
bs_auth_url = os.getenv("BS_AUTH_URL")
bs_file_system_url = os.getenv("BS_FILE_SYSTEM_URL")

#credentials
bs_username = os.getenv("BS_USERNAME")
bs_password = os.getenv("BS_PASSWORD")
customer_key = os.getenv("CUSTOMER_KEY")


@shared_task
def create_files_on_file_system(client_id: int, token: str, front_side: str, back_side: str, doc_photo: str, _id: int) -> None:
    """Таска, запускает процесс отправки документов асинхронно, затем апдейтит статус documents_sent_status=True"""
    from .models import Lead
    front_photo_file, back_photo_file, document_photo_file = prepare_files_to_send(front_side=front_side, back_side=back_side, doc_photo=doc_photo)
    file_create_url = bs_file_system_url+f"/{customer_key}/add?client={client_id}"
    response_code = send_file_to_bs(url=file_create_url, file=document_photo_file, type_of_file="photo", token=token)
    response_code = send_file_to_bs(url=file_create_url, file=back_photo_file, type_of_file="document", token=token)
    response_code = send_file_to_bs(url=file_create_url, file=front_photo_file, type_of_file="document", token=token)
    if response_code == 200:
        lead_object = Lead.objects.get(id=_id)
        lead_object.documents_sent_status = True
        lead_object.save

    
def prepare_files_to_send(front_side: str, back_side: str, doc_photo: str) -> tuple:
    """Takes base64 objects and return files"""
    photo_front_side_file = base64.b64decode(front_side)
    photo_back_side_file = base64.b64decode(back_side)
    document_photo_file = base64.b64decode(doc_photo)
    return photo_front_side_file, photo_back_side_file, document_photo_file
    

def send_file_to_bs(url, file, type_of_file, token):
    payload = {}
    header = {'bsauth': token}
    if type_of_file=='document':
        files = [('file', ('IDCARD.pdf', file, 'application/pdf'),)]
        response = requests.request("POST", url+'&tags=4', headers=header, files=files)
        return response.status_code

    if type_of_file=="photo":
        files = [('file', ('photo.jpeg', file, 'image/jpeg'),)]
        response = requests.request("POST", url+'&tags=1', headers=header, data=payload, files=files)
        return response.status_code
    # if response.status_code!=200:
    #      raise Exception(f"error while sending file to bs, with response code: {response.status_code}")