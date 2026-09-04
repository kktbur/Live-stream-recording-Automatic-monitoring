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
establishes the platform network matrix; PR-07 and PR-08 migrate Bilibili and
YouTube request boundaries to verified-by-default first-party adapters. Issue #1
remains open because other upstream paths and public-sample evidence are pending.

The active reliability work begins with the 0.3.0 Resolver scheduler: bounded
concurrency, platform cooldown, jitter, and retry timing are being separated from
recording and conversion workers before the later recovery-state-machine work.
