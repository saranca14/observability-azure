# resource "random_pet" "ssh_key_name" {
#   prefix    = "ssh"
#   separator = ""
# }

# resource "azapi_resource_action" "ssh_public_key_gen" {
#   type        = "Microsoft.Compute/sshPublicKeys@2022-11-01"
#   resource_id = azapi_resource.ssh_public_key.id
#   action      = "generateKeyPair"
#   method      = "POST"

#   response_export_values = ["publicKey", "privateKey"]
# }

# resource "azapi_resource" "ssh_public_key" {
#   type      = "Microsoft.Compute/sshPublicKeys@2022-11-01"
#   name      = "gft_otel_key"
#   location  = data.azurerm_resource_group.existing_rg.location
#   parent_id = data.azurerm_resource_group.existing_rg.id
# }


# # Save the PRIVATE key to ~/.ssh/id_rsa
# resource "local_file" "ssh_private_key" {
#   content         = azapi_resource_action.ssh_public_key_gen.output.privateKey
#   filename        = pathexpand("~/.ssh/id_rsa")
#   file_permission = "0600" 
# }

# # Save the PUBLIC key to ~/.ssh/id_rsa.pub
# resource "local_file" "ssh_public_key" {
#   content         = azapi_resource_action.ssh_public_key_gen.output.publicKey
#   filename        = pathexpand("~/.ssh/id_rsa.pub")
#   file_permission = "0644"
# }


# output "key_data" {
#   value = azapi_resource_action.ssh_public_key_gen.output.publicKey
#   sensitive = true
# }

