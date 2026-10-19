import ipaddress
import re
from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """
    Make sure the URL has a scheme.
    """

    url = url.strip()

    if not url:
        raise ValueError("URL cannot be empty.")

    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "https://" + url

    return url


def get_url_parts(url: str):
    """
    Parse URL into useful components.
    """

    parsed = urlparse(url)

    return parsed


def has_ip_address(hostname: str) -> bool:
    """
    Check whether hostname is an IPv4 or IPv6 address.
    """

    if not hostname:
        return False

    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def has_shortening_service(url: str) -> bool:
    """
    Detect common URL-shortening domains.
    """

    shortening_domains = {
        "bit.ly",
        "tinyurl.com",
        "goo.gl",
        "t.co",
        "is.gd",
        "ow.ly",
        "buff.ly",
        "cutt.ly",
        "rb.gy",
        "shorturl.at",
    }

    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()

    return hostname in shortening_domains


def count_subdomains(hostname: str) -> int:
    """
    Approximate number of subdomain levels.
    """

    if not hostname:
        return 0

    parts = hostname.split(".")

    if len(parts) <= 2:
        return 0

    return len(parts) - 2


def extract_url_features(url: str) -> dict:
    """
    Extract features that can be obtained directly
    from the URL itself.
    """

    url = normalize_url(url)

    parsed = urlparse(url)

    hostname = parsed.hostname or ""

    features = {}

    # 1. IP address
    features["having_ip_address"] = (
        1 if has_ip_address(hostname) else -1
    )

    # 2. URL length
    length = len(url)

    if length < 54:
        features["url_length"] = -1
    elif length <= 75:
        features["url_length"] = 0
    else:
        features["url_length"] = 1

    # 3. URL shortening service
    features["shortining_service"] = (
        1 if has_shortening_service(url) else -1
    )

    # 4. @ symbol
    features["having_at_symbol"] = (
        1 if "@" in url else -1
    )

    # 5. Double slash redirecting
    path_after_scheme = re.sub(
        r"^https?://",
        "",
        url,
        flags=re.IGNORECASE
    )

    features["double_slash_redirecting"] = (
        1 if "//" in path_after_scheme else -1
    )

    # 6. Prefix/suffix
    features["prefix_suffix"] = (
        1 if "-" in hostname else -1
    )

    # 7. Subdomain
    subdomain_count = count_subdomains(hostname)

    if subdomain_count == 0:
        features["having_sub_domain"] = -1
    elif subdomain_count == 1:
        features["having_sub_domain"] = 0
    else:
        features["having_sub_domain"] = 1

    # 8. HTTPS token
    features["https_token"] = (
        -1
        if parsed.scheme.lower() == "https"
        else 1
    )

    return features