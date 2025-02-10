"""Module providing a Core job scheduler Model."""

from enum import Enum
import uuid
from pydantic import BaseModel
from typing import List, Union, Optional


class DayOfWeek(str, Enum):
    """
    [DayOfWeek](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#dayofweek)
    
    Monday - string - Monday
    Tuesday - string - Tuesday
    Wednesday - string - Wednesday
    Thursday - string - Thursday
    Friday - string - Friday
    Saturday - string - Saturday
    Sunday - string - Sunday

    """
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'
    Sunday = 'Sunday'

class CronScheduleConfig(BaseModel):
    """

    [CronScheduleConfig](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#cronscheduleconfig)

    endDateTime - string - The end time for this schedule. The end time must be later than the start time.
    interval -integer - The time interval in minutes. A number between 1 and 5270400 (10 years).
    localTimeZoneId - string - The time zone identifier registry on local computer for windows, see Default Time Zones
    startDateTime - string - The start time for this schedule. If the start time is in the past, it will trigger a job instantly.
    type string: Cron - A string represents the type of the plan. Additional planType types may be added over time

    """

    endDateTime: str = None
    interval: int = None
    localTimeZoneId: str = None
    startDateTime: str = None
    type: str = 'Cron'

class DailyScheduleConfig(BaseModel):
    """

    [DailyScheduleConfig](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#dailyscheduleconfig)

    endDateTime - string - The end time for this schedule. The end time must be later than the start time.
    localTimeZoneId - string - The time zone identifier registry on local computer for windows, see Default Time Zones
    startDateTime - string - The start time for this schedule. If the start time is in the past, it will trigger a job instantly.
    times - string[] - A list of time slots in hh:mm format, at most 100 elements are allowed.
    type string: Daily - A string represents the type of the plan. Additional planType types may be added over time

    """

    endDateTime: str = None
    localTimeZoneId: str = None
    startDateTime: str = None
    times: List[str] = None
    type: str = 'Daily'    

class WeeklyScheduleConfig(BaseModel):
    """

    [WeeklyScheduleConfig](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#weeklyscheduleconfig)

    endDateTime - string - The end time for this schedule. The end time must be later than the start time.
    localTimeZoneId - string - The time zone identifier registry on local computer for windows, see Default Time Zones
    startDateTime - string - The start time for this schedule. If the start time is in the past, it will trigger a job instantly.
    times - string[] - A list of time slots in hh:mm format, at most 100 elements are allowed.
    type string: Weekly - A string represents the type of the plan. Additional planType types may be added over time
    weekdays - DayOfWeek[] - A list of weekdays, at most seven elements are allowed.

    """

    endDateTime: str = None
    localTimeZoneId: str = None
    startDateTime: str = None
    times: List[str] = None
    type: str = 'Weekly' 
    weekdays: List[DayOfWeek] = None    

class GroupType(str, Enum):
    """
    [GroupType](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#grouptype)
    
    DistributionList - string - Principal is a distribution list.
    SecurityGroup - string - Principal is a security group.
    Unknown - string -Principal group type is unknown.

    """
    DistributionList = 'DistributionList'
    SecurityGroup = 'SecurityGroup'
    Unknown = 'Unknown'

class GroupDetails(BaseModel):
    """

    [GroupDetails](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#groupdetails)

    groupType - GroupType - The type of the group. Additional group types may be added over time.

    """

    groupType: GroupType = None

class ServicePrincipalDetails(BaseModel):
    """

    Service principal specific details. Applicable when the principal type is ServicePrincipal.

    [ServicePrincipalDetails](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#serviceprincipaldetails)

    aadAppId - string - The service principal's Microsoft Entra AppId.

    """

    aadAppId: str = None

class UserDetails(BaseModel):
    """

    User principal specific details. Applicable when the principal type is User.

    [UserDetails](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#userdetails)

    userPrincipalName - string - The user principal name.

    """

    userPrincipalName: str = None

class PrincipalType(BaseModel):
    """

    The type of the principal. Additional principal types may be added over time.

    [PrincipalType](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#principaltype)

    Group - string - Principal is a security group.
    ServicePrincipal - string - Principal is a Microsoft Entra service principal.
    ServicePrincipalProfile - string - Principal is a service principal profile.
    User - string - Principal is a Microsoft Entra user principal.  

    """

    Group: str = None
    servicePrincipal: str = None
    servicePrincipalProfile: str = None
    User: str = None

class ServicePrincipalProfileDetails(BaseModel):
    """

    Service principal profile details. Applicable when the principal type is ServicePrincipalProfile.

    [ServicePrincipalProfileDetails](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#serviceprincipalprofiledetails)

    parentPrincipal - Principal - The service principal profile's parent principal.

    """

    parentPrincipal: Optional["Principal"] = None

class Principal(BaseModel):
    """

    Represents an identity or a Microsoft Entra group.

    [Principal](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#principal)

    displayName - string - The principal's display name.
    groupDetails - GroupDetails - Group specific details. Applicable when the principal type is Group.
    id: string - The principal's ID.
    servicePrincipalDetails - ServicePrincipalDetails - Service principal specific details. Applicable when the principal type is ServicePrincipal.
    servicePrincipalProfileDetails - ServicePrincipalProfileDetails - Service principal profile details. Applicable when the principal type is ServicePrincipalProfile.
    type string: PrincipalType - The type of the principal. Additional principal types may be added over time.
    userDetails - UserDetails - User principal specific details. Applicable when the principal type is User.
    

    """

    displayName: str = None
    groupDetails: GroupDetails = None
    id: uuid.UUID = None
    servicePrincipalDetails: ServicePrincipalDetails = None
    servicePrincipalProfileDetails: ServicePrincipalProfileDetails = None
    type: str = None
    userDetails: UserDetails = None

# ServicePrincipalProfileDetails.model_rebuild()

class ServicePrincipalDetails(BaseModel):
    """

    Service principal specific details. Applicable when the principal type is ServicePrincipal.

    [ServicePrincipalDetails](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#serviceprincipaldetails)

    aadAppId - str - The service principal's Microsoft Entra AppId.

    """

    aadAppId: str = None

class ItemSchedule(BaseModel):
    """

    [ItemSchedule](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#itemschedule)

    configuration - ScheduleConfig - The actual data contains the time/weekdays of this schedule.
    createdDateTime - string - The created time stamp of this schedule in Utc.
    enabled - boolean - Whether this schedule is enabled. True - Enabled, False - Disabled.
    id - string - The schedule ID.
    owner - Principal - The user identity that created this schedule or last modified.

    """

    configuration: Union[CronScheduleConfig, DailyScheduleConfig, WeeklyScheduleConfig] = None
    #configuration: DailyScheduleConfig = None
    createdDateTime: str = None
    enabled: bool = None
    id: uuid.UUID = None
    owner: Principal = None

class ItemSchedules(BaseModel):
    """

    list of schedules for this item.

    [ItemSchedules](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/list-item-schedules?tabs=HTTP#itemschedules)

    continuationToken - string - The token for the next result set batch. If there are no more records, it's removed from the response.
    continuationUri - string - The URI of the next result set batch. If there are no more records, it's removed from the response.
    value - ItemSchedule[] - list of schedules for this item.
    
    """

    continuationToken: str = None
    continuationUri: str = None
    value: List[ItemSchedule] = None


class CreateScheduleRequest(BaseModel):
    """

    Create item schedule plan request payload.

    [CreateScheduleRequest](https://learn.microsoft.com/en-us/rest/api/fabric/core/job-scheduler/create-item-schedule?tabs=HTTP#createschedulerequest)

    configuration - ScheduleConfig -  CronScheduleConfig
                                    - DailyScheduleConfig
                                    - WeeklyScheduleConfig
    enabled - boolean - Whether this schedule is enabled. True - Enabled, False - Disabled

    
    """
    
    enabled: bool = None
    configuration: Union[CronScheduleConfig, DailyScheduleConfig, WeeklyScheduleConfig] = None
    