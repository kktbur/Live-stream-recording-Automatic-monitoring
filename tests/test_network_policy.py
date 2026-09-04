from reco_box.domain import Platform
from reco_box.network_policy import (
    DEFAULT_NETWORK_POLICY,
    NetworkPolicy,
    TLSEndpointOverride,
)


def test_default_network_policy_verifies_https_requests() -> None:
    assert DEFAULT_NETWORK_POLICY.verify_for(
        Platform.TWITCASTING, "https://twitcasting.tv/demo"
    ) is True


def test_tls_override_matches_only_one_platform_and_exact_host() -> None:
    override = TLSEndpointOverride(
        Platform.TWITCASTING,
        "legacy.twitcasting.tv",
        "documented compatibility test placeholder",
    )
    policy = NetworkPolicy(tls_overrides=(override,))

    assert policy.verify_for(Platform.TWITCASTING, "https://legacy.twitcasting.tv/live") is False
    assert policy.verify_for(Platform.TWITCASTING, "https://api.legacy.twitcasting.tv/live") is True
    assert policy.verify_for(Platform.TWITCH, "https://legacy.twitcasting.tv/live") is True
