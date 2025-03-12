# data "azurerm_client_config" "current" {}

# resource "azurerm_key_vault_access_policy" "obs-key-vault-policy" {
#   key_vault_id = azurerm_key_vault.obs-key-vault.id
#   tenant_id    = data.azurerm_client_config.current.tenant_id
#   object_id    = data.azurerm_client_config.current.object_id
#   secret_permissions = [
#     "Get",
#     "List",
#     "Set",
#   ]
#   key_permissions = [
#     "Get",
#     "Create",
#   ]
#   certificate_permissions = [
#     "Get",
#     "List",
#   ]
# }

# resource "azurerm_key_vault" "obs-key-vault" {
#   name                            = "obs-key-vault"
#   resource_group_name             = data.azurerm_resource_group.existing_rg.name
#   location                        = data.azurerm_resource_group.existing_rg.location
#   tenant_id                       = data.azurerm_client_config.current.tenant_id
#   sku_name                        = "standard"
#   enabled_for_disk_encryption     = true
#   enabled_for_deployment          = true
#   enabled_for_template_deployment = true
# }

# resource "azurerm_key_vault_secret" "shopping_app_insights_connection_string" {
#   name         = "shopping-app-insights-connection-string"
#   value        = azurerm_application_insights.shopping_app_insights.connection_string
#   key_vault_id = azurerm_key_vault.obs-key-vault.id
# }

# resource "azurerm_key_vault_secret" "voting_app_insights_connection_string" {
#   name         = "voting-app-insights-connection-string"
#   value        = azurerm_application_insights.voting_app_insights.connection_string
#   key_vault_id = azurerm_key_vault.obs-key-vault.id
# }