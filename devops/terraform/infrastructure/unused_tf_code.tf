# resource "local_file" "ansible_inventory" {
#   content = <<EOT
# [otel_collector_vm]
# ${azurerm_public_ip.my_terraform_public_static_ip.ip_address} ansible_user="azureadmin" ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_ssh_common_args='-o StrictHostKeyChecking=no'
# EOT

#   filename = "${path.module}/../configure_vm/inventory/hosts.ini"
#   depends_on = [ azurerm_linux_virtual_machine.my_terraform_vm ]
# }

# resource "local_file" "appinsights_secrets" {
#   for_each = toset(var.namespaces)

#   content = <<EOT
# apiVersion: v1
# kind: Secret
# metadata:
#   name: appinsights-secret
#   namespace: ${each.value}
# type: Opaque
# stringData:
#   connection-string: "${azurerm_application_insights.default.connection_string}"
# EOT

#   filename = "${path.module}/../k8s-deployments/common/appinsights-secret-${each.value}.yaml"
# }