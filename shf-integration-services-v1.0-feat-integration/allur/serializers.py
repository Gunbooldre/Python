from rest_framework import serializers


class VerificationSerializer(serializers.Serializer):
    code = serializers.CharField()
    date = serializers.DateTimeField() #надо чекнуть что требует BS


class CarSerializer(serializers.Serializer):
    brand = serializers.CharField()
    colour = serializers.CharField()
    condition = serializers.CharField()
    country = serializers.CharField()
    fuelType = serializers.CharField(source='fuel_type')
    model = serializers.CharField()
    price = serializers.DecimalField(decimal_places=2, max_digits=10)
    type = serializers.CharField()
    year = serializers.CharField()


class AddressSerializer(serializers.Serializer):
    district = serializers.CharField()
    flat = serializers.CharField()
    house = serializers.CharField()
    region = serializers.CharField()
    settlement = serializers.CharField()
    street = serializers.CharField()


class DocumentSerializer(serializers.Serializer):
    countryOfResidence = serializers.CharField()
    expirationDate = serializers.CharField()
    issuedDate = serializers.CharField()
    issuer = serializers.CharField()
    number = serializers.CharField()
    photoBack = serializers.CharField()
    photoFront = serializers.CharField()
    type = serializers.CharField()

class CustomerSerializer(serializers.Serializer):
    actualAddress = AddressSerializer()
    birthDate = serializers.CharField()
    birthPlace = serializers.CharField()
    contactPersonFullName = serializers.CharField()
    contactPersonPhone = serializers.CharField()
    document = DocumentSerializer()
    employerAddress = AddressSerializer()
    employerName = serializers.CharField()
    employerPhone = serializers.CharField()
    employmentType = serializers.CharField()
    firstname = serializers.CharField()
    gender = serializers.CharField()
    iin = serializers.CharField()
    income = serializers.BooleanField()
    lastname = serializers.CharField()
    maritalStatus = serializers.CharField()
    mobilePhone = serializers.CharField()
    numberOfDependents = serializers.IntegerField()
    officialIncome = serializers.DecimalField(decimal_places=2, max_digits=10)
    patronymic = serializers.CharField()
    photo = serializers.CharField()
    registrationAddress = AddressSerializer()
    residencyStatus = serializers.CharField()

class LeadInputSerializer(serializers.Serializer):
    calculationType = serializers.CharField()
    car = CarSerializer()
    cas = serializers.BooleanField()
    city = serializers.CharField()
    customer = CustomerSerializer()
    discount = serializers.BooleanField()
    downpayment = serializers.DecimalField(decimal_places=2, max_digits=10)
    duration = serializers.IntegerField()
    gosProgram = serializers.BooleanField()
    grace = serializers.BooleanField()
    instalmentDate = serializers.CharField()
    insurance = serializers.BooleanField()
    partnerId = serializers.CharField()
