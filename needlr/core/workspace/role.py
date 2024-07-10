"""Module providing a Core WorkspaceRole functions."""

from collections.abc import Iterator
from needlr import _http
from needlr._http import FabricResponse
from needlr.auth.auth import _FabricAuthentication
from needlr.models.workspace import _Principal, GroupPrincipal, ServicePrincipal, UserPrincipal, ServicePrincipalProfile, WorkspaceRole

# Intentionally blank to avoid any import coming from here
__all__ = [
    'GroupPrincipal', 'ServicePrincipal', 'UserPrincipal', 'ServicePrincipalProfile'
]
class _WorkspaceRoleClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces)

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        self._auth = auth
        self._base_url = base_url

    def assign(self, workspace_id:str, principal:_Principal, role:WorkspaceRole) -> FabricResponse:
        """
        Assign a Principal to a Workspace for a given role

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/add-workspace-role-assignment?tabs=HTTP)
        """
        body = {
            "principal":principal.to_json(),
            "role": role
        }
        resp = _http._post_http(
            url = self._base_url+f"workspaces/{workspace_id}/roleAssignments",
            auth=self._auth,
            json=body,
            responseNotJson=True
        )
        return resp

    def delete(self, workspace_id:str, principal:_Principal)  -> FabricResponse:
        """
        Delete a Principal's Role Assignment

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/delete-workspace-role-assignment?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = self._base_url+f"workspaces/{workspace_id}/roleAssignments/{principal.id}",
            auth=self._auth,
            responseNotJson=True
        )
        return resp

    def ls(self, workspace_id:str, **kwargs) -> Iterator[FabricResponse]:
        """
        List Role Assignments

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/get-workspace-role-assignments?tabs=HTTP)
        """
        # TODO: Implement retry / error handling
        resp = _http._get_http_paged(
            url = self._base_url+f"workspaces/{workspace_id}/roleAssignments",
            auth=self._auth,
            items_extract=lambda x:x["value"],
            **kwargs
        )
        for page in resp:
            for item in page.items:
                yield item

    def update(self, workspace_id:str, principal:_Principal, role:WorkspaceRole) -> FabricResponse:
        """
        Update a Principal's Role Assignment

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/update-workspace-role-assignment?tabs=HTTP)
        """
        resp = _http._patch_http(
            url = self._base_url+f"workspaces/{workspace_id}/roleAssignments/{principal.id}",
            auth=self._auth,
            json={"role":role},
            responseNotJson=True
        )
        return resp
