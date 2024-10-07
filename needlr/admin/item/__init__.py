import json
import time

from needlr.auth.auth import _FabricAuthentication
from needlr import _http
from .item import FabricItem, LakehouseItem, WarehouseItem
from . import types

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

def _list_items_by_filter(base_url, auth:_FabricAuthentication, type:str=None, capacity_id:str=None, state:str=None, workspace_id:str=None, **kwargs):
    """
    List Items of a Specific Type

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/items/list-items?tabs=HTTP)
    """
    # Implement retry / error handling
    params = {k:v for k,v in {'type': type
                              ,'capacityId': capacity_id
                              ,'state': state
                              ,'worspaceId': workspace_id
                              }.items() 
                              if v is not None and v != ""
            }
    yield from _list_items(base_url, auth, params=params, **kwargs)




