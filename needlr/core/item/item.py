import json
import time
from collections.abc import Iterator

from needlr.auth.auth import _FabricAuthentication
from needlr import _http
from needlr._http import FabricResponse
from needlr.models.item import Item, ItemType

class _ItemClient():

    def create_item(self, base_url, workspace_id:str, fabric_item:Item, auth:_FabricAuthentication, wait_for_success=False, retry_attempts=5) -> FabricResponse:
        """
        Create Item

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/create-item?tabs=HTTP)
        [Operation State Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/long-running-operations/get-operation-state?tabs=HTTP#operationstate)
        """
        create_op = _http._post_http(
            url = base_url+f"workspaces/{workspace_id}/items",
            auth=auth,
            json=fabric_item.model_dump()
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

    def list_items(self, base_url, workspace_id:str, auth:_FabricAuthentication, **kwargs)  -> Iterator[Item]:
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
                yield Item(**item)

    def list_items_by_filter(self, base_url:str, workspace_id:str, auth:_FabricAuthentication, item_type:ItemType, **kwargs) -> Iterator[Item]:
        """
        List Items of a Specific Type

        [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/list-items?tabs=HTTP)
        """
        # Implement retry / error handling
        params = {k:v for k,v in {'type': item_type
                                ,'workspaceId': workspace_id
                                }.items() 
                                if v is not None and v != ""
                }
        yield from self.list_items(base_url=base_url, workspace_id=workspace_id, auth=auth, params=params, **kwargs)
