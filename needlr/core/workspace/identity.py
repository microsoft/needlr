"""Module providing Core Workspace Identity functions."""

from needlr import _http
from needlr._http import FabricResponse
from needlr.auth.auth import _FabricAuthentication

class _WorkspaceIdentityClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces)

    ### Coverage

    * Provision a workspace identity for a workspace. > provision_identity()
    * Deprovision a workspace identity for a workspace. > deprovision_identity()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes an Identity object.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the role.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def provision_identity(self, workspace_id:str) -> FabricResponse:
        """
        Assign a Principal to a Workspace for a given role

        Args:
            workspace_id (str): The ID of the workspace to assign the principal to.

        Returns:
            FabricResponse: The response from the API call.

        Reference:
        - [Add Workspace Role Assignment](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/provision-identity?tabs=HTTP)
        """
        resp = _http._post_http(
            url = self._base_url+f"workspaces/{workspace_id}/provisionIdentity",
            auth=self._auth,
            responseNotJson=True
        )
        return resp

    def deprovision_identity(self, workspace_id:str) -> FabricResponse:
        """
        Assign a Principal to a Workspace for a given role

        Args:
            workspace_id (str): The ID of the workspace to assign the principal to.

        Returns:
            FabricResponse: The response from the API call.

        Reference:
        - [Add Workspace Role Assignment](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/deprovision-identity?tabs=HTTP)
        """
        resp = _http._post_http(
            url = self._base_url+f"workspaces/{workspace_id}/deprovisionIdentity",
            auth=self._auth,
            responseNotJson=True
        )
        return resp