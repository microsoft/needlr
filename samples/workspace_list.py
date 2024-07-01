
import logging 
from needlr import auth, FabricClient
from needlr.admin.item import types

fr = FabricClient(auth=auth.FabricInteractiveAuth(scopes=['https://api.fabric.microsoft.com/.default'])
                )

# print(fr.workspace.ls())
# for _ in fr.workspace.ls():
#     print(_)


# print(fr.workspace.item_ls(workspace_id='9bbbcb66-a075-407e-b0a7-9052ed2840d0'))
# for _ in fr.workspace.item_ls(workspace_id='9bbbcb66-a075-407e-b0a7-9052ed2840d0'):
#     print(_)


# for _ in fr.admin_workspace.ls():
#     print(_)

# print(fr.admin_workspace.get(workspace_id='5bd603ee-cfa8-48e3-8f7e-ceb3dc6dbfd5'))

# sh = logging.StreamHandler()
# logger_faburest = logging.getLogger('needler')
# logger_faburest.setLevel(logging.DEBUG)
# logger_faburest.addHandler(sh)

# print(fr.admin_workspace.item_ls())
# print(len([_ for _ in fr.admin_workspace.item_ls()]))
# for i, _ in enumerate(fr.admin_workspace.item_ls()):
#     print(i, _)


# for _ in fr.admin_workspace.item_ls():
#     print(_)

for _ in fr.workspace.item_ls(workspace_id='7a62aed6-4402-4c65-a23a-87541d2b6c8d', type='Lakehouse'):
    print(_)



 