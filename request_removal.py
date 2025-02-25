"""Update ./docker_images.txt with image removals based on image tag pattern and dest dir."""

import argparse
import logging
import re

DOCKER_IMAGES_FILE = "./docker_images.txt"

SHA_PATTERN = re.compile(r"^(?P<sha>[a-f0-9]+)$")
SHA_TOKEN = "[SHA]"


def _matches_pattern(image_pattern: str, cvmfs_image: str) -> bool:
    """Determine if a CVMFS image matches the given pattern w/ known tokens."""

    # [SHA] suffix
    if image_pattern.endswith(SHA_TOKEN):
        # Example Matches:
        # "feature-branch-[SHA]" -> Matches "feature-branch-abc123"
        # "feature-branch-[SHA]" -> Does NOT match "feature-branch-xyz-abc123"

        # w/o SHA_TOKEN suffix (ex: feature-branch-)
        base = image_pattern[: -len(SHA_TOKEN)]
        if not cvmfs_image.startswith(base):
            return False

        # the suffix of an actual image (ex: abc123 -> True; xyz-abc123 -> False)
        potential_sha = cvmfs_image[len(base) :]
        return bool(SHA_PATTERN.fullmatch(potential_sha))

    # FUTURE DEV: support additional string tokens
    # Exact match case
    else:
        return cvmfs_image == image_pattern


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
