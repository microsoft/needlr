from abc import ABC
import atexit
from datetime import datetime, timedelta
import os
import json
import shutil
from typing import List

from . import scopes

from msal import PublicClientApplication, ConfidentialClientApplication, SerializableTokenCache

INTERACTIVE = "interactive"
DEVICE_FLOW = "device"

DEVELOPER_SIGN_ON_CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"

# Factory
# interactive > InteractiveAuth
# device > DeviceAuth
# token > TokenAuth ? later on support them providing us the token?

class _FabricAuthentication(ABC):
    def __init__(self) -> None:
        self._token = None
        self._expiration = datetime.now()
    def _get_token(self) -> str:
        raise NotImplementedError()
    def get_auth_header(self) -> dict:
        return {
            "Authorization": "Bearer " + self._get_token(),
            "Content-Type": "application/json"
        }

class _CacheableMixin(ABC):
    def __init__(self):
        super().__init__()
        # TODO: Make this configurable?
        self._cache_directory = ".needlr"
        self._cache_filename = "token.cache.bin"
        self._cache = SerializableTokenCache()
        self._establish_cache()

    def _establish_cache(self):
        if not os.path.exists(self._cache_directory):
            os.mkdir(self._cache_directory)
        if os.path.exists(os.path.join(self._cache_directory, self._cache_filename)):
            self._cache.deserialize(open(os.path.join(self._cache_directory, self._cache_filename), "r").read())
        atexit.register(lambda:
            open(os.path.join(self._cache_directory, self._cache_filename), "w").write(self._cache.serialize())
            # Hint: The following optional line persists only when state changed
            if self._cache.has_state_changed else None
            )

class FabricInteractiveAuth(_CacheableMixin, _FabricAuthentication):
    """
    Interactive Authentication requiring the user to login so Needlr can
    impersonate the user.

    kwargs:
    redirect_uri=None
    domain_hint=None
    """
    def __init__(self, scopes:List[str]=[scopes.DEFAULT], client_id:str=DEVELOPER_SIGN_ON_CLIENT_ID, authority:str=None, **interactive_auth_kwargs) -> None:
        super().__init__()
        _client_id = client_id
        _authority = authority or "https://login.microsoftonline.com/organizations"
        
        self._scopes = scopes
        self._interactive_auth_kwargs = interactive_auth_kwargs
        
        self._app = PublicClientApplication(
            _client_id,
            authority= _authority,
            token_cache = self._cache
        )

    def _set_access_token(self) -> None:
        # TODO: Should this bet set only once?
        account_dict = None
        _list_of_accounts = self._app.get_accounts()
        if len(_list_of_accounts) > 0:
            account_dict = _list_of_accounts[0]
        try:
            auth_json = self._app.acquire_token_silent(
                scopes=self._scopes,
                account = account_dict,
                token_cache = self._cache,
                **self._interactive_auth_kwargs
            )
        except Exception as e:
            print(f"Silent failed: {e} \nTrying interactive...")
            auth_json = self._app.acquire_token_interactive(
                scopes=self._scopes,
                **self._interactive_auth_kwargs
            )
        if auth_json is None:
            print("Token not found in cache. Trying Interactive...")
            auth_json = self._app.acquire_token_interactive(
                scopes=self._scopes,
                **self._interactive_auth_kwargs
            )
        _requested_at = datetime.now()
        if "error" in auth_json:
            error_str=json.dumps(auth_json)
            raise RuntimeError(f"001-Failed to get auth token: {error_str}")
        
        self._token = auth_json["access_token"]
        self._expiration = _requested_at + timedelta(seconds=auth_json["expires_in"])

    def _get_token(self) -> str:
        if datetime.now() >= self._expiration:
            self._set_access_token()
        return self._token

class FabricServicePrincipal(_CacheableMixin, _FabricAuthentication):
    """
    Service Principal authentication to enable user-less interaction with Fabric.
    Please note, not all Fabric APIs support Service Principal authentication.

    kwargs:
    redirect_uri=None
    """
    def __init__(self, client_id:str, client_secret:str, tenant_id:str, scopes:List[str]=[scopes.DEFAULT], authority:str=None, **client_auth_kwargs) -> None:
        super().__init__()
        self._client_id = client_id
        self._client_secret = client_secret
        self._tenant_id = tenant_id
        self._authority = authority or "https://login.microsoftonline.com/"
        self._app = ConfidentialClientApplication(
            self._client_id,
            self._client_secret,
            authority= self._authority+self._tenant_id,
            token_cache=self._cache
        )
        self._scopes = scopes
        self._client_auth_kwargs = client_auth_kwargs
        
    def _set_access_token(self) -> None:
        auth_json = self._app.acquire_token_for_client(
            scopes=self._scopes,
            **self._client_auth_kwargs
        )
        _requested_at = datetime.now()
        if "error" in auth_json:
            error_str=json.dumps(auth_json)
            raise RuntimeError(f"002-Failed to get auth token: {error_str}")
        
        self._token = auth_json["access_token"]
        self._expiration = _requested_at + timedelta(seconds=auth_json["expires_in"])

    def _get_token(self) -> str:
        if datetime.now() >= self._expiration:
            self._set_access_token()
        return self._token
