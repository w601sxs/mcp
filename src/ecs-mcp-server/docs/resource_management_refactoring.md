# ECS Resource Management Refactoring

This document describes the refactoring of the ECS resource management API to use a more direct approach with boto3 API operations.

## Overview

The ECS resource management API has been refactored to provide a more direct mapping to boto3 API operations. Instead of using separate handler functions for each combination of action and resource type, the new API uses a single function that takes the boto3 API operation name and parameters as input.

This approach has several benefits:
- **Simplicity**: Direct mapping to boto3 API operations without intermediate layers
- **Flexibility**: Can support any ECS API operation without adding new handler functions
- **Maintainability**: Less code to maintain as new API operations are added
- **Consistency**: Parameters are passed directly to boto3 in their expected format
- **Security**: Clear separation between read-only and write operations

## Permissions

The API now enforces permission checks for write operations:

- Operations starting with "Describe" or "List" are considered read-only and can be executed without special permissions
- All other operations (Create, Delete, Update, etc.) require WRITE permission, which is enabled by setting `ALLOW_WRITE=true` in the environment

If a write operation is attempted without the proper permission, the API will return an error:

```json
{
  "status": "error",
  "error": "Operation CreateCluster requires WRITE permission. Set ALLOW_WRITE=true in your environment to enable write operations."
}
```

## API Changes

### Old API

```python
# Old API
await ecs_resource_management(
    action="list",
    resource_type="cluster",
    identifier=None,
    filters={}
)

# Old API with identifier
await ecs_resource_management(
    action="describe",
    resource_type="service",
    identifier="my-service",
    filters={"cluster": "my-cluster"}
)
```

### New API

```python
# New API
await ecs_api_operation(
    api_operation="ListClusters",
    api_params={}
)

# New API with parameters
await ecs_api_operation(
    api_operation="DescribeServices",
    api_params={
        "cluster": "my-cluster",
        "services": ["my-service"],
        "include": ["TAGS"]
    }
)
```

## Supported Operations

The following ECS API operations are supported:

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

## Migration Guide

### Listing Resources

#### Old API
```python
# List clusters
response = await ecs_resource_management(
    action="list",
    resource_type="cluster"
)
```

#### New API
```python
# List clusters
response = await ecs_api_operation(
    api_operation="ListClusters",
    api_params={}
)
```

### Describing Resources

#### Old API
```python
# Describe a cluster
response = await ecs_resource_management(
    action="describe",
    resource_type="cluster",
    identifier="my-cluster"
)
```

#### New API
```python
# Describe a cluster
response = await ecs_api_operation(
    api_operation="DescribeClusters",
    api_params={
        "clusters": ["my-cluster"],
        "include": ["ATTACHMENTS", "SETTINGS", "STATISTICS", "TAGS"]
    }
)
```

### Filtering Resources

#### Old API
```python
# List services in a cluster
response = await ecs_resource_management(
    action="list",
    resource_type="service",
    filters={"cluster": "my-cluster"}
)
```

#### New API
```python
# List services in a cluster
response = await ecs_api_operation(
    api_operation="ListServices",
    api_params={"cluster": "my-cluster"}
)
```

### Creating Resources

#### New API (not available in old API)
```python
# Create a service
response = await ecs_api_operation(
    api_operation="CreateService",
    api_params={
        "cluster": "my-cluster",
        "serviceName": "my-service",
        "taskDefinition": "my-task-definition",
        "desiredCount": 2,
        "launchType": "FARGATE",
        "networkConfiguration": {
            "awsvpcConfiguration": {
                "subnets": ["subnet-1", "subnet-2"],
                "securityGroups": ["sg-1"],
                "assignPublicIp": "ENABLED"
            }
        }
    }
)
```

## Examples

See the `examples/ecs_api_operation_example.py` file for complete examples of using the new API.

## Testing

Unit tests for the new API are available in `tests/unit/test_resource_management_api_operation.py`.
