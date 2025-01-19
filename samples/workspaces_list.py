# This sample demonstrates the bare bones of connecting to Fabric through
# Needlr and listing all of the workspaces they have access to.
# This is a great way to test your connectivity.

import os
from dotenv import load_dotenv
from needlr.auth import FabricServicePrincipal, FabricInteractiveAuth
from needlr import FabricClient

auth = FabricInteractiveAuth()

# If you're testing with a service principal uncomment this section

# load_dotenv()
# APP_ID=os.environ.get("APP_ID")
# TENANT_ID=os.environ.get("TENANT_ID")
# APP_SECRET=os.environ.get("APP_SECRET")
#auth = FabricServicePrincipal(APP_ID,APP_SECRET,TENANT_ID)

fc = FabricClient(auth)

for ws in fc.workspace.ls():
    print(f"{ws.name}: Id:{ws.id} Capacity:{ws.capacityId}")
    for itm in fc.workspace.item_ls(ws.id):
        print(f"\t{itm.displayName}:{itm.type}")