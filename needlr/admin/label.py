"""Module providing a Core Workspace functions."""

from needlr._http import FabricResponse
from needlr import _http
from needlr.auth.auth import _FabricAuthentication
import uuid

from needlr.models.workspace import _Principal, UserPrincipal
# Intentionally blank to avoid any import coming from here
__all__ = [
    'UserPrincipal'
]

class _LabelClient():
    """

    Set or remove sensitivity labels

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/labels)

    ### Coverage

    * Bulk remove > bulk_remove()
    * Bulk set > bulk_set()

    """
    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a new instance of the Label class.

        Args:
            auth (_FabricAuthentication): The authentication object used for authentication.
            base_url (str): The base URL of the label.

        """
        self._auth = auth
        self._base_url = base_url

    def bulk_remove(self, item_list: list[dict]) -> FabricResponse:
        """
        Bulk remove labels from items.

        Args:
            item_list (list[dict]): A list of items to remove the label from.
                Each item should be a dictionary containing the following keys:
                - id: The ID of the item.
                - type: The type of the item (e.g., "Workspace", "Item").

        Returns:
            FabricResponse: The response from the API call.
        """
        url = "https://api.fabric.microsoft.com/v1/admin/items/bulkRemoveLabels"
        body = {"items": item_list}
        print(body)
        return _http._post_http(url=url, auth=self._auth, params=body)
    
    def bulk_set(self, item_list: list[dict], label_id: uuid.UUID,assignmentMethod:str = None, delegatedPrincipal:_Principal = None) -> FabricResponse:
        """
        Bulk set labels on items.

        Args:
            item_list (list[dict]): A list of items to set the label on.
                Each item should be a dictionary containing the following keys:"
                "id: The ID of the item."
                "type: The type of the item (e.g., "Workspace", "Item").
            label_id (uuid.UUID): The ID of the label to set.
            assignmentMethod (str, optional): The assignment method for the label. Defaults to None.
            delegatedPrincipal (_Principal, optional): The principal to delegate the label assignment to. Defaults to None.
                Only principals of type 'User' are supported (UserPrincipal)
                The default is None, which means no delegation.
            
            "Returns:
            FabricResponse: The response from the API call. 
            """
        url = "https://api.fabric.microsoft.com/v1/admin/items/bulkSetLabels"
        body = {
            "items": item_list,
            "labelId": str(label_id),
        }
        if assignmentMethod is not None:
            body["assignmentMethod"] = assignmentMethod
        if delegatedPrincipal is not None:
            if isinstance(delegatedPrincipal, UserPrincipal):
                body["delegatedPrincipal"] = {
                    "id": str(delegatedPrincipal.id),
                    "type": "User"
                }
        return _http._post_http(url=url, auth=self._auth, params=body)