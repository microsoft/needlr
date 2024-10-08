import json
import time
from collections.abc import Iterator

from needlr.auth.auth import _FabricAuthentication
from needlr import _http
from needlr._http import FabricResponse
from needlr.models.item import Item, ItemType

class _ItemClient():
    """
    Item Client

    This class provides methods for interacting with items in the fabric workspace.

    Methods:
    - create_item: Create an item in the fabric workspace.
    - list_items: Retrieve a list of items from the specified workspace.
    - list_items_by_filter: List items of a specific type based on the provided filters.
    """
    
    def create_item(self, base_url, workspace_id:str, fabric_item:Item, auth:_FabricAuthentication, wait_for_success=False, retry_attempts=5) -> FabricResponse:
        """
        Create Item

        This method is used to create an item in the fabric workspace.

        Parameters:
        - base_url (str): The base URL of the fabric API.
        - workspace_id (str): The ID of the workspace where the item will be created.
        - fabric_item (Item): The item object to be created.
        - auth (_FabricAuthentication): The authentication object for making API requests.
        - wait_for_success (bool): Flag indicating whether to wait for the item creation to succeed. Default is False.
        - retry_attempts (int): The number of retry attempts if the item creation is not successful. Default is 5.

        Returns:
        - FabricResponse: The response object containing the result of the item creation.

        References:
        - [Create Item API](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/create-item?tabs=HTTP)
        - [Get Operation State API](https://learn.microsoft.com/en-us/rest/api/fabric/core/long-running-operations/get-operation-state?tabs=HTTP#operationstate)
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
            for _ in range(retry_attempts):
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
                raise _http.NeedlerRetriesExceeded(json.dumps({"Location":create_op.next_location, "error":"010-needlr failed to retrieve object status in set retries"}))

    def list_items(self, base_url, workspace_id:str, auth:_FabricAuthentication, **kwargs)  -> Iterator[Item]:
        """
        List Items

        Retrieves a list of items from the specified workspace.

        Args:
            base_url (str): The base URL of the API.
            workspace_id (str): The ID of the workspace.
            auth (_FabricAuthentication): The authentication object.
            **kwargs: Additional keyword arguments to be passed to the API.

        Yields:
            Item: An item object representing each item retrieved.

        Returns:
            Iterator[Item]: An iterator of item objects.

        Reference:
        [Microsoft Documentation](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/list-items?tabs=HTTP)
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

        This method lists items of a specific type based on the provided filters.

        Args:
            base_url (str): The base URL of the API.
            workspace_id (str): The ID of the workspace.
            auth (_FabricAuthentication): The authentication object.
            item_type (ItemType): The type of the item.
            **kwargs: Additional keyword arguments.

        Returns:
            Iterator[Item]: An iterator of Item objects.

        Reference:
        - [List Items API](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/list-items?tabs=HTTP)
        """
        # Implement retry / error handling
        params = {k:v for k,v in {'type': item_type
                                ,'workspaceId': workspace_id
                                }.items() 
                                if v is not None and v != ""
                }
        yield from self.list_items(base_url=base_url, workspace_id=workspace_id, auth=auth, params=params, **kwargs)
