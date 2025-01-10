import pytest

from typing import Generator
from needlr import auth, FabricClient
from needlr.models.domain import Domain as ds



class TestDomain:

    def test_domain_ls(self, fc: FabricClient):
        resp = fc.domain.ls()
        assert len(list(resp)) > 0

   
        
