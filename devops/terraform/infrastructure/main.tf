terraform {
  required_version = "> 1.0"

  required_providers {
    azapi = {
      source = "azure/azapi"
    }
    azurerm = {
      source = "hashicorp/azurerm"
    }
    random = {
      source = "hashicorp/random"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

# Get Resource Group
data "azurerm_resource_group" "existing_rg" {
  name = "monitoring-bench"
}