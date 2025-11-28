# Authorisation via an Access Token

## Overview

* To access ODM APIs, users must provide an authorization token.
* The token defines which data can be retrieved and which operations are permitted (e.g.,
view-only vs. edit).

## Genestack API Token

* Personal access tokens provide permanent API access to a user’s data.
* Features:
    * A user can create multiple tokens.
    * Tokens can be revoked at any time.
    * Tokens are requested in the user profile or by clicking “Generate API Token” on
    the starting page.
* Use the header: `Genestack-Api-Token`.

## Identity Provider Access Token

* ODM also supports access tokens from an identity provider (e.g., Azure AD).
* Use the header: `Authorization`.
* Additional configuration is required to enable identity provider token usage.

## Important Notes

* If both tokens are provided, the identity provider access token takes precedence.
* For security and consistency, enterprise deployments should prefer identity provider
tokens where possible.
