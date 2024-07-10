
from needlr import auth, FabricClient
from needlr.models.item import Item, ItemType
from needlr.core.workspace.role import GroupPrincipal, WorkspaceRole

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

#for _ in fr.workspace.item_ls(workspace_id='558B0068-C465-4249-895E-A3985CBE841C', type='Lakehouse'):
#    print(_)

wsname = 'TONIO_WS_TEST_1'

pr = GroupPrincipal(id="d93322d5-ba1e-4af6-8778-784c0944dd8b")
print(pr)

ws = fr.workspace.create(display_name=wsname, capacity_id='558B0068-C465-4249-895E-A3985CBE841C', description='test')
print(ws)
print(type(ws))

res = fr.workspace.role.assign(workspace_id=ws.id, principal=GroupPrincipal(id="d93322d5-ba1e-4af6-8778-784c0944dd8b"), role=WorkspaceRole.Contributor)
print(res.is_successful)

res = fr.workspace.role.ls(workspace_id=ws.id)
print(list(res))

res = fr.workspace.role.update(workspace_id=ws.id, principal=GroupPrincipal(id="d93322d5-ba1e-4af6-8778-784c0944dd8b"), role=WorkspaceRole.Member)
print(res.is_successful)

res = fr.workspace.role.delete(workspace_id=ws.id, principal=GroupPrincipal(id="d93322d5-ba1e-4af6-8778-784c0944dd8b"))
print(res.is_successful)


#wh = fr.warehouse.create(display_name='wh1', workspace_id=ws.id, description='wh1')
#print(wh)
#print(type(wh))



"""
ws2 = fr.workspace.update(workspace_id=ws.id, display_name='New'+wsname)
print(ws2)
print(type(ws2))

print(((ws for ws in fr.workspace.ls() if ws.name == 'New'+wsname).__next__()).name)

print("Before unassign")
print(fr.workspace.get(workspace_id=ws.id))

a = fr.workspace.capacity_unassign(workspace_id=ws.id)

print("After  unassign")
print(fr.workspace.get(workspace_id=ws.id))

print("After  re-assign")
a = fr.workspace.capacity_assign(workspace_id=ws.id, capacity_id='558B0068-C465-4249-895E-A3985CBE841C')
print(fr.workspace.get(workspace_id=ws.id))

for il in fr.workspace.item_ls(workspace_id=ws.id):
    print(il)

for il in fr.workspace.item_ls(workspace_id="e951d4bf-eb6b-4973-8b38-560d91ba57db", item_type=ItemType.DataPipeline):
    print(il)


print((fr.workspace.delete(workspace_id=ws.id)).is_successful)
"""