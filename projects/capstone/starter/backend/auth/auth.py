from urllib.request import urlopen
from flask import request
from functools import wraps
from jose import jwt
import json

AUTH0_DOMAIN = 'iamfsnd.us.auth0.com'
ALGORITHM = ['RS256']
API_AUDIENCE = 'courses'


class AuthError(Exception):
    def __init__(self, error, status_code) -> None:
        self.error = error
        self.status_code = status_code


def get_auth_header():
    try:
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            raise AuthError({
                "error": "Authorization not in header",
                "description": "Header must contain Authorization parameter"
            }, 401)

        header_parts = auth_header.split(' ')
        if header_parts[0].lower() != 'bearer':
            raise AuthError({
                'error': 'No Bearer part',
                'description': 'Authorization first part should be Bearer'
            }, 401)
        elif len(header_parts) < 2:
            raise AuthError({
                'error': 'authorization header length less than 2',
                'description': 'Authorization should contain Bearer and Token parts'
            }, 401)
        else:
            token = header_parts[1]
            return token
    except Exception as e:
        print(e)


def verify_jwt(token):
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())

    unverified_header = jwt.get_unverified_header(token)
    if 'kid' not in unverified_header:
        raise AuthError({
            'error': 'kid not in token header',
            'description': 'kid is part of the JWT header'
        }, 401)

    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e'],
            }
    if rsa_key:
        try:
            payload = jwt.decode(token, rsa_key, algorithms=ALGORITHM,
                                 audience=API_AUDIENCE,
                                 issuer=f'https://{AUTH0_DOMAIN}/')
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the' +
                'audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)

    raise AuthError({
        'error': 'error decoding token header',
        'description': 'Unable to find appropriate kid in token header'
    }, 401)


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'error': 'Payload does not have permissions set',
            'description': 'Set permissions on the payload'
        }, 401)

    if permission not in payload['permissions']:
        raise AuthError({
            'error': 'Invalid permission',
            'description': 'permission not included in the payload'
        }, 401)
    else:
        return True


def authorize_user(permission=''):
    def require_auth(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = get_auth_header()
            payload = verify_jwt(token)
            check_permissions(permission, payload)
            return fn(*args, **kwargs)
        return wrapper
    return require_auth
