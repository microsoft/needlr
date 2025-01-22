"""Module providing a HTTP call features."""

from needlr import __version__
from needlr.utils.util import FabricException
from needlr.auth.auth import _FabricAuthentication
from needlr.models.item import Item

import json
import logging
import time
from urllib.parse import unquote
from typing import Callable, Generator, List, Union

import requests

module_logger = logging.getLogger('needlr')

class FabricResponse():
    # body: Union[dict, bytes]
    """
    Interface for a response from Fabric.  Consists of a:

    * body: The text or json returned from Fabric.
    * status_code: The status code returned by the HTTP Response
    * method: The method used to make the HTTP Request

    Takes an option responseNotJson to just read the content.

    * Raises a `ValueError` if a non 204 status code's.
    * Raises a `FabricException` if 'error' appears in the response text and a 4xx or 5xx status code is returned.
    * Raises a `requests.RequestException` if 'error' does not appear in
    the response text and a 4xx or 5xx status code is returned.

    """

    def __init__(self, response:requests.Response, **kwargs):
        super().__init__()
        self.body = None
        self.status_code = response.status_code
        self.method = response.request.method
        self.is_successful = 200 <= response.status_code < 400
        self.is_accepted = response.status_code == 202
        self.is_created = response.status_code == 201
        self.headers = response.headers
        self.next_location = response.headers["Location"] if "Location" in response.headers else None
        self.retry_after = response.headers["Retry-After"] if "Retry-After" in response.headers else None
        try:
            response.raise_for_status()
            if response.status_code != 204 and response.text and response.text != "":
                if "responseNotJson" in kwargs and kwargs["responseNotJson"]:
                    self.body = response.content
                else:
                    self.body = json.loads(response.text)
        except json.JSONDecodeError:
            raise ValueError("Error in parsing: {}".format(response.text))
        except requests.RequestException:
            if "error" in response.text:
                raise FabricException(response.text)
            else:
                raise requests.RequestException(response.text)
            

    def __str__(self) -> str:
        return json.dumps(self.body, indent=2)
        
        

class FabricPagedResponse(FabricResponse):
    items: List[dict]
    """
    Interface for a response from Fabric that have an iterative
    list of objects.  Consists of a:

    * items: The json returned from Fabric. Contains only the items in a list.
    * body: The text or json returned from Fabric.
    * status_code: The status code returned by the HTTP Response
    * method: The method used to make the HTTP Request

    Takes an option responseNotJson to just read the content.

    * Raises a `ValueError` if a non 204 status code's.
    * Raises a `FabricException` if 'error' appears in the response text and a 4xx or 5xx status code is returned.
    * Raises a `requests.RequestException` if 'error' does not appear in
    the response text and a 4xx or 5xx status code is returned.

    """

    def __init__(self, response: requests.Response, items_extract:Callable, **kwargs):
        super().__init__(response, **kwargs)
        self.items = items_extract(self.body)

_USER_AGENT = {"User-Agent": "needlr/{0} {1}".format(
    __version__, requests.utils.default_headers().get("User-Agent"))}

def _parse_requests_args(**kwargs):
    output = dict()
    keys = [k for k in kwargs.keys() if k.startswith("requests_")]
    for k in keys:
        output[k.split("_", 1)[1]] = kwargs.pop(k)
    return output

def _get_http(url: str, auth:_FabricAuthentication, params: dict = None, **kwargs) -> FabricResponse:
    """
    :kwargs dict headers_include:Additional headers to include.
    :kwargs List[str] headers_include:Additional headers to include.
    """
    _requests_args = _parse_requests_args(**kwargs)

    return FabricResponse(requests.get(
        url,
        params=params,
        headers=_generate_request_headers(auth, kwargs.get(
            "headers_include"), kwargs.get("headers_exclude")),
        **_requests_args
    ))

def _get_http_paged(url: str, auth:_FabricAuthentication, params: dict = dict(), 
                    items_extract:Callable = lambda x:x["data"],
                    maxResults_param_name:str = "maxResults", maxResults:int = 100,
                    continuationToken_request_name:str = "continuationToken", 
                    continuationToken_response_name:str = "continuationToken", 
                    continuationToken_in_body:bool = True,
                    **kwargs) -> Generator[FabricPagedResponse, None, None]:
    """
    Special Note: params will be overwritten by the default or kwargs provided values for
    maxResults_param_value (default 100) and maxResults_param_name (default maxResults)

    * `url: str` the URL to call and append additional paging parameters
    * `auth:_FabricAuthentication` the authentication object to get Access Tokens
    * `params: dict = dict()` a set of parameters to pass to the URL
    * `items_extract:Callable = lambda x:x["data"]` a function that can extract the list of items from the response payload
    * `maxResults_param_name:str = "maxResults"` the name of the URL parameter to limit the results returned for a given API call
    * `maxResults:int = 100` the maximum results that should be requested for a given API call
    * `continuationToken_request_name:str = "continuationToken"` the name of the URL parameter that is used to continue the list iteration from where you left off. This can be different for different APIs: e.g. `continuation`.
    * `continuationToken_response_name:str = "continuationToken"`the name of the property property that is in the response header or body. This can be different for different APIs: e.g. `x-ms-continuation`.
    * `continuationToken_in_body:bool = True` True if the continuationToken can be extracted from the response body. False i the continuationToken can be extracted from the response header.
    * `**kwargs` Catchall for additional method parameters that need to be passed in such as args for the `requests` package.
    """
    _requests_args = _parse_requests_args(**kwargs)
    
    next_url = url
    max_results_params = {maxResults_param_name: maxResults}
    params_local = params.copy()
    params_local.update(max_results_params)
    module_logger.debug(f"Get paged result for: {url} with params {str(max_results_params)}")

    iteration_count = 0
    should_continue = True

    while should_continue:
        module_logger.debug(f"Get paged result for: {url} (iteration#{iteration_count})")
        iteration_count+=1
        resp = requests.get(
            url,
            params=params_local,
            headers=_generate_request_headers(auth, kwargs.get(
                "headers_include"), kwargs.get("headers_exclude")),
            **_requests_args
        )
        # module_logger.debug(resp.headers)
        # module_logger.debug(resp.json())

        if continuationToken_in_body:
            params_local[continuationToken_request_name] = resp.json().get(continuationToken_response_name)
        else:
            params_local[continuationToken_request_name] = resp.headers.get(continuationToken_response_name)

        if params_local[continuationToken_request_name]:
            should_continue = True
            params_local[continuationToken_request_name] = unquote(params_local[continuationToken_request_name])
        else:
            should_continue = False

        
        # module_logger.debug(f'{resp.json().get("continuationUri")=}')
        module_logger.debug(f'{continuationToken_response_name=}')
        module_logger.debug(f'{params_local[continuationToken_request_name]=}')
        # next_url = url + params_local[continuationToken_request_name]
        # url = params_local[continuationToken_request_name]
        
        paged_resp = FabricPagedResponse(resp, items_extract=items_extract)

        module_logger.debug(f"Get paged result for: {url} Next URL is: {next_url}")

        yield paged_resp

def _post_http(url: str, auth:_FabricAuthentication, params: dict = None,
                json: Union[list, dict] = None, files: dict = None,
                **kwargs) -> FabricResponse:
    """
    :kwargs dict headers_include:Additional headers to include.
    :kwargs List[str] headers_include:Additional headers to include.
    :kwargs bool responseNotJson: True if the response is not expected to be JSON
    """
    # Extra Args are passed to the requests method
    extra_args = {}
    if json:
        extra_args["json"] = json
    if params:
        extra_args["params"] = params
    if files:
        extra_args["files"] = files
    response_args = {}
    _requests_args = _parse_requests_args(**kwargs)
    if "responseNotJson" in kwargs:
        response_args["responseNotJson"] = kwargs["responseNotJson"]
    return FabricResponse(
        requests.post(
            url,
            headers=_generate_request_headers(auth, kwargs.get(
                "headers_include"), kwargs.get("headers_exclude")),
            **extra_args,
            **_requests_args
        ),
        **response_args
    )

def _post_http_paged(url: str, auth:_FabricAuthentication, params: dict = dict(),
                    json: Union[list, dict] = None, files: dict = None,
                    items_extract:Callable = lambda x:x["data"],
                    maxResults_param_name:str = "maxResults", maxResults:int = 100,
                    continuationToken_request_name:str = "continuationToken", 
                    continuationToken_response_name:str = "continuationToken", 
                    continuationToken_in_body:bool = True,
                    **kwargs) -> Generator[FabricPagedResponse, None, None]:
    """
    Special Note: params will be overwritten by the default or kwargs provided values for
    maxResults_param_value (default 100) and maxResults_param_name (default maxResults)

    * `url: str` the URL to call and append additional paging parameters
    * `auth:_FabricAuthentication` the authentication object to get Access Tokens
    * `params: dict = dict()` a set of parameters to pass to the URL
    * `items_extract:Callable = lambda x:x["data"]` a function that can extract the list of items from the response payload
    * `maxResults_param_name:str = "maxResults"` the name of the URL parameter to limit the results returned for a given API call
    * `maxResults:int = 100` the maximum results that should be requested for a given API call
    * `continuationToken_request_name:str = "continuationToken"` the name of the URL parameter that is used to continue the list iteration from where you left off. This can be different for different APIs: e.g. `continuation`.
    * `continuationToken_response_name:str = "continuationToken"`the name of the property property that is in the response header or body. This can be different for different APIs: e.g. `x-ms-continuation`.
    * `continuationToken_in_body:bool = True` True if the continuationToken can be extracted from the response body. False i the continuationToken can be extracted from the response header.
    * `**kwargs` Catchall for additional method parameters that need to be passed in such as args for the `requests` package.
    """
    next_url = url
    max_results_params = {maxResults_param_name: maxResults}
    params_local = params.copy()
    params_local.update(max_results_params)

    # Extra Args are passed to the requests method
    extra_args = {}
    if json:
        extra_args["json"] = json
    if params:
        extra_args["params"] = params_local
    if files:
        extra_args["files"] = files

    _requests_args = _parse_requests_args(**kwargs)
    
    module_logger.debug(f"Get paged result for: {url} with params {str(max_results_params)}")

    iteration_count = 0
    should_continue = True

    while should_continue:
        module_logger.debug(f"Get paged result for: {url} (iteration#{iteration_count})")
        iteration_count+=1
        resp = requests.post(
            url,
            params=params_local,
            headers=_generate_request_headers(auth, kwargs.get(
                "headers_include"), kwargs.get("headers_exclude")),
            **extra_args,
            **_requests_args
        )
        # module_logger.debug(resp.headers)
        # module_logger.debug(resp.json())

        if continuationToken_in_body:
            params_local[continuationToken_request_name] = resp.json().get(continuationToken_response_name)
        else:
            params_local[continuationToken_request_name] = resp.headers.get(continuationToken_response_name)

        if params_local[continuationToken_request_name]:
            should_continue = True
        else:
            should_continue = False
        
        paged_resp = FabricPagedResponse(resp, items_extract=items_extract)

        module_logger.debug(f"Get paged result for: {url} Next URL is: {next_url}")

        yield paged_resp


def _post_http_long_running(url: str, auth:_FabricAuthentication, item: Item = None,
                    params: dict = dict(), files: dict = None, json_par: json = None,
                    wait_for_success:bool = True, 
                    retry_attempts:int = 5,
                    **kwargs) -> FabricResponse:
    """
    * `url: str` the URL to call and append additional paging parameters
    * `auth:_FabricAuthentication` the authentication object to get Access Tokens
    * `params: dict = dict()` a set of parameters to pass to the URL
    * `files: dict = None` a dictionary of files to upload
    * `fabric_item:FabricItem = FabricItem()` the FabricItem to upload
    * `wait_for_success:bool = True` True if the function should wait for the operation to complete
    * `retry_attempts:int = 5` the number of times to retry the operation before failing
    """
    if item:
        json_val = item.model_dump()
    elif json_par:
        json_val = json_par
    else:
        json_val = None
    create_op = _post_http(
        url = url,
        auth=auth,
        params=params,
        json=json_val,    
        file=files
    )

    if not wait_for_success:
        return create_op

    if create_op.is_created:
        return create_op
    
    if create_op.is_successful and create_op.status_code == 200:
        return create_op

    if create_op.is_accepted and wait_for_success:
        _completed = False
        _retry_after = int(create_op.retry_after)
        _result = {}
        for _ in range(retry_attempts):
            time.sleep(_retry_after)
            op_status = _get_http(
                url=create_op.next_location,
                auth=auth
            )
            # If it's a non-terminal state, keep going
            if op_status.body["status"] in ["NotStarted", "Running", "Undefined"]:
                _retry_after = int(op_status.retry_after)
                continue
            # Successful state, get the response from the Location header
            elif op_status.body["status"] == "Succeeded":
                _completed = True
                # If the operation is complete, but there is no location provided, then return the last requested payload.
                if op_status.next_location is None:
                    _result = op_status
                else:
                    op_results = _get_http(
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
            raise NeedlerRetriesExceeded(json.dumps({"Location":create_op.next_location, "error":"010-needlr failed to retrieve object status in set retries"}))


def _delete_http(url: str, auth:_FabricAuthentication, params: dict = None, json: Union[list, dict] = None, **kwargs) -> FabricResponse:
    """
    :kwargs dict headers_include:Additional headers to include.
    :kwargs List[str] headers_include:Additional headers to include.
    """
    extra_args = {}
    if json:
        extra_args["json"] = json
    if params:
        extra_args["params"] = params
    _requests_args = _parse_requests_args(**kwargs)
    return FabricResponse(requests.delete(
        url,
        headers=_generate_request_headers(auth, kwargs.get(
            "headers_include"), kwargs.get("headers_exclude")),
        **extra_args,
        **_requests_args
    ))

def _patch_http(url: str, auth:_FabricAuthentication, params: dict = None, json: Union[list, dict] = None,  item: Item = None,**kwargs) -> FabricResponse:
    """
    :kwargs dict headers_include:Additional headers to include.
    :kwargs List[str] headers_include:Additional headers to include.
    """
    extra_args = {}
    if json:
        extra_args["json"] = json
    if params:
        extra_args["params"] = params
    if item:
        extra_args["json"] = item.model_dump()
        
    _requests_args = _parse_requests_args(**kwargs)
    return FabricResponse(requests.patch(
        url,
        headers=_generate_request_headers(auth, kwargs.get(
            "headers_include"), kwargs.get("headers_exclude")),
        **extra_args,
        **_requests_args
    ))

def _put_http(url: str, auth:_FabricAuthentication, params: dict = None, json: Union[list, dict] = None, **kwargs) -> FabricResponse:
    """
    :kwargs dict headers_include:Additional headers to include.
    :kwargs List[str] headers_include:Additional headers to include.
    """
    extra_args = {}
    if json:
        extra_args["json"] = json
    if params:
        extra_args["params"] = params
    _requests_args = _parse_requests_args(**kwargs)
    return FabricResponse(requests.put(
        url,
        headers=_generate_request_headers(auth, kwargs.get(
            "headers_include"), kwargs.get("headers_exclude")),
        **extra_args,
        **_requests_args
    ))

def _generate_request_headers(auth:_FabricAuthentication, include: dict = {}, exclude: List[str] = []):
    auth_headers = auth.get_auth_header()

    if include:
        auth_headers.update(include)
    if exclude:
        for key in exclude:
            if key in auth_headers:
                auth_headers.pop(key)
    return dict(**auth_headers, **_USER_AGENT)

class NeedlerRetriesExceeded(Exception):
    pass