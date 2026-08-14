.PHONY: test image lint render-dev render-prod terraform-check

test:
	python3 -m unittest discover -v

image:
	docker build -t platform-app:local .

lint:
	helm lint helm/platform-app

render-dev:
	helm template platform-app helm/platform-app -f environments/dev.yaml

render-prod:
	helm template platform-app helm/platform-app -f environments/prod.yaml

terraform-check:
	terraform fmt -check -recursive
	terraform -chdir=terraform init -backend=false
	terraform -chdir=terraform validate
