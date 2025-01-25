import pytest
from needlr import FabricClient
from needlr.models.lakehouse import Lakehouse
from needlr.models.workspace import Workspace
from needlr.models.onelakeshortcut import OneLakeShortcutType, OneLakeShortcutConflictPolicy, OneLakeShortcutTarget, OneLakeShortcutTarget_OneLake

class TestOneLakeShortcutLifeCycle:
    def test_shortcut_create(self, fc: FabricClient, workspace_test: Workspace,  lakehouse_test: Lakehouse, testParameters: dict[str, str]):
        policy = OneLakeShortcutConflictPolicy.Abort
        target_onelake = OneLakeShortcutTarget_OneLake( itemId =  testParameters['shortcut_source_lakehouse_id'], 
                                                path = testParameters['shortcut_source_path'], 
                                                workspaceId =  testParameters['shortcut_source_workspace_id'])
        target = OneLakeShortcutTarget(type=OneLakeShortcutType.OneLake, oneLake=target_onelake)
        # Create Shortcut
        sh = fc.onelakeshortcut.create( workspace_id= workspace_test.id, 
                                        itemId = lakehouse_test.id,    
                                        display_name= testParameters['shortcut_name'],  
                                        path = testParameters['shortcut_path'], 
                                        target = target, 
                                        shortcutConflictPolicy = policy)
        assert sh.is_successful

    @pytest.mark.order(after="test_shortcut_create")
    def test_shortcut_ls(self, fc: FabricClient, workspace_test: Workspace, lakehouse_test: Lakehouse):
        shl = fc.onelakeshortcut.ls(workspace_id=workspace_test.id, itemId=lakehouse_test.id)
        assert len(list(shl)) > 0

    @pytest.mark.order(after="test_shortcut_ls")
    def test_shortcut_get(self, fc: FabricClient, workspace_test: Workspace, lakehouse_test: Lakehouse, testParameters: dict[str, str]):
        shl = fc.onelakeshortcut.ls(workspace_id=workspace_test.id, itemId=lakehouse_test.id)
        shl2 = list(shl)
        sh = shl2[0]
        shdef = fc.onelakeshortcut.get(workspace_id=workspace_test.id, itemId=lakehouse_test.id, shortcut_name=sh.name, shortcut_path=sh.path)
        assert shdef is not None