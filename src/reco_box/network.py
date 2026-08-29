from __future__ import annotations

from urllib.parse import urlparse

from .localization import tr


def normalize_proxy(value: str) -> str:
    candidate = value.strip()
    if not candidate:
        return ""
    if "://" not in candidate:
        candidate = f"http://{candidate}"
    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.port is None:
        raise ValueError(tr("代理地址必须是主机:端口或 HTTP/HTTPS 地址"))
    if parsed.username or parsed.password:
        raise ValueError(tr("代理地址不能包含账号密码"))
    if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
        raise ValueError(tr("代理地址不能包含路径、查询参数或片段"))
    return f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"
