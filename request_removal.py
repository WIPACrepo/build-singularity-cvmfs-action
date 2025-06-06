"""Update the docker-images file with image removals based on image tag pattern and dest dir."""

import argparse
import logging
import os
import re
from pathlib import Path

from utils import valid_image_tag_pattern

SHA_PATTERN = re.compile(r"^(?P<sha>[a-f0-9]+)$")
SHA_TOKEN = "[SHA]"


def _matches_pattern(image_pattern: str, image: str) -> bool:
    """Determine if a CVMFS image matches the given pattern w/ known tokens."""

    # [SHA] suffix
    if image_pattern.endswith(SHA_TOKEN):
        logging.debug(f"trying [SHA]-pattern: {image_pattern=} -> {image=}")
        # Example Matches:
        # "feature-branch-[SHA]" -> Matches "feature-branch-abc123"
        # "feature-branch-[SHA]" -> Does NOT match "feature-branch-xyz-abc123"

        # w/o SHA_TOKEN suffix (ex: feature-branch-)
        base = image_pattern[: -len(SHA_TOKEN)]
        if not image.startswith(base):
            logging.debug(f"-> no match (does not start with {base=})")
            return False

        # the suffix of an actual image (ex: abc123 -> True; xyz-abc123 -> False)
        potential_sha = image[len(base) :]
        if SHA_PATTERN.fullmatch(potential_sha):
            logging.debug(f"-> matched!")
            return True
        else:
            logging.debug(f"-> no match (does not start with {base=})")
            return False

    # FUTURE DEV: support additional string tokens
    # Exact match case
    else:
        logging.debug(f"trying exact-name match: {image_pattern=} -> {image=}")
        if image == image_pattern:
            logging.debug(f"-> matched!")
            return True
        else:
            logging.debug(f"-> no match (not equal)")
            return False


def _get_image(line: str) -> str:
    try:
        image = line.split()[-1]
    except IndexError:
        image = ""
    logging.debug(f"image: {line=} -> {image=}")
    return image


def main() -> None:
    """Main."""
    parser = argparse.ArgumentParser(
        description=f"Update {os.environ['DOCKER_IMAGES_FILE']} to remove image(s)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--dest-dir",
        required=True,
        type=Path,
        help="CVMFS destination directory",
    )
    parser.add_argument(
        "--image-tag-pattern",
        required=True,
        type=valid_image_tag_pattern,
        help="Image tag to match (e.g., 'branch' for 'branch-[SHA]' or full tag for exact match)",
    )
    args = parser.parse_args()
    for arg, val in vars(args).items():
        logging.warning(f"{arg}: {val}")

    # read
    with open(os.environ["DOCKER_IMAGES_FILE"], "r") as f:
        in_lines = [ln.strip() for ln in f.readlines()]  # Remove trailing '\n'

    # Modify lines that match the pattern
    image_pattern = f"{args.dest_dir}/{args.image_tag_pattern}"
    out_lines = [
        f"-{ln}" if _matches_pattern(image_pattern, _get_image(ln)) else ln
        for ln in in_lines
    ]

    # log changed lines
    for a, b in zip(in_lines, out_lines):
        if a != b:
            logging.debug(f"Changed Line: {a} -> {b}")

    # write
    with open(os.environ["DOCKER_IMAGES_FILE"], "w") as f:
        f.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")
    main()
