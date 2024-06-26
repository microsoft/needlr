from ... import _http
# from ..item import item
from ...auth.auth import _FabricAuthentication

# Intentionally blank to avoid any import coming from here
__all__ = [
    'ADMIN', 'CONTRIBUTOR', 'MEMBER', 'VIEWER',
    'GroupPrincipal', 'ServicePrincipal', 'UserPrincipal'
]

ADMIN = "Admin"
CONTRIBUTOR = "Contributor"
MEMBER = "Member"
VIEWER = "Viewer"

class _Principal():
    def __init__(self, id, type_name) -> None:
        self._id = id
        self._type = type_name
    def to_json(self):
        output = self.__dict__.copy()
        output["id"] = output.pop("_id")
        output["type"] = output.pop("_type")

        return output

class _WorkspaceRoleClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces)

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        self._auth = auth
        self._base_url = base_url

    def assign(self, workspace_id:str, principal:_Principal, role_name:str):
        """
        Assign a Principal to a Workspace for a given role

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/add-workspace-role-assignment?tabs=HTTP)
        """
        body = {
            "principal":principal.to_json(),
            "role": role_name
        }
        resp = _http._post_http(
            url = self._base_url+f"workspaces/{workspace_id}/roleAssignments",
            auth=self._auth,
            json=body,
            responseNotJson=True
        )
        return resp

    def delete(self, workspace_id:str, principal:_Principal):
        """
        Delete a Principal's Role Assignment

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/delete-workspace-role-assignment?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = self._base_url+f"workspaces/{workspace_id}/roleAssignments/{principal._id}",
            auth=self._auth,
            responseNotJson=True
        )
        return resp

    def ls(self, workspace_id:str, **kwargs):
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

    def update(self, workspace_id:str, principal:_Principal, role_name:str):
        """
        Update a Principal's Role Assignment

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/update-workspace-role-assignment?tabs=HTTP)
        """
        resp = _http._patch_http(
            url = self._base_url+f"workspaces/{workspace_id}/roleAssignments/{principal._id}",
            auth=self._auth,
            json={"role":role_name},
            responseNotJson=True
        )
        return resp

class GroupPrincipal(_Principal):
    def __init__(self, id, groupType) -> None:
        super().__init__(id, type_name="Group")

class ServicePrincipal(_Principal):
    def __init__(self, id) -> None:
        super().__init__(id, type_name="ServicePrincipal")

class UserPrincipal(_Principal):
    def __init__(self, id, ) -> None:
        super().__init__(id, type_name="User")
