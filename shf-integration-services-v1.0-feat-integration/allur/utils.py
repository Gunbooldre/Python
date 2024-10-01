from . import schemas
import os

production = os.getenv("PRODUCTION")

def prepare_data_to_brainy_soft(lead_information: schemas.LeadInputSchema) -> dict:

        maritalStatus = lead_information.customer.marital_status
        match maritalStatus:
            case 'SINGLE':
                maritalStatus = '101151'
            case 'MARRIED':
                maritalStatus = '101152'

        issuer = lead_information.customer.document.issuer
        match issuer:
            case 'MINISTRY_OF_THE_INTERIOR':
                issuer = 'МВД РК'
            case 'MINISTRY_OF_JUSTICE':
                issuer = 'МЮ РК'

        residencyStatus = lead_information.customer.residency_status
        match residencyStatus:
            case 'NOT_RESIDENT':
                residencyStatus = 'Нерезидент'
            case 'RESIDENT':
                residencyStatus = 'Резидент'

        gender = lead_information.customer.gender
        match gender:
            case 'MALE':
                gender = '101251'
            case 'FEMALE':
                gender = '101252'
        official_income = lead_information.customer.official_income

        data =  {
            "channel": "GENERATOR",
            "subdivisionId": 101791,
            "lastName": lead_information.customer.lastname,
            "firstName": lead_information.customer.firstname,
            "patronymic": lead_information.customer.patronymic,
            "inn": lead_information.customer.iin,
            "birthDate": lead_information.customer.birth_date,
            "sexId": gender,
            "birthCountryId": 101041,
            "amount": lead_information.car.price,
            "period": lead_information.duration,
            "birthPlace": lead_information.customer.birth_place,
            "passport": {
                'no': lead_information.customer.document.number,
                'issueDate': lead_information.customer.document.issued_date,
                'closeDate': lead_information.customer.document.expiration_date,
                "seria": "0001"
            },
            "registrationAddressData": {
                "regionName": lead_information.customer.registration_address.region,
                "housingType": lead_information.customer.registration_address.settlement,
                "localityName": "",
                "streetName": lead_information.customer.registration_address.street,
                "houseNo": lead_information.customer.registration_address.house,
                "apartmentNo": "",
                "buildingNo": "",
                "telephone": lead_information.customer.contact_person_phone,
                "additionalPhone": lead_information.customer.contact_person_phone,
                "countryId": 101041
            },
            "addressData": {
                "regionName": lead_information.customer.registration_address.region,
                "housingType": lead_information.customer.registration_address.settlement,
                "localityName": "",
                "streetName": lead_information.customer.registration_address.street,
                "houseNo": lead_information.customer.registration_address.house,
                "apartmentNo": "",
                "buildingNo": "",
                "telephone": lead_information.customer.contact_person_phone,
                "additionalPhone": lead_information.customer.contact_person_phone,
                "countryId": 101041,
                "managerId": 1010861
            },
            "mobilePhone": lead_information.customer.mobile_phone,
            "email": "-",
            "creditProductId": 101339, 
              # 101339 - test 10133793 - prod
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
                    "value": lead_information.customer.iin
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
                    "value": official_income
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

        return data



def prepare_data_to_create_collateral(lead_information: schemas.LeadInputSchema, 
                                      client_id: int, 
                                      partner_name: str) -> dict:

    data = {
    "name": "Автомобиль",
    "collateralTypeId": 101762, # одинавый на тесте и проде
    "depositorId": client_id,
    "document": "",
    "comment": "",
    "assessedValue": lead_information.car.price,
    "hypothecationValue": lead_information.car.price,
    "collateralProperties": [
        {
            "collateralPropertyTypeId": 10184647 if production else 10184650,
            "value": partner_name,
            "orderId": 0
        },
        {
            "collateralPropertyTypeId": 10184649 if production else 10184651,
            "value": lead_information.car.brand,
            "orderId": 0
        },
        {
            "collateralPropertyTypeId": 10184651 if production else 10184656,
            "value":  lead_information.downpayment/float(lead_information.car.price)*100,
            "orderId": 0
        },
        {
            "collateralPropertyTypeId": 10184653 if production else 10184658,
            "value": lead_information.downpayment,
            "orderId": 0
        },
        {
            "collateralPropertyTypeId": 10184655 if production else 10184660,
            "value": lead_information.car.price,
            "orderId": 0
        },
        {
            "collateralPropertyTypeId": 10184658 if production else 10184652,
            "value": lead_information.car.brand,
            "orderId": 0
        },
        {
            "collateralPropertyTypeId": 10184660 if production else 10184653,
            "value": lead_information.car.model,
            "orderId": 0
        },
        {
            "collateralPropertyTypeId": 10184662 if production else 10184665,
            "value": lead_information.car.colour,
            "orderId": 0
        },
        {
            "collateralPropertyTypeId": 10184664 if production else 10184667,
            "value": lead_information.car.year,
            "orderId": 0
        },
        {
            "collateralPropertyTypeId": 10184665 if production else 10184668,
            "value": lead_information.car.condition,
            "orderId": 0
        },
        {
            "collateralPropertyTypeId": 10184667 if production else 10184670,
            "value": lead_information.car.type, #vincod?
            "orderId": 0
        }
    ]
    }
    return data

import json

def prepare_data_to_edit_app(app_data: str, collateral_id: int):
    app_data = json.loads(app_data)
    data = {
    "id": app_data["data"]["id"],
    "name": app_data["data"]["id"],
    "collateralIds": [int(collateral_id[0])],
    "creationDate": app_data["data"]["creationDate"],
    "clientId": app_data["data"]["clientId"],
    "currencyId": app_data["data"]["currencyId"],
    "creditProductId": app_data["data"]["creditProductId"],
    "creditFieldReq": {
        "id": app_data["data"]["creditFieldReq"]["id"],
        "dateCalcMethodId": app_data["data"]["creditFieldReq"]["dateCalcMethodId"],
        "allowHolidaysPayment": app_data["data"]["creditFieldReq"]["allowHolidaysPayment"],
        "shortTermControl": app_data["data"]["creditFieldReq"]["shortTermControl"],
        "shiftFirstRepaymentDate": app_data["data"]["creditFieldReq"]["shiftFirstRepaymentDate"],
        "interestChargeMethodId": app_data["data"]["creditFieldReq"]["interestChargeMethodId"],
        "interestCalcMethodId": app_data["data"]["creditFieldReq"]["interestCalcMethodId"],
        "repaymentNorm": app_data["data"]["creditFieldReq"]["repaymentNorm"],
        "calcIntOnIssueDate": app_data["data"]["creditFieldReq"]["calcIntOnIssueDate"],
        "calcInterestOnDelinqBalance": app_data["data"]["creditFieldReq"]["calcInterestOnDelinqBalance"],
        "calcIntOnDelinqBalanceOnlyAtDelinqIntRate": app_data["data"]["creditFieldReq"]["calcIntOnDelinqBalanceOnlyAtDelinqIntRate"],
        "calcArrearInterest": app_data["data"]["creditFieldReq"]["calcArrearInterest"],
        "arrearInterestFirstDay": app_data["data"]["creditFieldReq"]["arrearInterestFirstDay"],
        "arrearInterestLastDay": app_data["data"]["creditFieldReq"]["arrearInterestLastDay"],
        "principalDistribMethodId": app_data["data"]["creditFieldReq"]["principalDistribMethodId"],
        "forepaymentConsiderationMethodId": app_data["data"]["creditFieldReq"]["forepaymentConsiderationMethodId"],
        "creditLineId": app_data["data"]["creditFieldReq"]["creditLineId"],
        "trancheDuration": app_data["data"]["creditFieldReq"]["trancheDuration"],
        "interestForTranche": app_data["data"]["creditFieldReq"]["interestForTranche"],
        "delinquencyIntRate": app_data["data"]["creditFieldReq"]["delinquencyIntRate"],
        "delinqIntRateDelay": app_data["data"]["creditFieldReq"]["delinqIntRateDelay"],
        "delinqIntDaysLimit": app_data["data"]["creditFieldReq"]["delinqIntDaysLimit"],
        "useDelinqIntRateTillNextTranche": app_data["data"]["creditFieldReq"]["useDelinqIntRateTillNextTranche"],
        "keepUsingDelinqIntRate": app_data["data"]["creditFieldReq"]["keepUsingDelinqIntRate"],
        "interestRateTypeId": app_data["data"]["creditFieldReq"]["interestRateTypeId"],
        "chargeExtraInterest": app_data["data"]["creditFieldReq"]["chargeExtraInterest"],
        "extraIntDaysQty": app_data["data"]["creditFieldReq"]["extraIntDaysQty"],
        "interestLgotPeriod": app_data["data"]["creditFieldReq"]["interestLgotPeriod"],
        "interestLgotRate": app_data["data"]["creditFieldReq"]["interestLgotRate"],
        "interestGracePeriod": app_data["data"]["creditFieldReq"]["interestGracePeriod"],
        "trancheCount": app_data["data"]["creditFieldReq"]["trancheCount"],
        "repaymentSequenceId": app_data["data"]["creditFieldReq"]["repaymentSequenceId"],
        "mandatoryChargePeriod": app_data["data"]["creditFieldReq"]["mandatoryChargePeriod"],
        "allowPrepayment": app_data["data"]["creditFieldReq"]["allowPrepayment"],
        "prolongationPeriod": app_data["data"]["creditFieldReq"]["prolongationPeriod"],
        "earlyProlongationFromCurrentDate": app_data["data"]["creditFieldReq"]["earlyProlongationFromCurrentDate"],
        "prolongationOnNewSchedule": app_data["data"]["creditFieldReq"]["prolongationOnNewSchedule"],
        "prolongedIntToLastTranche": app_data["data"]["creditFieldReq"]["prolongedIntToLastTranche"],
        "penaltyTypeId": app_data["data"]["creditFieldReq"]["penaltyTypeId"],
        "calendarDaysPenalty": app_data["data"]["creditFieldReq"]["calendarDaysPenalty"],
        "firstWeekendWithoutPenalty": app_data["data"]["creditFieldReq"]["firstWeekendWithoutPenalty"],
        "stopPenaltyOnClose": app_data["data"]["creditFieldReq"]["stopPenaltyOnClose"],
        "qtyDaysStopPenaltyOnClose": app_data["data"]["creditFieldReq"]["qtyDaysStopPenaltyOnClose"],
        "fixedDelayPenalty": app_data["data"]["creditFieldReq"]["fixedDelayPenalty"],
        "delayPenaltyDay": app_data["data"]["creditFieldReq"]["delayPenaltyDay"],
        "inviteAmountPct": app_data["data"]["creditFieldReq"]["inviteAmountPct"],
        "inviteDiscountPerFriend": app_data["data"]["creditFieldReq"]["inviteDiscountPerFriend"],
        "inviteMinIntRate": app_data["data"]["creditFieldReq"]["inviteMinIntRate"],
        "scheduleRecalcEnabled": app_data["data"]["creditFieldReq"]["scheduleRecalcEnabled"],
        "fullScheduleDatesRecalc": app_data["data"]["creditFieldReq"]["fullScheduleDatesRecalc"],
        "useDelinqIntRateForPsk": app_data["data"]["creditFieldReq"]["useDelinqIntRateForPsk"],
        "discountingEnabled": app_data["data"]["creditFieldReq"]["discountingEnabled"],
        "useEirForDiscounting": app_data["data"]["creditFieldReq"]["useEirForDiscounting"],
        "fees": [],
        "principalParts": [],
        "penaltyRates": [
            {
                "id": app_data["data"]["creditFieldReq"]["penaltyRates"][0]["id"],
                "periodBegin": app_data["data"]["creditFieldReq"]["penaltyRates"][0]["periodBegin"],
                "periodEnd": app_data["data"]["creditFieldReq"]["penaltyRates"][0]["periodEnd"],
                "principalRate": app_data["data"]["creditFieldReq"]["penaltyRates"][0]["principalRate"],
                "interestRate": app_data["data"]["creditFieldReq"]["penaltyRates"][0]["interestRate"],
                "feeRate": app_data["data"]["creditFieldReq"]["penaltyRates"][0]["feeRate"],
            }
        ],
    },
    "loanAmount": app_data["data"]["loanAmount"]
    }

    return data