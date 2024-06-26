

from needlr import auth, FabricClient


fr = FabricClient(auth=auth.FabricInteractiveAuth(client_id='04b07795-8ddb-461a-bbee-02f9e1bf7b46'
                                                ,scopes=['https://api.fabric.microsoft.com/.default'])
                )

print(fr.workspace.ls())
for _ in fr.workspace.ls():
    print(_)





