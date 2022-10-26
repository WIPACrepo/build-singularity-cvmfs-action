# build-singularity-cvmfs-action
GitHub Action Package for Requesting Singularity Builds on CVMFS

### Overview
A CI workflow can request to add or remove Docker-based Singularity builds on CVMFS at a specified directory/sub-directory.

### Examples

#### Minimal Example
These inputs are required.
```
- uses: WIPACrepo/
build-singularity-cvmfs-action@v##
  with:
    github_token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}  # so job can git push
    docker_tags: ${{ needs.docker.outputs.tags }}  # or similar
```

#### Full Example
See Skymap Scanner's [publish.yml](https://github.com/icecube/skymap_scanner/blob/master/.github/workflows/publish.yml)

### Under The Hood
This action adds one or more lines to the end of `WIPACrepo/cvmfs-actions/docker_tags.txt`, which triggers Singularity-image building and hosting. Optionally, a `-` prefix is attached to lines when images are requested to be removed.

For example, a line may look like, `docker://icecube/skymap_scanner:3 realtime/skymap_scanner:3` for the tag, `icecube/skymap_scanner:3` (See [full example](#full-example)). All previous occurrences of this line are removed from the `.txt` file (including those with and without the `-` (remove) prefix).