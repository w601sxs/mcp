# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Resource Management module for ECS MCP Server.
This module provides tools and prompts for managing ECS resources.
"""

from typing import Any, Dict

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from awslabs.ecs_mcp_server.api.resource_management import ecs_api_operation


def register_module(mcp: FastMCP) -> None:
    """Register resource management module tools and prompts with the MCP server."""

    @mcp.tool(name="ecs_resource_management", annotations=None)
    async def mcp_ecs_resource_management(
        api_operation: str = Field(
            ...,
            description="The ECS API operation to execute (CamelCase)",
        ),
        api_params: Dict[str, Any] = Field(
            ...,
            description="Dictionary of parameters to pass to the API operation",
        ),
    ) -> Dict[str, Any]:
        """
        Execute ECS API operations directly.
        
        This tool allows direct execution of ECS API operations using boto3.
        
        Supported operations:
        - CreateCapacityProvider
        - CreateCluster
        - CreateService
        - CreateTaskSet
        - DeleteAccountSetting
        - DeleteAttributes
        - DeleteCapacityProvider
        - DeleteCluster
        - DeleteService
        - DeleteTaskDefinitions
        - DeleteTaskSet
        - DeregisterContainerInstance
        - DeregisterTaskDefinition
        - DescribeCapacityProviders
        - DescribeClusters
        - DescribeContainerInstances
        - DescribeServiceDeployments
        - DescribeServiceRevisions
        - DescribeServices
        - DescribeTaskDefinition
        - DescribeTasks
        - DescribeTaskSets
        - DiscoverPollEndpoint
        - ExecuteCommand
        - GetTaskProtection
        - ListAccountSettings
        - ListAttributes
        - ListClusters
        - ListContainerInstances
        - ListServiceDeployments
        - ListServices
        - ListServicesByNamespace
        - ListTagsForResource
        - ListTaskDefinitionFamilies
        - ListTaskDefinitions
        - ListTasks
        - PutAccountSetting
        - PutAccountSettingDefault
        - PutAttributes
        - PutClusterCapacityProviders
        - RegisterContainerInstance
        - RegisterTaskDefinition
        - RunTask
        - StartTask
        - StopServiceDeployment
        - StopTask
        - SubmitAttachmentStateChanges
        - SubmitContainerStateChange
        - SubmitTaskStateChange
        - TagResource
        - UntagResource
        - UpdateCapacityProvider
        - UpdateCluster
        - UpdateClusterSettings
        - UpdateContainerAgent
        - UpdateContainerInstancesState
        - UpdateService
        - UpdateServicePrimaryTaskSet
        - UpdateTaskProtection
        - UpdateTaskSet
        
        Parameters:
            api_operation: The ECS API operation to execute (CamelCase)
            api_params: Dictionary of parameters to pass to the API operation
            
        Returns:
            Dictionary containing the API response
        """
        return await ecs_api_operation(api_operation, api_params)

    # Prompt patterns for resource management
    @mcp.prompt("list ecs resources")
    def list_ecs_resources_prompt():
        """User wants to list ECS resources"""
        return ["ecs_resource_management"]

    @mcp.prompt("show ecs clusters")
    def show_ecs_clusters_prompt():
        """User wants to see ECS clusters"""
        return ["ecs_resource_management"]

    @mcp.prompt("describe ecs service")
    def describe_ecs_service_prompt():
        """User wants to describe an ECS service"""
        return ["ecs_resource_management"]

    @mcp.prompt("view ecs tasks")
    def view_ecs_tasks_prompt():
        """User wants to view ECS tasks"""
        return ["ecs_resource_management"]

    @mcp.prompt("check task definitions")
    def check_task_definitions_prompt():
        """User wants to check ECS task definitions"""
        return ["ecs_resource_management"]

    @mcp.prompt("show running containers")
    def show_running_containers_prompt():
        """User wants to see running containers in ECS"""
        return ["ecs_resource_management"]

    @mcp.prompt("view ecs resources")
    def view_ecs_resources_prompt():
        """User wants to view ECS resources"""
        return ["ecs_resource_management"]

    @mcp.prompt("inspect ecs")
    def inspect_ecs_prompt():
        """User wants to inspect ECS resources"""
        return ["ecs_resource_management"]

    @mcp.prompt("check ecs status")
    def check_ecs_status_prompt():
        """User wants to check ECS status"""
        return ["ecs_resource_management"]
