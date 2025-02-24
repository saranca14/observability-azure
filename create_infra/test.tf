# # Create Virtual Network
# resource "azurerm_virtual_network" "otel-vnet" {
#   name                = "otel-vnet"
#   address_space       = ["10.0.0.0/16"]
#   location            = data.azurerm_resource_group.existing_rg.location
#   resource_group_name = data.azurerm_resource_group.existing_rg.name
# }

# # Create Subnet
# resource "azurerm_subnet" "otel_subnet" {
#   name                 = "otel-subnet"
#   resource_group_name  = data.azurerm_resource_group.existing_rg.name
#   virtual_network_name = azurerm_virtual_network.otel-vnet.name
#   address_prefixes     = ["10.0.1.0/24"]
# }

# # Create Network Security Group
# resource "azurerm_network_security_group" "otel_nsg" {
#   name                = "otel-nsg"
#   location            = data.azurerm_resource_group.existing_rg.location
#   resource_group_name = data.azurerm_resource_group.existing_rg.name

#   security_rule {
#     name                       = "allow_ssh"
#     priority                   = 100
#     direction                  = "Inbound"
#     access                     = "Allow"
#     protocol                   = "Tcp"
#     source_port_range          = "*"
#     destination_port_range     = "22"
#     source_address_prefix      = "*"
#     destination_address_prefix = "*"
#   }

#   security_rule {
#     name                       = "allow_http"
#     priority                   = 101
#     direction                  = "Inbound"
#     access                     = "Allow"
#     protocol                   = "Tcp"
#     source_port_range          = "*"
#     destination_port_range     = "80"
#     source_address_prefix      = "*"
#     destination_address_prefix = "*"
#   }
# }

# # Associate NSG with Subnet
# resource "azurerm_subnet_network_security_group_association" "otel_nsg_assoc" {
#   subnet_id                 = azurerm_subnet.otel_subnet.id
#   network_security_group_id = azurerm_network_security_group.otel_nsg.id
# }

# # Create Network Interface
# resource "azurerm_network_interface" "otel_nw_nic" {
#   name                = "otel-nic"
#   location            = data.azurerm_resource_group.existing_rg.location
#   resource_group_name = data.azurerm_resource_group.existing_rg.name

#   ip_configuration {
#     name                          = "internal"
#     subnet_id                     = azurerm_subnet.otel_subnet.id
#     private_ip_address_allocation = "Dynamic"
#   }
# }




#########




# # Create Virtual Machine
# resource "azurerm_virtual_machine" "otel_vm" {
#   name                  = "otel-vm"
#   location              = data.azurerm_resource_group.existing_rg.location
#   resource_group_name   = data.azurerm_resource_group.existing_rg.name
#   network_interface_ids = [azurerm_network_interface.otel_nw_nic.id]
#   vm_size               = "Standard_B1s"

#   # OS Disk
#   storage_os_disk {
#     name              = "otel-os-disk"
#     caching           = "ReadWrite"
#     create_option     = "FromImage"
#     managed_disk_type = "Standard_LRS"
#   }

#   # Image Reference (Ubuntu 20.04 LTS)
#   storage_image_reference {
#     publisher = "Canonical"
#     offer     = "UbuntuServer"
#     sku       = "20_04-lts"
#     version   = "latest"
#   }

#   # OS Profile
#   os_profile {
#     computer_name  = "otel-vm"
#     admin_username = "azureuser"
#     admin_password = "gfttest123"
#   }

#   # OS Profile for SSH
#   os_profile_linux_config {
#     disable_password_authentication = false
#   }
# }

# # Output VNet and VM Details
# output "vnet_name" {
#   value = azurerm_virtual_network.otel-vnet.name
# }

# output "subnet_name" {
#   value = azurerm_subnet.otel_subnet.name
# }

# output "vm_private_ip" {
#   value = azurerm_network_interface.otel_nw_nic.private_ip_address
# }
