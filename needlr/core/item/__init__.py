import json
import time

from ...auth.auth import _FabricAuthentication
from ... import _http
from .item import FabricItem, LakehouseItem, WarehouseItem

def _create_item(base_url,workspace_id:str, fabric_item:FabricItem, auth:_FabricAuthentication, wait_for_success=False, retry_attempts=5):
    """
    Create Item

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/create-item?tabs=HTTP)
    [Operation State Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/long-running-operations/get-operation-state?tabs=HTTP#operationstate)
    """

    create_op = _http._post_http(
        url = base_url+f"workspaces/{workspace_id}/items",
        auth=auth,
        json=fabric_item.to_json()
    )
    if not wait_for_success:
        return create_op

    if create_op.is_created:
        return create_op
    if create_op.is_accepted and wait_for_success:
        _completed = False
        _retry_after = create_op.retry_after
        _result = {}
        for trial in range(retry_attempts):
            time.sleep(_retry_after)
            op_status = _http._get_http(
                url=create_op.next_location,
                auth=auth
            )
            # If it's a non-terminal state, keep going
            if op_status.body["status"] in ["NotStarted", "Running", "Undefined"]:
                _retry_after = op_status.retry_after
                continue
            # Successful state, get the response from the Location header
            elif op_status.body["status"] == "Succeeded":
                _completed = True
                # Get Operation Results?
                op_results = _http._get_http(
                    url=op_status.next_location,
                    auth=auth
                )
                _result = op_results
                break
            # Unhandled but terminal state
            else:
                _completed = True
                _result = op_status
                break
        # Fall through
        if _completed:
            return _result
        else:
            raise _http.NeedlerRetriesExceeded(json.dumps({"Location":create_op.next_location, "error":"010-needler failed to retrieve object status in set retries"}))

def _list_items(base_url, workspace_id:str, auth:_FabricAuthentication, **kwargs):
    """
    List Items

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/list-items?tabs=HTTP)
    """
    # Implement retry / error handling
    resp = _http._get_http_paged(
        url = base_url+f"workspaces/{workspace_id}/items",
        auth=auth,
        items_extract=lambda x:x["value"],
        **kwargs
    )
    for page in resp:
        for item in page.items:
            yield item

def _list_items_of_type(base_url, workspace_id:str, type_name:str, auth:_FabricAuthentication, **kwargs):
    """
    List Items of a Specific Type

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/list-items?tabs=HTTP)
    """
    # Implement retry / error handling
    yield from _list_items(base_url, workspace_id, auth, params={"type":type_name}, **kwargs)
