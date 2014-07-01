#!/usr/bin/env python

import sys
import logging

from ghctags.lib import configure_logging, get_connection, RepoMeta


def main(args=sys.argv):
    configure_logging()

    if len(args) == 3:
        username = sys.argv[1]
        reponame = sys.argv[2]

        repo_meta = RepoMeta(username, reponame)
        repo_meta.queue_for_update()
    else:
        print "Usage: %s [username] [reponame]" % sys.argv[0]
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
