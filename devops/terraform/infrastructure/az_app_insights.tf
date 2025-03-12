resource "azurerm_application_insights" "shopping_app_insights" {
  name                = "shopping-app-insights"
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  location            = "West Europe"
  application_type    = "web"
}

resource "azurerm_application_insights" "voting_app_insights" {
  name                = "voting-app-insights"
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  location            = "West Europe"
  application_type    = "web"
}

locals {
  app_insights_map = {
    "shopping-app" = azurerm_application_insights.shopping_app_insights.connection_string
    "voting-app"   = azurerm_application_insights.voting_app_insights.connection_string
  }
}