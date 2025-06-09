"""Utility functions."""

import re


_IMAGE_NAME = r"[a-z0-9._-]+"
_TAG_VERBATIM = r"[a-zA-Z0-9._-]+"
_TAG_PATTERN = r"[a-zA-Z0-9._\-\[\]]+"  # this one allows [ and ]

IMAGE_NAMETAG_RE = re.compile(rf"^{_IMAGE_NAME}:{_TAG_VERBATIM}$")
IMAGE_NAMETAG_PATTERN_RE = re.compile(rf"^{_IMAGE_NAME}:{_TAG_PATTERN}$")


def valid_image_nametag(image_nametag: str) -> str:
    """Return `image_nametag` if it is a valid image name w/ tag.`"""
    if not IMAGE_NAMETAG_RE.fullmatch(image_nametag):
        raise ValueError(f"Invalid image name/tag: {image_nametag}")
    return image_nametag


def valid_image_nametag_pattern(image_nametag_pattern: str) -> str:
    """Return `image_nametag_pattern` if it is a valid image tag (verbatim or pattern)."""
    if not IMAGE_NAMETAG_PATTERN_RE.fullmatch(image_nametag_pattern):
        raise ValueError(f"Invalid image tag or tag pattern: {image_nametag_pattern}")
    return image_nametag_pattern
