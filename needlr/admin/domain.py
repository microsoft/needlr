"""Module providing Admin Domain functions."""

from collections.abc import Iterator
from needlr import _http
import uuid
from needlr.auth.auth import _FabricAuthentication
from needlr.models.domain import Domain
import json
from needlr.models.item import Item, ItemType

class _DomainClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/create-domain)

    ### Coverage

    * Create Domain > create()
    

    """
    def __init__(self, auth:_FabricAuthentication, base_url):
        """
        Initializes a Domain object.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the Domain.

        """        
        self._auth = auth
        self._base_url = base_url

    def create(self, display_name: str, parentDomainId: uuid.UUID, description: str) -> Domain:
        """
        Create Domain

        This method creates a new domain in fabric.

        Args:
            description (str, optional): The description of the domain. Defaults to None.
            display_name (str): The display name of the domain.
            parentDomainId (uuid.UUID): The domain parent object ID

        Returns:
            Domain: The created Domain object.
        """
        url = "https://api.fabric.microsoft.com/v1/admin/domains/"

        body = {
            
                "displayName": display_name,
                "description": description,
                "parentDomainId": str(parentDomainId),
            }

        print("Request Body:", body)  # Log the request body for debugging

        try:
            resp = _http._post_http_long_running(
            url=url,
            auth=self._auth,
            item=Item(**body)
        )
            return Domain(**resp.body)
        except Exception as e:
            print("Error:", e)
            if hasattr(e, 'response'):
                print("Response Body:", e.response.text)


    def get(self, DomainId: uuid.UUID) -> Domain:
        """
        Get Domain

        This method get a  domain in fabric.

        Args:
            
            DomainId (uuid.UUID): The domain ID

        Returns:
            Domain: the domain information
        """
        url = "https://api.fabric.microsoft.com/v1/admin/domains/"

        resp = _http._get_http(
            url=url + DomainId,
            auth=self._auth,
            
        )
        domain = Domain(**resp.body)
        return domain
        

    def ls(self, **kwargs) -> Iterator[Domain]:
        """
        list Domain

        This method list the domains in fabric.

        Args:

        Returns:
            list of domains
        """
        #url = "https://api.fabric.microsoft.com/v1/admin/domains/"

        ''' resp = _http._get_http_paged(
            url=url,
            items_extract=lambda x:x["domains"],
            params = kwargs'''
        resp = _http._get_http_paged(
                url = f"{self._base_url}admin/domains",
                auth= self._auth,
                items_extract=lambda x:x["domains"],
            )
        
        for page in resp:
            for item in page.items:
                yield Domain(**item)                
    
    def delete(self, DomainId: uuid.UUID) -> Domain:
        """
        delete Domain

        This method delete a  domain in fabric.

        Args:
            
            DomainId (uuid.UUID): The domain ID

        Returns:
            http response
        """
        url = "https://api.fabric.microsoft.com/v1/admin/domains/"

        resp = _http._delete_http(
            url = url + DomainId,
            auth=self._auth
        )
        return resp
      
            
