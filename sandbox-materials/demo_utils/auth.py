"""ODM API authentication helpers."""

import os
import re
import time
import threading
import warnings
from getpass import getpass

import odm_api
from azure.identity import InteractiveBrowserCredential
from dotenv import load_dotenv

_active_client = None


class AutoRefreshingApiClient:
    """
    Wraps odm_api.ApiClient with automatic background Azure token refresh.
    
    A daemon thread renews the token after refresh_ratio (default 0.9) of its
    lifetime has elapsed. Call stop() to end the refresh thread.
    """
    def __init__(
        self,
        configuration: odm_api.Configuration,
        azure_credential,
        azure_scope: str,
        refresh_ratio: float = 0.9,
    ) -> None:
        self.configuration = configuration
        self.azure_credential = azure_credential
        self.azure_scope = azure_scope
        self.refresh_ratio = refresh_ratio
        self.token_issued_at = 0
        self.token_expiry = 0
        self._stop_event = threading.Event()
        self._get_access_token()
        self.client = odm_api.ApiClient(configuration)
        self._start_background_refresh()

    def stop(self):
        self._stop_event.set()

    def _get_access_token(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            access_token = self.azure_credential.get_token(self.azure_scope)
        self.configuration.api_key['Access-token'] = access_token.token
        self.configuration.api_key_prefix['Access-token'] = 'Bearer'
        self.token_issued_at = time.time()
        self.token_expiry = access_token.expires_on

    def _start_background_refresh(self):
        def _refresh_loop():
            while not self._stop_event.is_set():
                lifetime = self.token_expiry - self.token_issued_at
                delay = lifetime * self.refresh_ratio
                if self._stop_event.wait(delay):
                    break
                self._get_access_token()
        self._refresh_thread = threading.Thread(target=_refresh_loop, daemon=True)
        self._refresh_thread.start()


def set_api_configuration(
    odm_url: str,
    use_azure_auth: bool = True,
    azure_scope: str = 'https://management.core.windows.net/.default',
    dotenv_path: str = '.env',
    token_env_var: str = 'ODM_API_TOKEN',
) -> odm_api.ApiClient:
    """
    Create and validate an ODM API client for the demo notebook.
    
    Authentication priority:
    1. Azure interactive browser login (if use_azure_auth=True).
    2. Token from dotenv_path (.env) under token_env_var.
    3. Token already present in the environment.
    4. Manual token prompt (getpass).
    
    Parameters:
    - odm_url: ODM instance base URL (UI paths are stripped).
    - use_azure_auth: Try Azure InteractiveBrowserCredential first.
    - azure_scope: Azure AD scope for the access token.
    - dotenv_path: Path to a .env file for the API token.
    - token_env_var: Environment variable name for the Genestack API token.
    
    Returns:
    - Authenticated client ready for endpoint classes.
    """
    odm_url = re.sub(r'/ui/.+$', '', odm_url).rstrip('/')
    configuration = odm_api.Configuration(host=odm_url)
    docs_url = f"{odm_url}/user-docs/tools/odm-api/python/generated/"

    def validate(client):
        odm_api.StudySPoTAsUserApi(client).search_studies_as_user(page_limit=1)

    global _active_client
    if _active_client is not None:
        _active_client.stop()
        _active_client = None

    azure_ok = False
    auto_client = None
    if use_azure_auth:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                azure_credential = InteractiveBrowserCredential()
            auto_client = AutoRefreshingApiClient(configuration, azure_credential, azure_scope)
            _active_client = auto_client
            validate(auto_client.client)
            print(f"Azure authentication successful! Docs: {docs_url}")
            azure_ok = True
        except Exception as e:
            if auto_client is not None:
                auto_client.stop()
            _active_client = None
            print(f"Azure authentication failed: {e}")

    if not azure_ok:
        configuration.api_key.clear()
        configuration.api_key_prefix.clear()

        # try loading token from .env file, then from environment
        load_dotenv(dotenv_path=dotenv_path, override=False)
        token = os.environ.get(token_env_var)

        if token:
            print(f"Using token from environment variable '{token_env_var}'.")
        else:
            print(f"'{token_env_var}' not found in environment or {dotenv_path}. Falling back to manual input.")
            token = getpass('Auth Token: ')

        configuration.api_key['Genestack-API-Token'] = token
        api_client = odm_api.ApiClient(configuration)
        try:
            validate(api_client)
            print(f"Token authentication successful! Docs: {docs_url}")
        except Exception as e:
            raise RuntimeError(f"Token authentication failed: {e}") from e

    return auto_client.client if azure_ok else api_client
