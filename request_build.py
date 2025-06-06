"""Update the docker-images file with a build request."""

import argparse
import logging
import os
from pathlib import Path

from utils import valid_image_tag


def main() -> None:
    """Main."""
    parser = argparse.ArgumentParser(
        description=f"Update {os.environ['DOCKER_IMAGES_FILE']} to build image(s)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--docker-tag",
        required=True,
        type=valid_image_tag,
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

    # assemble line for the docker-images file
    # TAG  = "icecube/skymap_scanner:3"
    # LINE = "docker://icecube/skymap_scanner:3 realtime/skymap_scanner:3"
    cvmfs_image_str = f"docker://{args.docker_tag} {args.dest_dir / args.docker_tag}"

    # read
    with open(os.environ["DOCKER_IMAGES_FILE"], "r") as f:
        lines = [ln.strip() for ln in f.readlines()]  # remove each trailing '\n'
        lines = [ln for ln in lines if ln]  # remove empty lines
        # remove all variations of `cvmfs_image_str`
        lines = [
            ln for ln in lines if ln not in [cvmfs_image_str, f"-{cvmfs_image_str}"]
        ]

    # append
    lines.append(cvmfs_image_str)
    logging.debug(f"Added line to {os.environ['DOCKER_IMAGES_FILE']}: {lines[-1]}")

    # write
    with open(os.environ["DOCKER_IMAGES_FILE"], "w") as f:
        for ln in lines:
            f.write(ln + "\n")


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")
    main()
