"""Module providing Admin Tenant functions."""

from collections.abc import Iterator
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.tenant import TenantSetting, TenantSettingOverrides

class _TenantClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/tenants)

    ### Coverage
    
    List Capacities Tenant Settings Overrides -> list_capacities_tenant_settings_overrides()
    List Tenant Settings -> lts()

    ### Required Scopes
        Tenant.Read.All or Tenant.ReadWrite.All    

    """

    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a Tenant client to support tenant level operations.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the role.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url    

    def lts(self, **kwargs) -> Iterator[TenantSetting]:
            """

            Returns a list of the tenant settings.

            Args:
                **kwargs: Additional keyword arguments that can be passed to customize the request.

            Returns:
                Iterator[TenantSetting]: An iterator that yields TenantSetting objects representing each TenantSetting.

            Reference:
            - [List Tenant Settings](https://learn.microsoft.com/en-us/rest/api/fabric/admin/tenants/list-tenant-settings?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}admin/tenantsettings",
                auth= self._auth,
                items_extract=lambda x:x["tenantSettings"],
            )

            for page in resp:
                for item in page.items:
                    yield TenantSetting(**item)

    def list_capacities_tenant_settings_overrides(self, **kwargs) -> TenantSettingOverrides:
        """
        Returns list of tenant setting overrides that override at the capacities.

        This API supports pagination. A maximum of 10,000 records can be returned per request. With the continuation token provided in the response, you can get the next 10,000 records.

        The user must be a Fabric Service Administrator or authenticate using a service principal.

        Args:

        Returns:
            TenantSettingOverrides: The retrieved object.

        Reference:
        [Tenants - List Capacities Tenant Settings Overrides](https://learn.microsoft.com/en-us/rest/api/fabric/admin/tenants/list-capacities-tenant-settings-overrides?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}admin/capacities/delegatedTenantSettingOverrides",
            auth=self._auth
        )

        # convert the None to 'None' for the response due to the impedence mismatch between the API and the model
        # None va 'None'
        # TODO: Find a better way of handling this and document this needed.
        for k,v in resp.body.items():
            if v is None:
                resp.body[k] = 'None'

        return TenantSettingOverrides(**resp.body)
