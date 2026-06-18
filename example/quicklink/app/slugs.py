"""Base62 random slug generation. See specs/decisions.md Decision 001."""
import secrets

_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LENGTH = 7


def generate_slug() -> str:
    """Return a random 7-char Base62 slug. Caller retries on the rare collision."""
    return "".join(secrets.choice(_ALPHABET) for _ in range(_LENGTH))
