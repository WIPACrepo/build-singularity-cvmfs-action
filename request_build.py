"""Update ./docker_images.txt with a build request."""

import argparse
import logging
from pathlib import Path

DOCKER_IMAGES_FILE = "./docker_images.txt"


def main() -> None:
    """Main."""
    parser = argparse.ArgumentParser(
        description=f"Update {DOCKER_IMAGES_FILE}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--docker-tag",
        required=True,
        help="The docker image tag",
    )
    parser.add_argument(
        "--dest-dir",
        required=True,
        type=Path,
        help="The destination directory, eg: 'realtime', 'ewms/observation-management-service', ...",
    )

    args = parser.parse_args()
    for arg, val in vars(args).items():
        logging.warning(f"{arg}: {val}")

    # assemble line for docker_images.txt
    # TAG  = "icecube/skymap_scanner:3"
    # LINE = "docker://icecube/skymap_scanner:3 realtime/skymap_scanner:3"
    cvmfs_image_str = f"docker://{args.docker_tag} {args.dest_dir / args.docker_tag}"

    # read
    with open(DOCKER_IMAGES_FILE, "r") as f:
        lines = [ln.strip() for ln in f.readlines()]  # remove each trailing '\n'
        lines = [ln for ln in lines if ln]  # remove empty lines
        # remove all variations of `cvmfs_image_str`
        lines = [
            ln for ln in lines if ln not in [cvmfs_image_str, f"-{cvmfs_image_str}"]
        ]

    # append
    lines.append(cvmfs_image_str)
    logging.debug(f"Added line to {DOCKER_IMAGES_FILE}: {lines[-1]}")

    # write
    with open(DOCKER_IMAGES_FILE, "w") as f:
        for ln in lines:
            f.write(ln + "\n")


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")
    main()
