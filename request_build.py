"""Update ./docker_images.txt with a build request."""

import argparse
import logging
import os

DOCKER_IMAGES_FILE = "./docker_images.txt"


def main() -> None:
    """Main."""
    parser = argparse.ArgumentParser(
        description=(f"Update {DOCKER_IMAGES_FILE}"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--docker-tag",
        required=True,
        help="The docker image tag",
    )
    parser.add_argument(
        "--dest-dir",
        default="",
        help="The destination directory, eg: realtime",
    )
    parser.add_argument(
        "--remove-docker-repo",
        default=False,
        action="store_true",
        help="whether to remove the docker image's repo when inserting to CVMFS dir",
    )

    args = parser.parse_args()
    for arg, val in vars(args).items():
        logging.warning(f"{arg}: {val}")

    # TAG  = "icecube/skymap_scanner:3"
    # LINE = "docker://icecube/skymap_scanner:3 realtime/skymap_scanner:3"

    if args.remove_docker_repo:
        dest_file = args.docker_tag.split("/", maxsplit=1)[1]
    else:
        dest_file = args.docker_tag

    cvmfs_image_str = (
        f"docker://{args.docker_tag} {os.path.join(args.dest_dir,dest_file)}"
    )

    # read
    with open(DOCKER_IMAGES_FILE, "r") as f:
        lines = [ln.strip() for ln in f.readlines()]  # rm each trailing '\n'
        # remove all instances of the line
        lines = [
            ln for ln in lines if ln not in [cvmfs_image_str, f"-{cvmfs_image_str}"]
        ]

    # append
    lines.append(cvmfs_image_str)
    logging.debug(f"Added line to {DOCKER_IMAGES_FILE}: {lines[-1]}")

    # write
    with open(DOCKER_IMAGES_FILE, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")
    main()
