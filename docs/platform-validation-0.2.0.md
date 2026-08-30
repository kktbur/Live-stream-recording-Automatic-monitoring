# Reco Box 0.2.0 platform validation

Validation date: 2026-08-30 (Asia/Shanghai)

## Automated validation completed

- Exact-domain detection and disguised-domain rejection for all ten new platforms.
- Anonymous resolver routing for the pinned upstream functions.
- Explicit anonymous-only boundary for SOOP Global and TwitCasting.
- Stable normalized stream result handling and proxy forwarding.
- FFmpeg proxy forwarding and bundled Node.js self-check.
- Existing-platform regression suite: 66 tests passed after the live-test fixes.

## Real-network method

The live checks used only public room URLs and did not use an account, Cookie,
password, age confirmation, or access-control bypass. A platform only passes the
recording column when Reco Box resolves a live URL, pinned FFmpeg records a short
TS file, FFmpeg stops, the TS is remuxed to MP4, and ffprobe reads the MP4.

Transient signed play URLs are never written to this document or application
logs. Local validation reports retain only the CDN origin.

## Release-gate status

| Platform | Public test URL | Anonymous live resolve | Short TS and MP4 | Result on 2026-08-30 |
| --- | --- | --- | --- | --- |
| Twitch | `https://www.twitch.tv/gaules` | Live, 5 routes | Passed: 4.03 s MP4 | Passed at 10:13 CST; room state is time-sensitive |
| SOOP Global | `https://www.sooplive.com/taenaatakpoker` | Failed before JSON parsing | Not run | Blocked: official/global API response was unavailable from this network |
| CHZZK | `https://chzzk.naver.com/live/c93cdb99760bc66b6f7f4462d95307ee` | Live, 1 route | Passed: 4.02 s MP4 | Passed at 10:13 CST |
| TwitCasting | `https://twitcasting.tv/TAXFRAUDALGDLY` | Live, 3 routes | Passed once: 5.20 s MP4; a repeat later timed out | Unstable; viewer headers were fixed, but repeated stop/record stability is not yet sufficient |
| SHOWROOM | `https://www.showroom-live.com/r/1126midorin` | Live, 1 route | Failed | Blocked: CDN returned HTTP 403 to FFmpeg; resolver-only success is not counted |
| BIGO LIVE | `https://www.bigo.tv/id/ap_ap` and `/id/pwxwb` | Both offline when tested | Not run | Blocked: no current public live sample remained available |
| 17LIVE | `https://17.live/en/live/536903` | Offline sample resolved | Not run | Blocked: public web entry requires an 18+ birthday confirmation, outside the anonymous test boundary |
| LiveMe | No valid fixed live-room URL | Upstream returned incomplete room data for the homepage | Not run | Blocked: official anonymous homepage did not expose the fixed live ID required by the pinned resolver |
| Picarto | `https://www.picarto.tv/BooruGuru` | Live, 1 route | Passed: 4.04 s MP4 | Passed at 10:15 CST |
| Shopee Live | historical Singapore session `953420` | Failed before JSON parsing | Not run | Blocked: session expired or was region-rejected; a historical session is not a live sample |

## Accurate conclusion

Three platforms passed the repeated end-to-end gate: Twitch, CHZZK, and Picarto.
TwitCasting completed one end-to-end recording after forwarding anonymous viewer
headers, but a later repetition timed out and therefore remains unstable. Six
platforms remain blocked by platform/network behavior or the absence of a valid
current public sample.

The source, installer pipeline, translations, and offline tests are ready, but
the agreed ten-platform live gate is not satisfied. Consequently, this state may
be pushed to `main` as truthful validation progress, but it must not be published
as a `v0.2.0` GitHub Release claiming that all ten new platforms are verified.

Before a release, refresh all public samples, repeat the unstable/blocked rows,
rebuild the installer, rerun the packaged self-test, regenerate the SHA-256 file,
and then publish both release assets.

The dated sample-discovery evidence and official-source links are recorded in
[`platform-live-samples-0.2.0.md`](platform-live-samples-0.2.0.md).
