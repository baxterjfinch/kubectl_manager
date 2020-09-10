import requests
import requests.auth
from rauth import OAuth2Service

class PlatformRequester:
    def __init__(self):
        self._access_token = None


    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, token):
        self._access_token = token
        print("\nAccess Token set to {0}\n".format(self._access_token))

    def create_item_type(self):
        pass
