variable "username" {
  type        = string
  description = "The username for the local account that will be created on the new VM."
  default     = "azureadmin"
}

# Kubernetes cluster namespace names
variable "namespaces" {
  type    = list(string)
  default = ["shopping-app", "voting-app"]
}

variable "subscription_id" {
  type        = string
  description = "The Azure subscription ID."
}