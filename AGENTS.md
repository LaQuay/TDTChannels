# AGENTS.md

## Purpose: Pull Request validation

This repository is public.

These instructions are intended for implementing and maintaining automated Pull Request validation for TDTChannels using GitHub Actions and small supporting scripts.

The main catalog files are:

* `TELEVISION.md`
* `RADIO.md`

Contributions must follow `CONTRIBUTING.md`.

## Required reading

Before changing validation logic:

1. Read `CONTRIBUTING.md`.
2. Inspect the real structure of `TELEVISION.md` and `RADIO.md`.
3. Review representative entries and legitimate historical exceptions.
4. Check the existing workflows under `.github/workflows/`.

Do not assume the catalog is perfectly uniform and do not rewrite catalog data merely to simplify validation.

## Implementation guidelines

* Keep changes focused on Pull Request validation.
* Do not refactor unrelated files.
* Prefer small, maintainable, and testable implementations.
* Prefer the Python standard library unless a dependency clearly improves correctness.
* Add or update tests for behavioral changes.
* Run all relevant tests before finishing.
* Report repository-specific exceptions, ambiguities, and known limitations.

## Validation behavior

* Validate only added or modified catalog entries whenever possible.
* Load the full catalog only when required, such as for duplicate detection.
* Favor low false-positive rates over aggressive blocking.
* Keep deterministic validation separate from network availability checks.
* Network checks must always be advisory because GitHub-hosted runners may execute outside Spain and many streams are geo-restricted.
* Do not download video or audio segments unless explicitly requested.
* Use `GET`, follow redirects, apply short timeouts and response-size limits, and use an identifiable User-Agent.
* Do not treat `Content-Type` as definitive proof of the response format.

## GitHub Actions

* Use standard GitHub-hosted runners.
* Support Pull Requests from forks.
* Prefer workflows that require no secrets.
* Use minimum permissions.
* Do not add write permissions solely to post comments.
* Add sensible job timeouts and cancel obsolete runs where appropriate.
* Do not add automatic approval or automatic merge.

## Public repository and secrets

Treat repository files, Git history, Pull Requests, workflow logs, fixtures, artifacts, and comments as publicly visible.

* Never commit, generate, paste, or expose credentials, tokens, passwords, API keys, private keys, cookies, signed URLs, session identifiers, or other sensitive values.
* Do not print secrets, authorization headers, cookies, or environment variables in logs.
* Use clearly fake placeholders or environment-variable references in tests and examples.
* Do not commit `.env` files.
* If credentials appear to be required, stop and report the requirement instead of adding them.
* If sensitive information is discovered, do not reproduce it. Report its location and recommend revocation and removal.

## Legal and compliance boundaries

* Only use streams and sources publicly and legitimately exposed by their official broadcaster or distributor.
* Do not add or facilitate access to unauthorized, private, pirated, paywalled, or unlawfully redistributed streams.
* Do not bypass authentication, DRM, geoblocking, access controls, anti-bot protections, or other technical restrictions.
* Do not extract hidden streams, forge authorization data, reuse private tokens, or impersonate official clients.
* Flag unclear authorization or official origin for human review.

## Scope

Unless explicitly requested:

* Do not add AI validation, paid APIs, or external infrastructure.
* Do not modify contributor submissions automatically.
* Do not post automatic Pull Request comments.
* Do not merge changes.
* Leave changes ready for human review.
