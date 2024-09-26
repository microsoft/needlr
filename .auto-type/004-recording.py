file: samples/ds.py
line: 23
---
        fc.workspace.capacity_assign(ws.id, capacity_id=fc.workspace.get('LargeDataScienceWS').capacityId)
        fc.workspace.role.assign(ws.id, principal=row['DS_GUID'], role='Contributor')