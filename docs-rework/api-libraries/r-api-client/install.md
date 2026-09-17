---
diataxis: how-to
tab: api-libraries
---

# Install

This guide explains how to install the ODM R API Client (`odmApi`).

## Requirements

- R

## Install dependencies

Install the required packages before installing `odmApi`:

```R
install.packages("jsonlite")
install.packages("httr")
install.packages("base64enc")
install.packages("stringi", dependencies=TRUE, INSTALL_opts = c('--no-lock'))
install.packages("stringr", dependencies=TRUE, INSTALL_opts = c('--no-lock'))
```

## Install the latest version

```R
genestackRepo <- "https://public-nexus.devops.gs.team/repository/r-releases"
install.packages("odmApi", repos = genestackRepo)
```

## Install a specific version

Use the helper function below to install a particular release:

```R
genestackRepo <- "https://public-nexus.devops.gs.team/repository/r-releases"
install_specific_version_from_nexus <- function(pkg, version = NULL) {
  pkg_name <- paste0(pkg, "_", version, ".tar.gz")
  url <- paste(genestackRepo, "src/contrib", pkg_name, sep = "/")
  install.packages(url, repos = NULL, method="libcurl")
}
odmApiVersion <- "1.57.0"
install_specific_version_from_nexus("odmApi", version = odmApiVersion)
```

## Next steps

See [Usage example](usage-example.md) for a worked example of authenticating and calling an API endpoint.
