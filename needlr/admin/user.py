"""Module providing Admin Users functions."""

from collections.abc import Iterator
from needlr import _http
import uuid
from needlr.auth.auth import _FabricAuthentication
from needlr.models.domain import Domain
import json
from needlr.models.item import Item, ItemType

class _UserClient():
    """
    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/users)

    ### Coverage

    * List Access Entities > access()

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a User object.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the User.

        """        
        self._auth = auth
        self._base_url = base_url

    def access(self, userId: str, itemType: ItemType = None) -> Iterator[Item]:
        """
        Get list of permission

        This method Returns a list of permission details for Fabric and PowerBI items the specified user can access.

        Args:
            
            UserId (str): The ID of the user whose permissions you want to retrieve.
            ItemType (ItemType): The type of item to filter by. If None, all items are returned.

        Returns:
            Domain: the domain information
        """
        url = f"GET https://api.fabric.microsoft.com/v1/admin/users/{userId}/access"
        if itemType:
            url += f"?type={str(itemType.value)}"

        resp = _http._get_http_paged(
            url = url,
            auth=self._auth,
            items_extract=lambda x:x["accessEntities"]
        )
        for page in resp:
            for item in page.items:
                yield Item(**item) 
        