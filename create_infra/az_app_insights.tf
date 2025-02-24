data "azurerm_client_config" "current" {}

resource "azurerm_application_insights" "default" {
  name                = "otel-app-test"
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  location            = "West Europe"
  application_type    = "web"
}

# Azure Dashboards (Updated)
# resource "azurerm_dashboard" "default" {
#   name                = "flask-otel-dashboard"
#   resource_group_name = data.azurerm_resource_group.existing_rg.name
#   location            = data.azurerm_resource_group.existing_rg.location

#   dashboard_properties = jsonencode({
#     lenses = {
#       "0" = {
#         order = 0
#         parts = [
#           {
#             position = {
#               x      = 0
#               y      = 0
#               colSpan = 6
#               rowSpan = 6
#             }
#             metadata = {
#               inputs = [
#                 {
#                   name  = "resourceType"
#                   value = "microsoft.insights/components"
#                 },
#                 {
#                   name  = "resourceId"
#                   value = "/subscriptions/${data.azurerm_client_config.current.subscription_id}/resourceGroups/${data.azurerm_resource_group.existing_rg.name}/providers/microsoft.insights/components/${azurerm_application_insights.default.name}"
#                 }
#               ]
#               type = "Extension/AppInsights"
#               settings = {
#                 viewId = "timechart"
#                 metrics = [
#                   {
#                     name      = "requests/count"
#                     aggregation = "sum"
#                   },
#                   {
#                     name      = "dependencies/count"
#                     aggregation = "sum"
#                   }
#                 ]
#               }
#             }
#           }
#         ]
#       }
#     }
#   })
# }
