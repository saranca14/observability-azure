data "azurerm_client_config" "current" {}

resource "azurerm_application_insights" "default" {
  name                = "otel-app-test"
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  location            = "West Europe"
  application_type    = "web"
}

