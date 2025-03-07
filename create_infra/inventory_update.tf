# resource "local_file" "ansible_inventory" {
#   content = <<EOT
# [otel_collector_vm]
# ${azurerm_public_ip.my_terraform_public_static_ip.ip_address} ansible_user="azureadmin" ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_ssh_common_args='-o StrictHostKeyChecking=no'
# EOT

#   filename = "${path.module}/../configure_vm/inventory/hosts.ini"
#   depends_on = [ azurerm_linux_virtual_machine.my_terraform_vm ]
# }


# Create a local file with the connection string in the desired format
resource "local_file" "application_insights_connection_string" {
  content = <<EOT
APPLICATION_INSIGHTS_CONNECTION_STRING: '${split(";", azurerm_application_insights.default.connection_string)[0]}'
EOT
  filename = "${path.module}/../configure_vm/roles/flask-app/vars/vars.yml"
}