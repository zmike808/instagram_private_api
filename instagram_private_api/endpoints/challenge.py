import json

from ..errors import ClientError, ClientLoginError


class ChallengeEndpointsMixin(object):
    """For endpoints in ``/challenge/``."""

    def send_challenge(self, account_id, identifier, code):
        """
        Authorize account by solving challenge
        :param account_id:
        :param identifier:
        :param code: code we got from email or sms
        :return:
        """
        login_params = {
            'security_code': code,
            'guid': self.uuid,
            'device_id': self.device_id,
            '_csrftoken': self.csrftoken,
            '_uuid': self.uuid,
            '_uid': self.authenticated_user_id
        }

        response = self._call_api(
            'challenge/{account_id}/{identifier}/'.format(account_id=account_id, identifier=identifier),
            params=login_params, return_response=True
        )

        if not self.csrftoken:
            raise ClientError(
                'Unable to get csrf from login.',
                error_response=self._read_response(response))

        login_json = json.loads(self._read_response(response))

        if not login_json.get('logged_in_user', {}).get('pk'):
            raise ClientLoginError('Unable to login.')

        if self.on_login:
            on_login_callback = self.on_login
            on_login_callback(self)

    def choose_confirm_method(self, account_id, identifier, confirm_method=1):
        """
        Choose whether you want to confirm your account by email or phone number
        0 - sms
        1 - email
        :return:
        """
        params = {
            'choice': confirm_method,
            'guid': self.uuid,
            'device_id': self.device_id,
            '_csrftoken': self.csrftoken,
            '_uuid': self.uuid,
            '_uid': self.authenticated_user_id
        }

        response = self._call_api(
            'challenge/{account_id}/{identifier}/'.format(account_id=account_id, identifier=identifier),
            params=params, return_response=True
        )

        response_json = json.loads(self._read_response(response))

        return response_json
