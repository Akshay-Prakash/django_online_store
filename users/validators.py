from rest_framework.exceptions import ValidationError


def validate_address_belongs_to_user(user, address):
    if user != address.user:
        raise ValidationError(
            detail=f'This address is not saved for the user: {user.username}.'
        )
    return True
