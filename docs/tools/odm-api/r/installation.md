# Installation of generated R API Client

## Requirements

- R

## Instructions

### Install

1. Install dependencies in advance

    ```R
    install.packages("jsonlite")
    install.packages("httr")
    install.packages("base64enc")
    install.packages("stringi", dependencies=TRUE, INSTALL_opts = c('--no-lock'))
    install.packages("stringr", dependencies=TRUE, INSTALL_opts = c('--no-lock'))
    ```

2. Install the latest version:

    ```R
    genestackRepo <- "https://public-nexus.devops.gs.team/repository/r-releases"
    install.packages("odmApi", repos = genestackRepo)
    ```

3. (Optional) Install specific version:

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
