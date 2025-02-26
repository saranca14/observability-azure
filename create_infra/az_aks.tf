resource "azurerm_log_analytics_workspace" "aks_monitoring" {
  name                = "votingapp-log-analytics"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "votingapp-aks"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  dns_prefix          = "votingapp"

  default_node_pool {
    name       = "default"
    node_count = 3
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
      log_analytics_workspace_id  = azurerm_log_analytics_workspace.aks_monitoring.id
    }
}

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.aks_monitoring.id
}
