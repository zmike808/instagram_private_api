import json
import codecs
from instagram_private_api import Client, ClientError, ClientTwoFactorRequiredError


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))


username = 'username'
password = 'password'
settings_file = '/path/to/file/settings_{}.json'.format(username)

api = Client(username, password, on_login=lambda x: onlogin_callback(x, settings_file))
try:
    api.login()
except ClientTwoFactorRequiredError as e:
    response = json.loads(e.error_response)
    settings = e.settings
    two_factor_info = response['two_factor_info']
    phone_number_tail = two_factor_info['obfuscated_phone_number']
    two_factor_identifier = two_factor_info['two_factor_identifier']
    verification_code = input('Enter verification code, sent on number ending with {}: '.format(phone_number_tail))
    try:
        api.login2fa(two_factor_identifier, verification_code)
    except ClientError as e:
        print(e.error_response)
