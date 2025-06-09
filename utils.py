"""Utility functions."""

import dataclasses
import re


@dataclasses.dataclass
class ImageParsed:
    """Parts of the image uri/name/tag"""

    uri: str
    nametag: str


_IMAGE_NAME = r"[a-z0-9._-]+"
_TAG_VERBATIM = r"[a-zA-Z0-9._-]+"
_TAG_PATTERN = r"[a-zA-Z0-9._\-\[\]]+"  # this one allows [ and ]

IMAGE_NAMETAG_RE = re.compile(rf"^{_IMAGE_NAME}:{_TAG_VERBATIM}$")
IMAGE_NAMETAG_PATTERN_RE = re.compile(rf"^{_IMAGE_NAME}:{_TAG_PATTERN}$")


def parse_image_uri(image_uri: str) -> ImageParsed:
    """Return `ImageParsed` obj if it is a valid image uri w/ name and tag."""

    nametag = image_uri.split("/")[-1]
    if not IMAGE_NAMETAG_RE.fullmatch(nametag):
        raise ValueError(f"Invalid image name/tag ({nametag}) for uri: {image_uri}")

    return ImageParsed(image_uri, nametag)


def valid_image_nametag_pattern(image_nametag_pattern: str) -> str:
    """Return `image_nametag_pattern` if it is a valid image tag (verbatim or pattern)."""
    if not IMAGE_NAMETAG_PATTERN_RE.fullmatch(image_nametag_pattern):
        raise ValueError(f"Invalid image tag or tag pattern: {image_nametag_pattern}")
    return image_nametag_pattern
