"""Utility functions."""

import re


_IMAGE_NAME = r"[a-z0-9._-]+"
_TAG_VERBATIM = r"[a-zA-Z0-9._-]+"
_TAG_PATTERN = r"[a-zA-Z0-9._\-\[\]]+"  # this one allows [ and ]

IMAGE_TAG_RE = re.compile(rf"^{_IMAGE_NAME}:{_TAG_VERBATIM}$")
IMAGE_TAG_PATTERN_RE = re.compile(rf"^{_IMAGE_NAME}:{_TAG_PATTERN}$")


def valid_image_tag(image_tag: str) -> str:
    """Return `image_tag` if it is a valid image tag.`"""
    if not IMAGE_TAG_RE.fullmatch(image_tag):
        raise ValueError(f"Invalid image tag: {image_tag}")
    return image_tag


def valid_image_tag_pattern(image_tag_pattern: str) -> str:
    """Return `image_tag_pattern` if it is a valid image tag (verbatim or pattern)."""
    if not IMAGE_TAG_PATTERN_RE.fullmatch(image_tag_pattern):
        raise ValueError(f"Invalid image tag or tag pattern: {image_tag_pattern}")
    return image_tag_pattern
