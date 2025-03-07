# resource "azurerm_linux_virtual_machine" "my_terraform_vm" {
#   name                  = "otel-vm"
#   location              = data.azurerm_resource_group.existing_rg.location
#   resource_group_name   = data.azurerm_resource_group.existing_rg.name
#   network_interface_ids = [azurerm_network_interface.my_terraform_nic.id]
#   size                  = "Standard_DS1_v2"

#   os_disk {
#     name                 = "myOsDisk"
#     caching              = "ReadWrite"
#     storage_account_type = "Premium_LRS"
#   }

#   source_image_reference {
#     publisher = "Canonical"
#     offer     = "0001-com-ubuntu-server-jammy"
#     sku       = "22_04-lts-gen2"
#     version   = "latest"
#   }

#   computer_name  = "otel-collector"
#   admin_username = var.username

#   admin_ssh_key {
#     username   = var.username
#     public_key = azapi_resource_action.ssh_public_key_gen.output.publicKey
#   }


#   boot_diagnostics {
#     storage_account_uri = azurerm_storage_account.my_storage_account.primary_blob_endpoint
#   }
# }