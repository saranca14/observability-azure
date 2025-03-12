terraform {
  backend "azurerm" {
    resource_group_name  = "monitoring-bench"
    storage_account_name = "gftoteltfstate2025"
    container_name       = "tfstatestore"
    key                  = "terraform.tfstate"
  }
}
