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

    * Add Workspace Role Assignment > assign()
    * Delete Workspace Role Assignment > delete()
    * Get Workspace > get()
    * List Workspace Role Assignments > ls()
    * Update Workspace Role Assignment > update()    

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a Role object.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the role.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def assign(self, workspace_id:str, principal:_Principal, role:WorkspaceRole) -> FabricResponse:
        """
        Assign a Principal to a Workspace for a given role

        Args:
            workspace_id (str): The ID of the workspace to assign the principal to.
            principal (_Principal): The principal to be assigned to the workspace.
            role (WorkspaceRole): The role to assign to the principal.

        Returns:
            FabricResponse: The response from the API call.

        Reference:
        - [Add Workspace Role Assignment](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/add-workspace-role-assignment?tabs=HTTP)
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

    def delete(self, workspace_id: str, principal: _Principal) -> FabricResponse:
        """
        Delete a Principal's Role Assignment

        This method deletes a role assignment for a principal in a workspace.

        Args:
            workspace_id (str): The ID of the workspace.
            principal (_Principal): The principal whose role assignment needs to be deleted.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
        [Delete Workspace Role Assignment](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/delete-workspace-role-assignment?tabs=HTTP)
        """
        resp = _http._delete_http(
            url=self._base_url + f"workspaces/{workspace_id}/roleAssignments/{principal.id}",
            auth=self._auth,
            responseNotJson=True
        )
        return resp

    def ls(self, workspace_id:str, **kwargs) -> Iterator[FabricResponse]:
        """
        List Role Assignments

        Retrieves a list of role assignments for a specific workspace.

        Args:
            workspace_id (str): The ID of the workspace for which to retrieve role assignments.
            **kwargs: Additional keyword arguments that can be passed to customize the request.

        Yields:
            FabricResponse: An iterator of role assignment objects.

        Raises:
            Any exceptions that occur during the request.

        Reference:
            [Microsoft Documentation](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/get-workspace-role-assignments?tabs=HTTP)
        """
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

        This method updates the role assignment of a principal for a specific workspace.

        Args:
            workspace_id (str): The ID of the workspace.
            principal (_Principal): The principal whose role assignment needs to be updated.
            role (WorkspaceRole): The new role to assign to the principal.

        Returns:
            FabricResponse: The response from the API call.

        Reference:
        [Microsoft Docs - Update Workspace Role Assignment](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/update-workspace-role-assignment?tabs=HTTP)
        """
        resp = _http._patch_http(
            url = self._base_url+f"workspaces/{workspace_id}/roleAssignments/{principal.id}",
            auth=self._auth,
            json={"role":role},
            responseNotJson=True
        )
        return resp
