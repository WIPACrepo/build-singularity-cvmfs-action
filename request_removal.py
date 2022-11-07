"""Update ./docker_images.txt with an/multiple image removal(s)."""

import argparse
import logging
import re

DOCKER_IMAGES_FILE = "./docker_images.txt"


def main() -> None:
    """Main."""
    parser = argparse.ArgumentParser(
        description=(f"Update {DOCKER_IMAGES_FILE}"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--remove-regex-path",
        required=True,
        help="The cvmfs directory path(s)",
    )

    args = parser.parse_args()
    for arg, val in vars(args).items():
        logging.warning(f"{arg}: {val}")

    # TAG  = "icecube/skymap_scanner:3"
    # LINE = "docker://icecube/skymap_scanner:3 realtime/skymap_scanner:3"

    # read
    with open(DOCKER_IMAGES_FILE, "r") as f:
        lines = [ln.strip() for ln in f.readlines()]  # rm each trailing '\n'

    matcher = re.compile(rf"^[^-].+ {args.remove_regex_path}$")  # compile once
    # negate any matched lines, keep the rest
    lines = [f"-{ln}" if matcher.match(ln) else ln for ln in lines]

    # write
    with open(DOCKER_IMAGES_FILE, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")
    main()
