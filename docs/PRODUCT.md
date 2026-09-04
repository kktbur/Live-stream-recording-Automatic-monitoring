# PRODUCT

## Purpose

Reco Box is a local Windows x64 desktop application for monitoring public
livestream rooms and recording available streams. It stores application data
and recording history locally and does not require a Reco Box account.

## Supported boundary

- Platform adapters use anonymous public access only.
- Room lists, recording history, and videos remain on the user's machine.
- Account cookies, login tokens, notification secrets, and credential-bearing
  proxy URLs are outside the product boundary.
- Platform support is time-sensitive. A platform marked supported or Beta does
  not guarantee every room will continue to resolve.

## Current maintenance focus

The 0.2.2 roadmap includes TLS certificate-verification hardening. PR-06 first
establishes the platform network matrix and connects Reco Box's own TwitCasting
anonymous requests to a verified-by-default policy. Other upstream paths must
be migrated and validated platform by platform before Issue #1 is closed.
