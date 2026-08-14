# Kubernetes Platform Automation

[![CI](https://github.com/Chakri-Kolan/k8s-platform-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/Chakri-Kolan/k8s-platform-automation/actions/workflows/ci.yml)

A deployable platform-engineering reference project: a secure sample service, OCI image, reusable Helm chart, environment profiles, Terraform-managed release, Prometheus metrics, and GitHub Actions validation and publishing.

## What this demonstrates

- Production-minded Helm templating and environment promotion
- Restricted pod security, non-root containers, and NetworkPolicy
- Rolling updates, health probes, autoscaling, disruption budgets, and topology spreading
- Terraform/Helm ownership boundaries against an existing cluster
- Versioned image publishing to GitHub Container Registry with provenance and SBOM
- Automated application, container, manifest, and Terraform validation

## Repository layout

```text
app/                   dependency-free sample HTTP service
helm/platform-app/     reusable application chart
environments/          development and production values
terraform/             namespace and Helm release ownership
tests/                 application behavior tests
.github/workflows/     CI and tagged image releases
docs/                  architecture and operational decisions
```

## Run locally

```bash
python3 -m app.server
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/metrics
```

Or run the same immutable container used by Kubernetes:

```bash
docker build -t platform-app:local .
docker run --rm -p 8080:8080 platform-app:local
```

## Validate

Requirements: Python 3.12+, Docker, Helm 3, Terraform 1.6+, and optionally kubeconform.

```bash
make test
make image
make lint
make render-dev
make terraform-check
```

GitHub Actions repeats these checks for every pull request and validates rendered resources with kubeconform.

## Deploy to an existing cluster

Helm directly:

```bash
helm upgrade --install platform-app helm/platform-app \
  --namespace platform-app --create-namespace \
  -f environments/dev.yaml \
  --set image.repository=ghcr.io/chakri-kolan/platform-app \
  --set image.tag=1.0.0 \
  --atomic --wait
```

Or let Terraform own the namespace and release:

```bash
terraform -chdir=terraform init
terraform -chdir=terraform apply -var='environment=dev'
```

The repository expects a working kubeconfig and an existing cluster. It does not create cloud infrastructure or store cluster credentials in GitHub.

## Release an image

Push a semantic version tag such as `v1.0.0`. The release workflow publishes an SBOM-attested image to `ghcr.io/chakri-kolan/platform-app`. Update the environment image tag intentionally before deployment.

## Operations

```bash
kubectl -n platform-app get deploy,pods,svc,hpa,pdb
kubectl -n platform-app rollout status deploy/platform-app-platform-app
helm -n platform-app rollback platform-app
```

See [docs/architecture.md](docs/architecture.md) for ownership, availability, security, and observability decisions.

## License

MIT
