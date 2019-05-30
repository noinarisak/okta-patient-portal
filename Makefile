.DEFAULT_GOAL := help

.PHONY: clean-pyc
clean-pyc: ## Remove Python file artifacts
	@echo "+ $@"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: clean
clean: clean-pyc ## Remove all file artifacts

.PHONY: lint
lint: ## Check code style with flake8
	@echo "+ $@"
	@docker-compose run web flake8 project

.PHONY: test
test: ## Run tests quickly with the default Python
	@echo "+ $@"
	@docker-compose run web python manage.py test

.PHONY: coverage
coverage: ## Check code coverage quickly with the default Python
	@echo "+ $@"
	@docker-compose run web python manage.py cov

.PHONY: run
run: ## Build application stack
	@echo "+ $@"
	@docker-compose up -d --build

.PHONY: rebuild
rebuild: run logs ## Rebuild containized application stack and tail logs
	@echo "+ $@"

.PHONY: logs
logs: ## Stdout logs
	@echo "+ $@"
	@docker-compose logs --follow

.PHONY: stop
stop: ## Stop running application stack
	@echo "+ $@"
	@docker-compose stop

.PHONY: tty-web
tty-web: ## Interactive mode to container
	@echo "+ $@"
	@docker exec -it okta-patient-portal_web_1 bash

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'