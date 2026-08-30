# Reco Box 0.2.0 platform validation

Validation date: 2026-08-30 (Asia/Shanghai)

## Validation boundary

- Only public rooms were tested. No platform account, Cookie, password, age
  confirmation, or access-control bypass was used.
- A full pass requires anonymous resolution, a short TS recording, a clean
  FFmpeg stop, lossless MP4 remuxing, and a readable MP4 duration from ffprobe.
- Transient signed playback URLs are not committed. Reports retain only the CDN
  origin and non-sensitive recording measurements.
- All ten overseas additions remain Beta in 0.2.0. A Beta label is not a claim
  that every platform has passed a real-network recording test.

## Automated checks

- Exact-domain detection and disguised-domain rejection for all new platforms.
- Anonymous resolver routing and normalized result handling.
- Explicit anonymous-only boundaries for SOOP Global and TwitCasting.
- Proxy forwarding to platform resolution and FFmpeg.
- Bundled Node.js runtime and translation catalog self-checks.
- Regression coverage for the original platforms and recording workflow.

## Real-network results

| Platform | Public sample | Anonymous resolve | Short TS and MP4 | Status on 2026-08-30 |
| --- | --- | --- | --- | --- |
| Twitch | `https://www.twitch.tv/gaules` | Live, 5 routes | Passed: 4.03 s MP4 | Passed; room state is time-sensitive |
| SOOP Global | `https://www.sooplive.com/taenaatakpoker` | Failed before JSON parsing | Not run | Beta; official API unavailable from this network |
| CHZZK | `https://chzzk.naver.com/live/c93cdb99760bc66b6f7f4462d95307ee` | Live, 1 route | Passed: 4.02 s MP4 | Passed |
| TwitCasting | `https://twitcasting.tv/TAXFRAUDALGDLY` | Live, 3 routes | Passed once; repeat timed out | Beta; intermittent |
| SHOWROOM | `https://www.showroom-live.com/r/1126midorin` | Live, 1 route | CDN returned HTTP 403 | Beta; resolver-only success is not a recording pass |
| BIGO LIVE | `https://www.bigo.tv/id/695645820` | Live, 1 route | Passed: 20.07 s MP4 | Passed end to end |
| 17LIVE | `https://17.live/en/live/536903` | Offline sample resolved | Not run | Beta; 18+ confirmation remains outside the anonymous boundary |
| LiveMe | `https://www.liveme.com/v/17880688621118196521/index.html` | Live, 2 routes | Passed: 20.04 s MP4 | Passed end to end with the bundled Node.js runtime |
| Picarto | `https://www.picarto.tv/BooruGuru` | Live, 1 route | Passed: 4.04 s MP4 | Passed |
| Shopee Live | Current public Shopee SG/ID sessions were inspected | Official pages exposed live sessions, but the pinned resolver was rejected by dynamic platform checks | Not counted | Beta; anonymous parsing may fail because of regional and anti-abuse controls |

## Priority-platform evidence

The release decision specifically rechecked BIGO LIVE, LiveMe, and Shopee Live:

- BIGO LIVE produced a 2,694,228-byte TS and a 2,527,417-byte MP4 with a
  20.066667-second duration.
- LiveMe produced a 4,832,164-byte TS and a 4,606,697-byte MP4 with a
  20.036000-second duration on a machine using the bundled Node.js runtime.
- Shopee Live had current public samples and playable streams, but Reco Box's
  pinned anonymous resolver could not reliably obtain the session response.
  Shopee's web client uses dynamic request validation and regional delivery.
  Reimplementing that moving protection was intentionally excluded from 0.2.0.

## 0.2.0 release decision

The user-approved 0.2.0 boundary is to publish the completed internationalized
application without claiming that Shopee Live is stable. BIGO LIVE and LiveMe
are documented as real-network passes. Shopee Live and every other incomplete
or intermittent overseas adapter remain visibly marked Beta.

Future releases may improve Shopee compatibility using maintainable upstream or
officially supported mechanisms. Reco Box will not add account login, Cookie
import, or access-control bypass to make that platform appear supported.

The dated source-discovery notes remain in
[`platform-live-samples-0.2.0.md`](platform-live-samples-0.2.0.md).
