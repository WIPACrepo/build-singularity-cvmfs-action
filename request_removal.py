"""Update ./docker_images.txt with image removals based on image tag pattern and dest dir."""

import argparse
import logging
import re

DOCKER_IMAGES_FILE = "./docker_images.txt"

TAG_PATTERN_SHA_SUFFIX = re.compile(
    r"^(?P<base>.+)-(?P<sha>[a-f0-9]+)$"
)  # Match `branch-[SHA]`


def _matches_pattern(image_pattern: str, image: str) -> bool:
    # [SHA] suffix
    if image_pattern.endswith("[SHA]"):
        match = TAG_PATTERN_SHA_SUFFIX.fullmatch(image)
        return (match is not None) and (match.group("base") == image_pattern)
    # Exact match case
    else:
        return image == image_pattern


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(
        description=(f"Update {DOCKER_IMAGES_FILE}"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--dest-dir",
        required=True,
        help="CVMFS destination directory",
    )
    parser.add_argument(
        "--delete-image-tags",
        required=True,
        help="Image tag to match (e.g., 'branch' for 'branch-[SHA]' or full tag for exact match)",
    )
    args = parser.parse_args()
    for arg, val in vars(args).items():
        logging.warning(f"{arg}: {val}")

    # Read file
    with open(DOCKER_IMAGES_FILE, "r") as f:
        in_lines = [ln.strip() for ln in f.readlines()]  # Remove trailing '\n'

    # Construct the base pattern
    image_pattern = f"{args.dest_dir}/{args.delete_image_tags}"

    # Modify lines that match the pattern
    out_lines = [
        f"-{ln}" if _matches_pattern(image_pattern, ln.split()[-1]) else ln
        for ln in in_lines
    ]

    # Log changed lines
    for a, b in zip(in_lines, out_lines):
        if a != b:
            logging.debug(f"Changed Line: {a} -> {b}")

    # Write updated file
    with open(DOCKER_IMAGES_FILE, "w") as f:
        f.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main()
