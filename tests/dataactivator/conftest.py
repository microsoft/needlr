import pytest
from typing import Generator
from needlr import FabricClient
from needlr.models.reflex import Reflex

@pytest.fixture(scope='session')
def reflex_test(fc: FabricClient, testParameters) -> Generator[Reflex, None, None]:
    r = fc.mlexperiment.create(workspace_id=testParameters['workspace_id'],
                                display_name=testParameters['reflex_displayName'],
                                definition=testParameters['reflex_definition'],
                                description=testParameters['reflex_description'])
    yield r