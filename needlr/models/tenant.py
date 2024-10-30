"""Module providing Tenant Models."""

from enum import Enum
from pydantic import BaseModel
from typing import List

class DelegatedFrom(BaseModel):
    """
    The Fabric component (workspace, capacity or domain) that the tenant setting was delegated from. Additional DelegatedFrom may be added over time.
    
    [DelegatedFrom](https://learn.microsoft.com/en-us/rest/api/fabric/admin/tenants/list-capacities-tenant-settings-overrides?tabs=HTTP#delegatedfrom)

    Capacity: string - The setting is delegated from a capacity.
    Domain: string	- The setting is delegated from a domain.
    Tenant: string - The setting is delegated from a tenant.
    
    """

    Capacity: str = None
    Domain: str = None
    Tenant: str = None

class TenantSettingPropertyType(str, Enum):
    """
    Tenant setting property type. Additional tenant setting property types may be added over time.

    [TenantSettingPropertyType](https://learn.microsoft.com/en-us/rest/api/fabric/admin/tenants/list-capacities-tenant-settings-overrides?tabs=HTTP#tenantsettingpropertytype)

    Boolean: string - A checkbox in the UI.
    Freetext: string - UI accepts any string for the text box.
    Integer: string - UI accepts only integers for the text box.
    MailEnabledSecurityGroup: string - UI accepts only email enabled security groups for the text box.
    Url: string - UI accepts only URLs for the text box.
        
    """

    Boolean = 'Boolean'
    Freetext = 'Freetext'
    Integer =   'Integer'
    MailEnabledSecurityGroup = 'MailEnabledSecurityGroup'
    Url = 'Url'

class TenantSettingProperty(BaseModel):
    """
    Tenant setting property.

    [TenantSettingProperty](https://learn.microsoft.com/en-us/rest/api/fabric/admin/tenants/list-capacities-tenant-settings-overrides?tabs=HTTP#tenantsettingproperty)

    name: string - The name of the property.
    type: TenantSettingPropertyType - The type of the property.
    value: string - The value of the property.
        
    """

    name: str = None
    type: TenantSettingPropertyType = None
    value: str = None


class TenantSettingSecurityGroup(BaseModel):
    """
    Tenant setting security group.

    [TenantSettingSecurityGroup](https://learn.microsoft.com/en-us/rest/api/fabric/admin/tenants/list-capacities-tenant-settings-overrides?tabs=HTTP#tenantsettingsecuritygroup)

    graphId: string - The graph ID of the security group.
    name: string	- The name of the security group.
        
    """

    graphId: str = None
    name: str = None    

class TenantSetting(BaseModel):
    """
    Tenant setting details.
    
    [TenantSetting](https://learn.microsoft.com/en-us/rest/api/fabric/admin/tenants/list-capacities-tenant-settings-overrides?tabs=HTTP#tenantsetting)

    canSpecifySecurityGroups: boolean - Indicates if the tenant setting is enabled for a security group. 0 - The tenant setting is enabled for the entire organization. 1 - The tenant setting is enabled for security groups.
    delegateToWorkspace: boolean	- Indicates whether the tenant setting can be delegated to a workspace admin. False - Workspace admin cannot override the tenant setting. True - Workspace admin can override the tenant setting.
    delegatedFrom: DelegatedFrom - Tenant setting delegated from tenant, capacity or domain.
    enabled: boolean - The status of the tenant setting. 0 - Disabled, 1- Enabled.
    enabledSecurityGroups: TenantSettingSecurityGroup - A list of enabled security groups.
    excludedSecurityGroups: TenantSettingSecurityGroup - A list of excluded security groups.
    properties: TenantSettingProperty - The tenant setting properties.
    settingName: string - The name of the tenant setting.
    tenantSettingGroup: string - Tenant setting group name.
    title: string - The title of the tenant setting.
    
    """

    canSpecifySecurityGroups: bool = None
    delegateToWorkspace: bool = None
    delegatedFrom: DelegatedFrom = None
    enabled: bool = None
    enabledSecurityGroups: List[TenantSettingSecurityGroup] = None
    excludedSecurityGroups: List[TenantSettingSecurityGroup] = None
    properties: List[TenantSettingProperty] = None
    settingName: str = None
    tenantSettingGroup: str = None
    title: str = None


class TenantSettingOverride(BaseModel):
    """
    A workspace, capacity or domain admin can override the tenant setting.

    [TenantSettingOverride](https://learn.microsoft.com/en-us/rest/api/fabric/admin/tenants/list-capacities-tenant-settings-overrides?tabs=HTTP#tenantsettingoverride)

    id: string - The ID of a capacity, domain or workspace.
    tenantSettings: TenantSetting[]	- A list of tenant settings.
        
    """

    id: str = None
    tenantSettings: List[TenantSetting] = None

class TenantSettingOverrides(BaseModel):
    """
    A list of tenant settings overrides

    [TenantSettingOverrides](https://learn.microsoft.com/en-us/rest/api/fabric/admin/tenants/list-capacities-tenant-settings-overrides?tabs=HTTP#tenantsettingoverrides)

    continuationToken: string - The token for the next result set batch. If there are no more records, it's removed from the response.
    continuationUri: string	- The URI of the next result set batch. If there are no more records, it's removed from the response.
    overrides: TenantSettingOverride[] - A list of tenant settings that were overridden by a workspace, capacity or domain admin.
        
    """

    continuationToken: str = None
    continuationUri: str = None
    overrides: List[TenantSettingOverride] = None    