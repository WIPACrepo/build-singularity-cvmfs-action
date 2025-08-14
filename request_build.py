"""Update the docker-images file with a build request."""

import argparse
import logging
import os
from pathlib import Path

from utils import parse_image_uri


def main() -> None:
    """Main."""
    parser = argparse.ArgumentParser(
        description=f"Update {os.environ['DOCKER_IMAGES_FILE']} to build image(s)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--image-uri",
        dest="image",  # type is 'ImageParsed'
        required=True,
        type=parse_image_uri,
        help=(
            "The docker image uri w/ name and tag, "
            "eg: 'icecube/skymap_scanner:4.0.0', 'ghcr.io/wipacrepo/iceprod:3.0.52', ..."
        ),
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
    cvmfs_image_str = (
        # ex: docker://icecube/skymap_scanner:4.1.0 realtime/skymap_scanner:4.1.0
        f"docker://{args.image.uri.removeprefix('docker.io/')} "
        f"{args.dest_dir / args.image.nametag}"
    )

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
