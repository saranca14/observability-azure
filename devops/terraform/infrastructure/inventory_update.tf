resource "local_file" "appinsights_secrets" {
  for_each = toset(var.namespaces)

  content = <<EOT
apiVersion: v1
kind: Secret
metadata:
  name: appinsights-secret-${each.value}
  namespace: obs
type: Opaque
stringData:
  connection-string: "${local.app_insights_map[each.value]}"
EOT

  filename = "${path.module}/../../kubernetes/common/appinsights-secret-${each.value}.yaml"
}