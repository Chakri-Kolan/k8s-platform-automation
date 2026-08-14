provider "kubernetes" {
  config_path = pathexpand(var.kubeconfig_path)
}

provider "helm" {
  kubernetes {
    config_path = pathexpand(var.kubeconfig_path)
  }
}

resource "kubernetes_namespace_v1" "app" {
  metadata {
    name = var.namespace
    labels = {
      "app.kubernetes.io/managed-by"               = "terraform"
      "pod-security.kubernetes.io/enforce"         = "restricted"
      "pod-security.kubernetes.io/enforce-version" = "latest"
    }
  }
}

resource "helm_release" "app" {
  name        = "platform-app"
  namespace   = kubernetes_namespace_v1.app.metadata[0].name
  chart       = "${path.module}/../helm/platform-app"
  atomic      = true
  timeout     = 300
  max_history = 5

  values = [file("${path.module}/../environments/${var.environment}.yaml")]
}
