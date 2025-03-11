"""Module providing Admin Domain functions."""

from collections.abc import Iterator
from needlr import _http
import uuid
from needlr.auth.auth import _FabricAuthentication
from needlr._http import FabricResponse
from needlr.models.domain import Domain
from needlr.models.item import Item

class _DomainClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/create-domain)

    ### Coverage

    * Create Domain > create()
    * Get Domain > get()
    
    * List Domains > ls()
    * Delete Domain > delete()
    * Update Domain > update()
    

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

    def create(self, display_name: str, **kwargs) -> Domain:
        """
        Creates a new Domain

        This method creates a new domain in fabric.

        Args:
            display_name (str): The display name of the domain.
            description (str, optional): The domain description. The description cannot contain more than 256 characters.
            ex:  description=Some Description
            parentDomainId (uuid.UUID, optional): The domain parent object ID.
            ex:  parentDomainId=00000000-0000-0000-0000-000000000000

        Returns:
            Domain: The created Domain object.

        Reference:
        - [Create Domain](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/create-domain?tabs=HTTP)            
        """

        body = {
            "displayName":display_name
        }

        for key, value in kwargs.items():

            if key is not None:
                if key =='description':
                    body["description"] = value

                if key == 'parentDomainId':
                    body["parentDomainId"] = value

        resp = _http._post_http_long_running(
            url = f"{self._base_url}admin/domains",
            auth=self._auth,
            item=Domain(**body)
        )
        return Domain(**resp.body) 


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
        List Domains

        Args:

        nonEmptyOnly (bool, optional): When true, only return domains that have at least one workspace containing an item. Default: false.
        nonEmptyOnly=True

        Returns:
            List of domains

        Reference:
        - [List Domains](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/list-domains?tabs=HTTP)            

        """
        m_url = f"{self._base_url}admin/domains/"

        for key, value in kwargs.items():
            if value is not None:
                m_url += f"?{key}={value}"
                break

        resp = _http._get_http_paged(
                url = m_url,
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
      
    def update(self, domain_id:str, display_name:str=None, description:str=None) -> Domain:
        """
        Updates the specified domain info.

        This method updates the display name and description of a domain identified by the given domain ID.

        Args:
            domain_id (str): The ID of the domain to update.
            display_name (str, optional): The new display name for the domain. Defaults to None.
            description (str, optional): The new description for the domain. Defaults to None.

        Returns:
            Workspace: The updated domain object.

        Raises:
            ValueError: If both display_name and description are left blank.

        Reference:
        - [Update Domain](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/update-domain?tabs=HTTP)
        """
        if ((display_name is None) and (description is None)):
            raise ValueError("display_name or description must be provided")

        body = dict()
        if display_name is not None:
            body["displayName"] = display_name
        if description is not None:
            body["description"] = description

        resp = _http._patch_http(
            url = self._base_url+f"admin/domains/{domain_id}",
            auth=self._auth,
            json=body
        )
        domain = Domain(**resp.body)
        return domain
          
