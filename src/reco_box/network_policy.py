from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit

from .domain import Platform


@dataclass(frozen=True, slots=True)
class TLSEndpointOverride:
    """A documented, exact-host override to the normal TLS policy."""

    platform: Platform
    hostname: str
    reason: str

    def matches(self, platform: Platform, url: str) -> bool:
        parsed = urlsplit(url)
        hostname = (parsed.hostname or "").rstrip(".").casefold()
        return self.platform is platform and hostname == self.hostname.rstrip(".").casefold()


@dataclass(frozen=True, slots=True)
class NetworkPolicy:
    """First-party network defaults used when Reco Box owns the request call."""

    tls_overrides: tuple[TLSEndpointOverride, ...] = ()

    def verify_for(self, platform: Platform, url: str) -> bool:
        """Return whether the URL should use certificate verification.

        Exceptions are exact host matches on purpose. A broad suffix or a global
        disable would make a compatibility workaround indistinguishable from a
        security regression.
        """
        return not any(
            override.matches(platform, url) for override in self.tls_overrides
        )


DEFAULT_NETWORK_POLICY = NetworkPolicy()
