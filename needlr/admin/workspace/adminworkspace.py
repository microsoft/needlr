from .. import item
from ... import _http
from ...auth.auth import _FabricAuthentication

class _AdminWorkspaceClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces)

    ### Coverage

    * Get Workspace > get()
    * Get Workspace Role Assignments > role_ls()
    * List Workspaces > ls()

    ### Required Scopes
        Tenant.Read.All or Tenant.ReadWrite.All

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        self._auth = auth
        self._base_url = base_url
    
    def get(self, workspace_id:str=None, workspace_name:str=None, workspace_region:str=None):
        """
        Get Workspaces

        Workspace name and region or workpsace id (guid) make it unique.

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/get-workspace?tabs=HTTP)
        """
        resp = _http._get_http(
            url = self._base_url+f"admin/workspaces/{workspace_id}",
            auth=self._auth
        )
        return resp

    def ls(self, **kwargs):
        """
        List Workspaces

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/workspaces/list-workspaces?tabs=HTTP)
        """
        # Implement retry / error handling / continuation token
        resp = _http._get_http_paged(
            url = self._base_url+"admin/workspaces",
            auth=self._auth,
            items_extract=lambda x:x["workspaces"],
            **kwargs
        )
        for page in resp:
            for item in page.items:
                yield item
    
    def item_ls(self, type:str=None, capacity_id:str=None, state:str=None, workspace_id:str=None):
        return item._list_items_by_filter(base_url=self._base_url, type=type, capacity_id=capacity_id, state=state, workspace_id=workspace_id, auth=self._auth)
        