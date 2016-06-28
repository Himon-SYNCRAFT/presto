from suds import WebFault
from suds.client import Client
from presto.allegro_client.exceptions import VersionKeyNotAvailable
from hashlib import sha256
import base64


class AllegroClient:
    _wsdl = 'https://webapi.allegro.pl.webapisandbox.pl/service.php?wsdl'
    _endpoint = 'https://webapi.allegro.pl.webapisandbox.pl/service.php'
    _version_key = None
    _session = None
    _country_id = 1  # Polska

    def __init__(self):
        self._client = Client(self._wsdl, location=self._endpoint)
        self._service = self._client.service

    def login(self, webapi_key, login, password):
        if self._version_key is None:
            self._set_version_key(webapi_key)

        self._session = self._service.doLoginEnc(
            userLogin=login,
            userHashPassword=self._encode_password(password),
            countryCode=self._country_id,
            webapiKey=webapi_key,
            localVersion=self._version_key
        ).sessionHandlePart

        return self._session

    def change_price(self):
        pass

    def add_new_auction(self):
        pass

    def update_auction(self):
        pass

    def end_auction(self):
        pass

    def _set_version_key(self, webapi_key):
        sys_sountry_status = self._service.doQueryAllSysStatus(
            countryId=self._country_id, webapiKey=webapi_key)

        sys_status_types = sys_sountry_status['item']

        for item in sys_status_types:
            if item['countryId'] == self._country_id:
                self._version_key = item['verKey']
                break
        else:
            raise VersionKeyNotAvailable

    def _encode_password(self, password):
        return base64.b64encode(sha256(password).digest()).decode('utf-8')
