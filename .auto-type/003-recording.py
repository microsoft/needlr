file: samples/ds.py
line: 15
---
        fc.semanticmodel.clone(source_workspace_id=template_ws.id, 
                                    semanticmodel_id=list(fc.semanticmodel.ls(workspace_id=template_ws.id))[0].id,
                                    clone_name='AnalyticsProjectSemanticModel', 
                                    target_workspace_id=ws.id)
        fc.report.clone(source_workspace_id=template_ws.id, 
                             report_id=list(fc.report.ls(workspace_id=template_ws.id))[0].id,
                             clone_name='AnalyticsProjectReport', 
                             target_workspace_id=ws.id)