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
        matches = [  # constrict regex str to just one line
            ln for ln in lines if re.match(rf"^.* {args.remove_regex_path}$", ln)
        ]
        # remove all matches from lines
        lines = [ln for ln in lines if ln not in matches]
        # if an image was negated, strip that & add, but only if it's unique (retain original order)
        cvmfs_image_str = [s := m.lstrip("-") for m in matches if s not in matches]

    # append negations of each
    for img in cvmfs_image_str:
        lines.append(f"-{img}")
        logging.debug(f"Added line to {DOCKER_IMAGES_FILE}: {lines[-1]}")

    # write
    with open(DOCKER_IMAGES_FILE, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")
    main()
