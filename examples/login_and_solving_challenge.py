import json
import codecs
import re

from instagram_private_api import Client, ClientError, ClientCheckpointRequiredError


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
except ClientCheckpointRequiredError as e:
    challenge_url = e.challenge_url

    challenge_pattern = r'.*challenge/(?P<account_id>\d.*)/(?P<identifier>\w.*)/'
    match = re.search(challenge_pattern, challenge_url)
    if not match:
        raise ClientError('Unable to parse challenge')

    match_dict = match.groupdict()
    account_id = match_dict['account_id']
    identifier = match_dict['identifier']

    res = api.choose_confirm_method(account_id, identifier)  # confirm_method param has default value 1, you can pass 0
    code = input('Enter code from email: ')
    api.send_challenge(account_id, identifier, code)
