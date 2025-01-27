"""Module providing Core Job Scheduling functions."""

from collections.abc import Iterator
from needlr import _http
from needlr._http import FabricResponse
import uuid
from needlr.auth.auth import _FabricAuthentication
#from needlr._http import FabricResponse, FabricException
from needlr.models.jobscheduler import (
    ItemSchedules
)

#import json
#from pydantic import BaseModel
#import uuid

class _JobSchedulerClient():
    """

    [_JobSchedulerClient](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler)

    Methods:
    cancel_item_job_instance - Cancel an item's job instance.
    create_item_schedule - Create a new schedule for an item.
    get_item_job_instance - Get one item's job instance.
    get_item_schedule - Get an existing schedule for an item.
    list_item_job_instances - Returns a list of job instances for the specified item.
    list_item_schedules - Get scheduling settings for one specific item.
    run_on_demand_item_job - Run on-demand item job instance.
    update_item_schedule - Update an existing schedule for an item.

    """

    def __init__(self, auth: _FabricAuthentication, base_url):
        """
        Initializes a _JobSchedulerClient object.

        Args:
            auth (_FabricAuthentication): An instance of the _FabricAuthentication class.
            base_url (str): The base URL for the role.

        Returns:
            None
        """
        self._auth = auth
        self._base_url = base_url

    def list_item_schedules(self, workspace_id:uuid.UUID, item_id:uuid.UUID, job_type:str, **kwargs) -> ItemSchedules:
            """
            Get scheduling settings for one specific item.

            Args:
                **kwargs: Additional keyword arguments that can be passed to customize the request.

            Returns:
                Iterator[Workspace]: An iterator that yields Workspace objects representing each workspace.

            Reference:
            - [List Workspaces](https://learn.microsoft.com/en-us/rest/api/fabric/core/workspaces/list-workspaces?tabs=HTTP)
            """
            resp = _http._get_http(
                url = f"{self._base_url}workspaces/{workspace_id}/items/{item_id}/jobs/{job_type}/schedules",
                auth= self._auth,
                **kwargs
            )
            localBody = resp.body

            listItemsScheduleResponse = ItemSchedules(**localBody)

            return listItemsScheduleResponse

    