# CODEMAP

## Repository map

    AGENTS.md                 Repository rules and safety boundary
    README.md                 User-facing overview and setup
    PRIVACY.md                Local-data and network privacy boundary
    SECURITY.md               Security policy
    OPEN_SOURCE_AUDIT.md      Third-party source and runtime audit
    docs/
      INDEX.md               Documentation navigation
      PRODUCT.md             Product purpose and boundary
      ACCEPTANCE.md          Maintenance acceptance rules
      CURRENT.md             Durable current state
      CODEMAP.md             This repository map
      decisions/              Durable engineering decisions
      maintenance/            Per-PR maintenance records
      platform-*.md           Platform validation and network evidence
    src/reco_box/             Application and resolver code
      bilibili.py             First-party anonymous Bilibili resolver
      youtube.py              First-party anonymous YouTube resolver
      scheduler.py            Resolver deadlines, jitter, and retry timing
      rate_limit.py           Resolver concurrency and platform cooldown limits
    tests/                    Automated regression and contract tests
      test_bilibili.py        Offline Bilibili request-boundary tests
      test_youtube.py         Offline YouTube request-boundary tests
      test_scheduler.py       Scheduler and resolver limit tests
      test_settings_controller.py  Settings persistence and monitor wiring tests
    tools/                    Verification and runtime-preparation tools
    packaging/                PyInstaller and Inno Setup inputs
    vendor/                   Pinned upstream source

## Change navigation

Start with `docs/INDEX.md`, then read the applicable maintenance record and ADR.
For network changes, read `docs/platform-network-security.md` and
`docs/agents/issue-tracker.md` before changing a platform adapter.
