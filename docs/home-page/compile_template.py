import sys
import pathlib
import re

import numpy as np
import pygit2
from jinja2 import Environment, FileSystemLoader
import semver

here = pathlib.Path(__file__)
repo_path = here.absolute().parents[2]
repo = pygit2.Repository(repo_path)

# ==========
# globals
# ==========


here = pathlib.Path(__file__).parent.absolute()
env = Environment(loader=FileSystemLoader(str(here)))


def get_tags():
    # semver_regex = "0|[1-9]\d*\.0|[1-9]\d*\.0|[1-9]\d*?:-?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*?:\.?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]**??:\+[0-9a-zA-Z-]+?:\.[0-9a-zA-Z-]+*?$"
    semver_regex = "\d+\.\d+\.\d+.*"
    tag_pattern = re.compile(f"^refs/tags/v({semver_regex})")

    tags = [tag_pattern.fullmatch(x) for x in repo.listall_references()]
    tags_num = [semver.VersionInfo.parse(x.groups(1)[0]) for x in tags if x is not None]

    return tags_num


def get_deployed_tags():
    r"""
    if anything more complicated needed to parse the name of directory of
    deployed tags look at:
    http://
    python-semver.readthedocs.io/en/latest/usage.html#dealing-with-invalid-versions
    """
    tree = repo.revparse_single("gh-pages").tree
    tags_deployed = [e.name for e in tree if e.type == 2]

    tags_num = []
    for x in tags_deployed:
        try:
            tags_num.append(semver.VersionInfo.parse(x.groups(1)[0] + ".0"))
        except ValueError:
            pass

    return tags_num


def filter_recent_tags(time_wall, tags_num):
    wall = semver.VersionInfo.parse(time_wall)
    recent_tags_num = []
    for tag in tags_num:
        if tag >= wall:
            recent_tags_num.append(tag)
    return recent_tags_num


def tags_to_dict(tags_num):
    versions_tmp = {}
    for tag in tags_num:
        major = tag.major
        minor = tag.minor
        if major not in versions_tmp:
            versions_tmp[major] = [minor]
        else:
            versions_tmp[major].append(minor)

    versions = {}
    for major, minors in versions_tmp.items():
        versions[major] = list(np.unique(minors))

    return versions


versions = tags_to_dict(filter_recent_tags("0.0.0", get_tags()))

# ==========
# dump
# ==========

data = dict(versions=versions)
template = env.get_template(sys.argv[1])
stream = template.stream(data)
stream.dump(str(here / sys.argv[2]))
