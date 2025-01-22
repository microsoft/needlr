# Needlr: A Unified SDK for Microsoft Fabric

The Needlr packages provides a unified, cross-experience Microsoft Fabric SDK. The goal of Needlr is to simplify the way you work with Fabric APIs and support deployments and automation allowing you to focus on solving your business problems.


## Quickstart
Needlr is available on [PyPi](https://pypi.org/project/needlr/) and can be installed via `pip install needlr`.

With needlr installed, you first authenticate by creating a Fabric client. You can use either [FabricInteractiveAuth](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.interactivebrowsercredential?view=azure-python) to use your personal credentials or `FabricServicePrincipal` to use a service principal (which is supported for most but not all APIs).

```python
from needlr import auth, FabricClient
from needlr.auth import FabricInteractiveAuth

fc = FabricClient(auth=auth.FabricInteractiveAuth())
for ws in fc.workspace.ls():
    print(f"{ws.name}: Id:{ws.id} Capacity:{ws.capacityId}")
```
You use Service Principals in a similar way by bringing in the app id, secret, and tenant id. Replace the strings below with your service principals information.

```python
from needlr import auth, FabricClient
from needlr.auth import FabricServicePrincipal

auth = FabricServicePrincipal("APP_ID", "APP_SECRET", "TENANT_ID")
fc = FabricClient(auth=auth)
for ws in fc.workspace.ls():
    print(f"{ws.name}: Id:{ws.id} Capacity:{ws.capacityId}")
```

Needlr supports many of the Fabric REST APIs and we appreciate contributions to help us close that gap.

Some of our best supported APIs include:

* Data Warehouse
* Data Engineering
* Real-time Intelligence

Needlr has been designed to support Fabric deployment and automation and follows a convention to make it easier to discover and connect APIs.

* List items like workspaces, tables: `fc.<item>.ls()` as in `fc.workspace.ls()`
* Create items like lakehouses, event streams: `fc.<item>.create()` as in `fs.lakehouse.create('NameOfLakehouse')`
* Delete items: `fc.<item>.delete()` as in `fc.warehouse.delete(worskspace_id, warehouse_id)`

Get started with more of our [samples](https://github.com/microsoft/needlr/tree/main/samples) and please be sure to share your ideas with us on what you need to support your Fabric deployments by creating an [issue](https://github.com/microsoft/needlr/issues).

## Additional Resources

* [Contributing](https://github.com/microsoft/needlr/blob/main/CONTRIBUTING.md) to the project
* Official [Fabric REST API](https://learn.microsoft.com/en-us/rest/api/fabric/articles/) docs