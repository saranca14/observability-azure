# Create the Azure Container Registry
resource "azurerm_container_registry" "gftotelshoppingapp" {
  name                = "gftotelshoppingapp"   # The name must be globally unique
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  location            = data.azurerm_resource_group.existing_rg.location
  sku                  = "Basic"

  admin_enabled       = true  # Enable admin access (optional)
}

# Output the ACR login server URL
output "acr_login_server" {
  value = azurerm_container_registry.gftotelshoppingapp.login_server
}