from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    '^09\d{9}$', message='Invalide phone number', code='invalide_phone_number')