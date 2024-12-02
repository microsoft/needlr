from typing import Generator
import pytest
from needlr import auth, FabricClient
from needlr.models.domain import Domain

@pytest.fixture(scope='session')
def domain_test(fc: FabricClient, domain_test:Domain, testParameters) -> Generator[Domain, None, None]:
    resp = fc.domain.create(display_name=testParameters['domain_name'], domain_id=testParameters['principal_id'], description=testParameters['domain_description'])
    assert resp.is_successful is True
    