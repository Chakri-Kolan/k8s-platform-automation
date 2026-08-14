variable "namespace" {
  description = "Namespace in which to install the application."
  type        = string
  default     = "platform-app"
}

variable "environment" {
  description = "Values profile to apply (dev or prod)."
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "environment must be dev or prod."
  }
}

variable "kubeconfig_path" {
  description = "Path to the kubeconfig for an existing cluster."
  type        = string
  default     = "~/.kube/config"
}
