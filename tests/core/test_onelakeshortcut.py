from needlr import FabricClient
from needlr.models.workspace import Workspace
from needlr.models.item import Item
from needlr.models.onelakeshortcut import OneLakeShortcut, OneLakeShortcutConflictPolicy, OneLakeShortcutTarget, OneLakeShortcutTarget_OneLake

class TestOneLakeShortcutLifeCycle:
    def test_shortcut_create(self, fc: FabricClient, workspace_test: Workspace, testParameters: dict[str, str]):
        policy = OneLakeShortcutConflictPolicy.Abort
        target = OneLakeShortcutTarget_OneLake( itemId =  testParameters['shortcut_source_lakehouse_id'], 
                                                path = testParameters['shortcut_source_path'], 
                                                workspaceId =  testParameters['shortcut_source_workspace_id'])
        sh = fc.onelakeshortcut.create( workspace_id= workspace_test.id, 
                                        itemId = item.id,    # <<<--- This neds to receive Shortcut as a Test !!!! Waiting on Will to PR my Shortcut library
                                        display_name= testParameters['shortcut_name'],  
                                        path = testParameters['shortcut_path'], 
                                        target = target, 
                                        shortcutConflictPolicy = policy)
        assert OneLakeShortcutTarget(sh) is not None