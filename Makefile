PROJECT=url_counter

.PHONY: clean
clean:
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name __pycache__ -delete
	rm -f .coverage

.PHONY: check-black
check-black:
	@echo "==> Running black"
	@black --check --diff --line-length 120 .

.PHONY: check-isort
check-isort:
	@echo "==> Running isort"
	@isort --recursive --check-only --diff .

.PHONY: lint
lint: check-black check-isort

.PHONY: fix-black
fix-black:
	@echo "==> Fixing black"
	@black --line-length 120 .

.PHONY: fix-isort
fix-isort:
	@echo "==> Fixing isort"
	@isort .

.PHONY: check-flake8
check-flake8:
	@echo "==> Running flake8"
	@flake8 ./

.PHONY: check-mypy
check-mypy:
	@echo "==> Running mypy"
	@mypy -p $(PROJECT) --no-warn-return-any --show-error-codes

.PHONY: build-base
build-base:
	DOCKER_BUILDKIT=1 docker build \
	-t url-parser-build \
	--build-arg DOCKER_BUILDKIT=1 \
	--build-arg BUILDKIT_INLINE_CACHE=1 \
	-f docker/Dockerfile.base \
	.

.PHONY: build-test
build-test: build-base
	DOCKER_BUILDKIT=1 docker build \
	-t url-counter-test \
	--build-arg DOCKER_BUILDKIT=1 \
	--build-arg BUILDKIT_INLINE_CACHE=1 \
	-f docker/Dockerfile.test \
	--target url-counter-test \
	.


test: build-test
	@echo "==> Running tests"
	@docker-compose run --rm url-counter-test pytest tests/ --cov-config=setup.cfg
