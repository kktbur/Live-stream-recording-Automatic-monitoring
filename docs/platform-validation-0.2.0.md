# Reco Box 0.2.0 platform validation

Validation date: 2026-08-30

## Automated validation completed

- Exact-domain detection and disguised-domain rejection for all ten new platforms.
- Anonymous resolver routing for the pinned upstream functions.
- Explicit anonymous-only boundary for SOOP Global and TwitCasting.
- Stable normalized stream result handling and proxy forwarding.
- FFmpeg proxy forwarding and bundled Node.js self-check.
- Existing-platform regression suite.

## Release-gate status

The source implementation and offline tests are complete, but the 0.2.0 public
release remains blocked until every row below has a dated public test URL and
passes the four required live checks. Test URLs must be public and must not
require an account, cookie, payment, age confirmation, or access-control bypass.

| Platform | Public URL | Offline state | Live state and stream URL | Short TS record and stop/remux | Status |
| --- | --- | --- | --- | --- | --- |
| Twitch | pending | pending | pending | pending | Blocked |
| SOOP Global | pending | pending | pending | pending | Blocked |
| CHZZK | pending | pending | pending | pending | Blocked |
| TwitCasting | pending | pending | pending | pending | Blocked |
| SHOWROOM | pending | pending | pending | pending | Blocked |
| BIGO LIVE | pending | pending | pending | pending | Blocked |
| 17LIVE | pending | pending | pending | pending | Blocked |
| LiveMe | pending | pending | pending | pending | Blocked |
| Picarto | pending | pending | pending | pending | Blocked |
| Shopee Live | pending | pending | pending | pending | Blocked |

Accurate blocker: public live-room samples are time-sensitive and no complete,
currently live anonymous sample set for all ten platforms was available during
this build. A GitHub Release must not be created from this state. When the table
passes, rebuild the installer, rerun the packaged self-test, regenerate the
SHA-256 file, and publish both assets.
