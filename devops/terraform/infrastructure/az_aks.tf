resource "azurerm_log_analytics_workspace" "observability" {
  name                = "observability-log-analytics"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}


# Create AKS Cluster
resource "azurerm_kubernetes_cluster" "observability" {
  name                = "observability-aks"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  dns_prefix          = "observability"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_B4ms"
  }

  identity {
    type = "SystemAssigned"  # Enable managed identity for AKS
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.observability.id
  }

  lifecycle {
    ignore_changes = [
      default_node_pool[0].upgrade_settings
    ]
  }
}

# Assign the AcrPull role to AKS Managed Identity for the ACR
# resource "azurerm_role_assignment" "aks_acr_pull" {
#   principal_id   = azurerm_kubernetes_cluster.observability.identity[0].principal_id
#   role_definition_name = "AcrPull"  # Assign the AcrPull role
#   scope           = azurerm_container_registry.gftotelshoppingapp.id
# }

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.observability.id
}
