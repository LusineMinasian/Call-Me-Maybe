"""Token vocabulary: the real text that every token id adds to the output."""

from typing import Any

from pydantic import BaseModel

from .loading import read_json


class Vocabulary(BaseModel):
    texts: list[str | None]

    def text(self, token_id: int) -> str | None:
        if 0 <= token_id < len(self.texts):
            return self.texts[token_id]
        return None


def _byte_decoder() -> dict[str, int]:
    printable = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    decoder = {chr(code): code for code in printable}
    extra = 0
    for byte in range(256):
        if byte not in printable:
            decoder[chr(256 + extra)] = byte
            extra += 1
    return decoder


def token_to_text(token: str, decoder: dict[str, int]) -> str | None:
    try:
        raw = bytes(decoder[char] for char in token)
        return raw.decode("utf-8")
    except (KeyError, UnicodeDecodeError):
        return None


def _check_entry(path: str, token: Any, token_id: Any) -> None:
    valid_id = isinstance(token_id, int) and not isinstance(token_id, bool)
    if not isinstance(token, str) or not valid_id or token_id < 0:
        raise ValueError(
            f"{path}: bad vocabulary entry {token!r}: {token_id!r}"
        )


def load_vocabulary(path: str) -> Vocabulary:
    data = read_json(path)
    if not isinstance(data, dict) or not data:
        raise ValueError(f"{path}: expected a non-empty JSON object")
    for token, token_id in data.items():
        _check_entry(path, token, token_id)
    decoder = _byte_decoder()
    texts: list[str | None] = [None] * (max(data.values()) + 1)
    for token, token_id in data.items():
        texts[token_id] = token_to_text(token, decoder)
    return Vocabulary(texts=texts)