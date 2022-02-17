from datetime import datetime

import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


class AuthBackend(authentication.BaseAuthentication):

    def authenticate(self, request, token=None):
        try:
            auth_header = request.headers['Token'].split(' ')
        except:
            return None

        if not auth_header or auth_header[0].lower() != 'barrer':
            raise exceptions.AuthenticationFailed('Need to add "Barrer" before token value')

        if len(auth_header) == 1 or len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header')

        return self.authenticate_credential(auth_header[1])

    def authenticate_credential(self, token) -> tuple:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')

        token_exp = datetime.fromtimestamp(payload['exp'])
        if token_exp < datetime.utcnow():
            raise exceptions.AuthenticationFailed('Token expired.')

        try:
            user = User.objects.get(id=payload['id'])
            user.last_request = datetime.utcnow()
            user.save()
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user matching this token was found.')

        return user, None
