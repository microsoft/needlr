"""Module providing Admin Domain functions."""

from collections.abc import Iterator
from needlr import _http
import uuid
from needlr.auth.auth import _FabricAuthentication
from needlr._http import FabricResponse
from needlr.models.domain import ( Domain, 
                            AssignDomainWorkspacesByCapacitiesRequest, 
                            UnassignDomainWorkspacesByIdsRequest,
                            AssignDomainWorkspacesByIdsRequest, 
                            DomainWorkspace, 
                            DomainWorkspaces )

#from needlr.models.item import Item

class _DomainClient():
    """

    [Reference](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/create-domain)

    ### Coverage

    * Create Domain > create()
    * Get Domain > get()
    * List Domains > ls()
    * Delete Domain > delete()
    * Update Domain > update()
    * Assign Domain Workspaces by Capacities > assign_domain_workspaces_by_capacities()
    * Assign Domain Workspaces by Id's > assign_domain_workspaces_by_ids()
    * List Domain Workspaces > list_domain_workspaces()
    

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


    def get(self, domain_id: uuid.UUID) -> Domain:
        """
        Returns the specified domain info.

        Args:
            
            domain_id (uuid.UUID): The domain ID

        Returns:
            Domain: the domain information

        Reference:
        [get Domain](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/get-domain?tabs=HTTP)            

        """
        resp = _http._get_http(
            url = f"{self._base_url}admin/domains/{domain_id}",
            auth=self._auth
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
        [List Domains](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/list-domains?tabs=HTTP)            

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
    
    def delete(self, domain_id: uuid.UUID) -> FabricResponse:
        """
        Deletes the specified domain.

        Args:
            
            domain_id (uuid.UUID): The domain ID

        Returns:
            FabricResponse

        Reference:
        [Delete Domain](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/delete-domain?tabs=HTTP)            

        """
        resp = _http._delete_http(
            url = f"{self._base_url}admin/domains/{domain_id}",
            auth=self._auth
        )
        return resp
      
    def update(self, domain_id: uuid.UUID, display_name: str=None, description: str=None) -> Domain:
        """
        Updates the specified domain info.

        This method updates the display name and description of a domain identified by the given domain ID.

        Args:
            domain_id (str): The ID of the domain to update.
            display_name (str, optional): The new display name for the domain. Defaults to None.
            description (str, optional): The new description for the domain. Defaults to None.

        Returns:
            Domain: The updated domain object.

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
          
    def assign_domain_workspaces_by_capacities( self, domain_id: uuid.UUID, capacities_ids: dict ) ->FabricResponse:
        """
        Assign all workspaces that reside on the specified capacities to the specified domain.
        Preexisting domain assignments will be overridden unless bulk reassignment is blocked by domain management tenant settings.

        Args:
            domain_id (str): The ID of the domain to assign.

        Returns:
           FabricResponse

        Raises:
            ValueError: If capacities_ids is blank.           

        Reference:
        - [Assign Domain Workspaces By Capacities](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/assign-domain-workspaces-by-capacities?tabs=HTTP)
        """

        body = dict()

        if capacities_ids is not None:
            body["capacitiesIds"] = capacities_ids
        else:
            raise ValueError("At least one capacity ID must be provided")


        resp = _http._post_http_long_running(
            url = f"{self._base_url}admin/domains/{domain_id}/assignWorkspacesByCapacities",
            auth=self._auth,
            item=AssignDomainWorkspacesByCapacitiesRequest(**body)
        )
        return resp
    
    def assign_domain_workspaces_by_ids( self, domain_id: uuid.UUID, workspace_ids: dict ) ->FabricResponse:
        """
        Assign workspaces to the specified domain by workspace ID.
        Preexisting domain assignments will be overridden unless bulk reassignment is blocked by domain management tenant settings.

        Args:
            domain_id (str): The ID of the domain to assign.
            workspace_ids (dict): A list of workspace IDs to assign to the domain.

        Returns:
            FabricResponse

        Raises:
            ValueError: If workspace_ids is blank.           

        Reference:
        - [Assign Domain Workspaces By ids](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/assign-domain-workspaces-by-ids?tabs=HTTP)
        """

        body = dict()

        if workspace_ids is not None:
            body["workspacesIds"] = workspace_ids
        else:
            raise ValueError("At least one workspace ID must be provided")


        resp = _http._post_http_long_running(
            url = f"{self._base_url}admin/domains/{domain_id}/assignWorkspaces",
            auth=self._auth,
            item=AssignDomainWorkspacesByIdsRequest(**body)
        )
        return resp


    def unassign_domain_workspaces_by_ids( self, domain_id: uuid.UUID, workspace_ids: dict ) ->FabricResponse:
        """
        Unassign workspaces from the specified domain by workspace ID.

        Args:
            domain_id (str): The ID of the domain to assign.
            workspace_ids (dict): A list of workspace IDs to unassign from the domain.

        Returns:
            FabricResponse

        Raises:
            ValueError: If workspace_ids is blank.           

        Reference:
        - [UnAssign Domain Workspaces By ids](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/unassign-domain-workspaces-by-ids?tabs=HTTP)
        """

        body = dict()

        if workspace_ids is not None:
            body["workspacesIds"] = workspace_ids
        else:
            raise ValueError("At least one workspace ID must be provided")


        resp = _http._post_http(
            url = f"{self._base_url}admin/domains/{domain_id}/unassignWorkspaces",
            auth=self._auth,
            json=body
        )
        return resp    

    def list_domain_workspaces(self, domain_id: uuid.UUID, **kwargs) -> Iterator[DomainWorkspaces]:
        """
        Returns a list of the workspaces assigned to the specified domain.

        Args:

        nonEmptyOnly (bool, optional): When true, only return domains that have at least one workspace containing an item. Default: false.
        nonEmptyOnly=True

        Returns:
            Returns a list of the workspaces assigned to the specified domain.

        Reference:
        [List Domains](https://learn.microsoft.com/en-us/rest/api/fabric/admin/domains/list-domain-workspaces?tabs=HTTP)            

        """
        m_url = f"{self._base_url}admin/domains/{domain_id}/workspaces"

        resp = _http._get_http_paged(
                url = m_url,
                auth= self._auth,
                items_extract=lambda x:x["value"],
            )

        for page in resp:
            for item in page.items:
                yield DomainWorkspace(**item) 

