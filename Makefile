# Setting SHELL to bash allows bash commands to be executed by recipes.
# Options are set to exit when a recipe line exits non-zero or a piped command fails.
SHELL = /usr/bin/env bash -o pipefail
.SHELLFLAGS = -ec

IMAGE_REGISTRY         ?= harbor.devops.gs.team
IMAGE_NAME             ?= genestack/user-docs
IMAGE_VERSION          ?= 1.0.0
IMAGE_TAG              := $(IMAGE_REGISTRY)/$(IMAGE_NAME):$(IMAGE_VERSION)
IMAGE_TAG_LATEST       := $(IMAGE_REGISTRY)/$(IMAGE_NAME):latest
IMAGE_PUSH             ?= docker
IMAGE_DEFAULT_PLATFORM := $(shell docker system info -f '{{.OSType}}/{{.Architecture}}')
IMAGE_PLATFORMS        ?= $(IMAGE_DEFAULT_PLATFORM)

ifeq ($(IMAGE_PUSH),full)
	IMAGE_BUILD_OUTPUTS := --output=type=docker --output=type=registry
else ifeq ($(IMAGE_PUSH),docker)
	IMAGE_BUILD_OUTPUTS := --output=type=docker
else ifeq ($(IMAGE_PUSH),registry)
	IMAGE_BUILD_OUTPUTS := --output=type=registry
else ifeq ($(IMAGE_PUSH),none)
	IMAGE_BUILD_OUTPUTS :=
endif

.PHONY: main
main: push

##@ General

# The help target prints out all targets with their descriptions organized
# beneath their categories. The categories are represented by '##@' and the
# target descriptions by '##'. The awk command is responsible for reading the
# entire set of makefiles included in this invocation, looking for lines of the
# file as xyz: ## something, and then pretty-format the target and help. Then,
# if there's a line with ##@ something, that gets pretty-printed as a category.
# More info on the usage of ANSI control characters for terminal formatting:
# https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_parameters
# More info on the awk command:
# http://linuxcommand.org/lc3_adv_awk.php

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Build

.PHONY: push
push: ## Build the site image, tagged IMAGE_VERSION and latest, to IMAGE_PUSH (docker, registry, full, none).
	docker buildx build \
	--platform=$(IMAGE_PLATFORMS) \
	--target=push \
	--tag=$(IMAGE_TAG) \
	--tag=$(IMAGE_TAG_LATEST) \
	$(IMAGE_BUILD_OUTPUTS) \
	.
