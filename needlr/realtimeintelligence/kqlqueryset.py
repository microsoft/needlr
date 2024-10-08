"""Module providing Core KQLQuerySet functions."""

from typing import Optional
from collections.abc import Iterator
import uuid

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
from needlr.models.kqlqueryset import KQLQuerySet
from needlr.models.item import Item, ItemType



class _KQLQuerySetClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/kqlqueryset/items)

    ### Coverage

    * Delete KQLQuerySet > delete()
    * Get KQLQuerySet > get()
    * List KQLQuerySet > ls()
    * Update KQLQuerySet > update()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a KQLQuerySet object.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL for the KQLQuerySet.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def delete(self, workspace_id:uuid.UUID, kqlQuerySet_id:uuid.UUID) -> FabricResponse:
        """
        Delete KQLQuerySet

        Deletes a KQLQuerySet from a workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace.
            kqlQuerySet_id (uuid.UUID): The ID of the KQLQuerySet.

        Returns:
            FabricResponse: The response from the delete request.

        Reference:
            [Delete KQLQuerySet](https://learn.microsoft.com/en-us/rest/api/fabric/kqlqueryset/items/delete-kql-queryset?tabs=HTTP)
        """
        resp = _http._delete_http(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlQuerysets/{kqlQuerySet_id}",
            auth=self._auth
        )
        return resp
  
    def get(self, workspace_id:uuid.UUID, kqlQuerySet_id:uuid.UUID) -> KQLQuerySet:
        """
        Get KQLQuerySet

        Retrieves a KQLQuerySet from the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace containing the KQLQuerySet.
            kqlQuerySet_id (uuid.UUID): The ID of the KQLQuerySet to retrieve.

        Returns:
            KQLQuerySet: The retrieved KQLQuerySet.

        References:
            - [Get KQLQuerySet](https://learn.microsoft.com/en-us/rest/api/fabric/kqlqueryset/items/get-kql-queryset?tabs=HTTP)
        """
        resp = _http._get_http(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlQuerysets/{kqlQuerySet_id}",
            auth=self._auth
        )
        kqlQuerySet = KQLQuerySet(**resp.body)
        return kqlQuerySet

    def ls(self, workspace_id:uuid.UUID) -> Iterator[KQLQuerySet]:
            """
            List KQLQuerySets

            Retrieves a list of KQLQuerySets associated with the specified workspace ID.

            Args:
                workspace_id (uuid.UUID): The ID of the workspace.

            Yields:
                Iterator[KQLQuerySet]: An iterator of KQLQuerySet objects.

            Reference:
                [List KQLQuerySets](https://learn.microsoft.com/en-us/rest/api/fabric/kqlqueryset/items/list-kql-querysets?tabs=HTTP)
            """
            resp = _http._get_http_paged(
                url = f"{self._base_url}workspaces/{workspace_id}/kqlQuerysets",
                auth=self._auth,
                items_extract=lambda x:x["value"]
            )
            for page in resp:
                for item in page.items:
                    yield KQLQuerySet(**item)

    def update(self, workspace_id:uuid.UUID, kqlQuerySet_id:uuid.UUID, display_name:str, description:str=None) -> KQLQuerySet:
        """
        Update KQLQuerySet

        This method updates the definition of a KQLQuerySet in Power BI.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the KQLQuerySet is located.
            kqlQuerySet_id (uuid.UUID): The ID of the KQLQuerySet to update.
            display_name (str): The updated display_name of the KQLQuerySet.
            description (str): The updated description of the KQLQuerySet.

        Returns:
            KQLQuerySet: The updated KQLQuerySet object.

        Reference:
        - [Update KQLQuerySet Definition](https://learn.microsoft.com/en-us/rest/api/fabric/kqlqueryset/items/update-kql-queryset?tabs=HTTP)
        """
        body = dict()
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        resp = _http._patch_http(
            url = f"{self._base_url}workspaces/{workspace_id}/kqlQuerysets/{kqlQuerySet_id}",
            auth=self._auth,
            item=Item(**body)
        )
        kqlQuerySet = KQLQuerySet(**resp.body)
        return kqlQuerySet

    def create(self, workspace_id:uuid.UUID, display_name:str, description:str=None) -> FabricResponse:
        """
        Create RadWrite KQLQuerySet

        This method creates a Shortcut KQLQuerySet in the specified workspace.

        Args:
            workspace_id (uuid.UUID): The ID of the workspace where the KQLQuerySet will be created.
            display_name (str): The display name of the KQLQuerySet.
            description (str, optional): The description of the KQLQuerySet. Defaults to None.

        Returns:
            FabricResponse: The response from the create request.

        Reference:
        [Create KQLQuerySet](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/create-item?tabs=HTTP#itemdefinition)
        """
        body = {
            "displayName":display_name,
            'type': ItemType.KQLQueryset
        }
        if description:
            body["description"] = description

        resp = _http._post_http_long_running(
            url = f"{self._base_url}workspaces/{workspace_id}/items",
            auth=self._auth,
            item=Item(**body)
        )
        return resp