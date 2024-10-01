from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional


class VerificationSchema(BaseModel):
    code: str
    date: str


class CarSchema(BaseModel):
    brand: str
    colour: str
    condition: str
    country: str
    fuel_type: str = "GAZOLINE"
    model: str
    price: str
    type: str
    year: str

    @validator('price', allow_reuse=True)
    def validate_price(cls, value):
        if isinstance(value, str):
            return int(float(value))
        return value 

class AddressSchema(BaseModel):
    district: str
    flat: str
    house: str
    region: str
    settlement: str
    street: str


class DocumentSchema(BaseModel):
    country_of_residence: str = Field(alias="countryOfResidence")
    expiration_date: str = Field(alias="expirationDate")
    issued_date: str = Field(alias="issuedDate")
    issuer: str
    number: str
    photo_back: str = Field(alias="photoBack")
    photo_front: str = Field(alias="photoFront")
    type: str

    @validator('expiration_date', check_fields=False)
    def validate_expiration_date(cls, value):
        try:
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('Неверный формат даты в поле expirationDate')
        return value.strftime("%Y-%m-%d")   
    
    @validator('issued_date', check_fields=False)
    def validate_issued_date(cls, value):
        try:
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('Неверный формат даты в поле issuedDate')
        return value.strftime("%Y-%m-%d")     

class CustomerSchema(BaseModel):
    actual_address: AddressSchema = Field(alias="actualAddress") 
    birth_date: str = Field(alias="birthDate")
    birth_place: str = Field(alias="birthPlace")
    contact_person_full_name: str = Field(alias="contactPersonFullName")
    contact_person_phone: str = Field(alias="contactPersonPhone")
    document: DocumentSchema
    employer_address: AddressSchema = Field(alias="employerAddress")
    employer_name: str = Field(alias="employerName")
    employer_phone: str = Field(alias="employerPhone")
    employment_type: str = Field(alias="employmentType")
    firstname: str
    gender: str
    iin: str
    income: bool
    lastname: str
    marital_status: str = Field(alias="maritalStatus")
    mobile_phone: str = Field(alias="mobilePhone")
    number_of_dependents: int = Field(alias="numberOfDependents")
    official_income: float = Field(alias="officialIncome")
    patronymic: str
    photo: str
    registration_address: AddressSchema = Field(alias="registrationAddress")
    residency_status: str = Field(alias="residencyStatus")


    @validator('birth_date', check_fields=False)
    def validate_birth_date(cls, value):
        try:
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('Неверный формат даты в поле birthDate')
        return value.strftime("%Y-%m-%d")  


class LeadInputSchema(BaseModel):
    calculation_type: Optional[str] = Field(alias="calculationType")
    car: CarSchema
    cas: bool
    city: str
    customer: CustomerSchema
    discount: bool
    downpayment: float
    duration: int
    gos_program: bool = Field(alias="gosProgram")
    grace: bool
    instalment_date: str  = Field(alias="instalmentDate")
    insurance: bool
    partner_id: str = Field(alias="partnerId")
    verification: VerificationSchema


    @validator('instalment_date', check_fields=False)
    def validate_instalment_date(cls, value):
        try:
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('Неверный формат даты в поле instalment_date')
