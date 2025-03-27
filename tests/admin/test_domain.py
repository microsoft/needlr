import pytest
from needlr import FabricClient
from needlr.models.domain import Domain



class TestDomain:

    def test_domain_ls(self, fc: FabricClient):
        resp = fc.domain.ls()
        assert len(list(resp)) > 0

    @pytest.mark.order(after="test_domain_ls")
    def test_domain_get(self, fc: FabricClient, domain_test:Domain, testParameters: dict[str, str]):
        testOneDomain_id = domain_test.id
        testDomain = fc.domain.get( testOneDomain_id)
        assert type(testDomain) is Domain


    @pytest.mark.order(after="test_domain_get")
    def test_domain_update(self, fc: FabricClient, domain_test: Domain, testParameters: dict[str, str]):
        domain_id = domain_test.id
        dom_display_name='new'+testParameters['domain_displayName']
        dom_description='New'+testParameters['domain_description']

        fc.domain.update(domain_id, dom_display_name, dom_description)
        testDomain = fc.domain.get( domain_id )
        assert testDomain.displayName == dom_display_name
        assert testDomain.description == dom_description

    @pytest.mark.order(after="test_domain_update")
    def test_domain_assign_workspaces_by_capacities(self, fc: FabricClient, domain_test: Domain, testParameters: dict[str, str]):
        domain_id = domain_test.id
        capList = []
        caps = fc.capacity.list_capacities()
        while True:
             try:
                 resp = next(caps)
                 capList.append(str(resp.id))
             except StopIteration:
                 break

        resp = fc.domain.assign_domain_workspaces_by_capacities( domain_id, capList )    
        assert resp.is_successful is True     

    @pytest.mark.order(after="test_domain_assign_workspaces_by_capacities")
    def test_domain_assign_workspaces_by_ids(self, fc: FabricClient, domain_test: Domain, testParameters: dict[str, str]):
        domain_id = domain_test.id
        workspaceList = []

        wkspc = fc.admin_workspaceclient.ls(state='active', type='workspace')

        while True:
                try:
                    resp = next(wkspc)
                    workspaceList.append(str(resp.id))
                except StopIteration:
                    break

        resp = fc.domain.assign_domain_workspaces_by_ids( domain_id, workspaceList )    
        assert resp.is_successful is True

    @pytest.mark.order(after="test_domain_assign_workspaces_by_ids")
    def test_domain_unassign_workspaces_by_ids(self, fc: FabricClient, domain_test: Domain, testParameters: dict[str, str]):
        domain_id = domain_test.id
        workspaceList = []

        wkspc = fc.admin_workspaceclient.ls(state='active', type='workspace')

        while True:
                try:
                    resp = next(wkspc)
                    workspaceList.append(str(resp.id))
                except StopIteration:
                    break

        resp = fc.domain.unassign_domain_workspaces_by_ids( domain_id, workspaceList )    
        assert resp.is_successful is True





    @pytest.mark.order(after="test_domain_unassign_workspaces_by_ids")
    def test_domain_list_domain_workspaces(self, fc: FabricClient, domain_test: Domain, testParameters: dict[str, str]):
        domain_id = domain_test.id
        resp = resp = fc.domain.list_domain_workspaces( domain_id )
        assert len(list(resp)) == 0


    @pytest.mark.order(after="test_domain_list_domain_workspaces")
    def test_domain_delete(self, fc: FabricClient, domain_test: Domain, testParameters: dict[str, str]):
        domain_id = domain_test.id
        resp = fc.domain.delete(domain_id)
        assert resp.is_successful is True     
        
