"""Update ./docker_images.txt with image removals based on image tag prefix and dest dir."""

import argparse
import logging

DOCKER_IMAGES_FILE = "./docker_images.txt"


def _prefix_match(full_prefix: str, line: str) -> bool:
    does_match = line.split()[-1].startswith(full_prefix)
    logging.debug(f"Checking '{line=}' against '{full_prefix=}' -> {does_match=}")
    return does_match


def main() -> None:
    """Main."""
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
        "--delete-image-tags-prefix",
        required=True,
        help="Image tag prefix to match for removal",
    )
    args = parser.parse_args()
    for arg, val in vars(args).items():
        logging.warning(f"{arg}: {val}")

    # read
    with open(DOCKER_IMAGES_FILE, "r") as f:
        in_lines = [ln.strip() for ln in f.readlines()]  # rm each trailing '\n'

    # Modify lines that start with the given prefix, ex: "realtime/my-branch-"
    full_prefix = f"{args.dest_dir}/{args.delete_image_tags_prefix}"
    out_lines = [f"-{ln}" if _prefix_match(full_prefix, ln) else ln for ln in in_lines]

    # log changed lines
    for a, b in zip(in_lines, out_lines):
        if a != b:
            logging.debug(f"Changed Line: {a} -> {b}")

    # write
    with open(DOCKER_IMAGES_FILE, "w") as f:
        f.write("\n".join(out_lines))


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")
    main()
