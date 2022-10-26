"""Update ./docker_images.txt."""

import argparse
import logging
import os


def main() -> None:
    """Prep and execute Condor job.

    Make scratch directory and condor file.
    """
    parser = argparse.ArgumentParser(
        description=("Update the ./docker_images.txt"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--action",
        required=True,
        choices=["add", "remove"],
        help="What do you want to do with the docker images?",
    )
    parser.add_argument(
        "--docker-tag",
        required=True,
        help="The docker image tag",
    )
    parser.add_argument(
        "--dest-dir",
        required=True,
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
        dest_file = args.docker_tag.split("/", max_split=1)[1]
    else:
        dest_file = args.docker_tag

    cvmfs_image_str = (
        f"docker://{args.docker_tag} {os.path.join(args.dest_dir,dest_file)}"
    )
    negated = f"- {cvmfs_image_str}"

    # read
    with open("./docker_images.txt", "r") as f:
        lines = [ln.strip() for ln in f.readlines()]  # rm each trailing '\n'
        # remove all instances of the line
        lines = [ln for ln in lines if ln not in [cvmfs_image_str, negated]]

    # append
    match args.action:
        case "add":
            lines.append(cvmfs_image_str)
            logging.info(f"Append: {cvmfs_image_str}")
        case "remove":
            lines.append(negated)
            logging.info(f"Append: {negated}")
        case unknown:
            raise RuntimeError(f"Unsupported --action: {unknown}")

    # write
    with open("./docker_images.txt", "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
