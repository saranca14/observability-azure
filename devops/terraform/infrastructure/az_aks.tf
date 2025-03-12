resource "azurerm_log_analytics_workspace" "observability" {
  name                = "observability-log-analytics"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_kubernetes_cluster" "observability" {
  name                = "observability-aks"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  dns_prefix          = "observability"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_B2s"
  }

  identity {
    type = "SystemAssigned"
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

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.observability.id
}
