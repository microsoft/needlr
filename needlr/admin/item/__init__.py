import json
import time

from ...auth.auth import _FabricAuthentication
from ... import _http
from .item import FabricItem, LakehouseItem, WarehouseItem


def _list_items(base_url:str, auth:_FabricAuthentication, **kwargs):
    """
    List Items

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/items/list-items?tabs=HTTP)
    """
    # Implement retry / error handling
    resp = _http._get_http_paged(
        url = base_url+f"admin/items",
        auth=auth,
        items_extract=lambda x:x["itemEntities"],
        **kwargs
    )
    for page in resp:
        for item in page.items:
            yield item

def _list_items_of_type(base_url, type_name:str, auth:_FabricAuthentication, **kwargs):
    """
    List Items of a Specific Type

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/items/list-items?tabs=HTTP)
    """
    # Implement retry / error handling
    yield from _list_items(base_url, auth, params={"type":type_name}, **kwargs)



