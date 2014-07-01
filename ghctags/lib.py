import os
import pika
import json
import logging
import subprocess
from ConfigParser import SafeConfigParser

log = logging.getLogger(__name__)


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)4.4s %(filename)20.20s:%(lineno)-4s %(message)s"
    )


def get_connection():
    cp = SafeConfigParser()
    cp.read("production.ini")
    credentials = pika.PlainCredentials(
        cp.get("app:main", "rmq.username"),
        cp.get("app:main", "rmq.password")
    )
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', virtual_host="/ghctags", credentials=credentials))
    return connection


class LookupResult(object):
    def __init__(self, filename, linenum):
        self.filename = filename
        self.line_number = linenum


class LookupResults(list):
    def __init__(self, status, locations=None):
        self.status = status
        if locations:
            self.extend(locations)


class RepoMeta(object):
    def __init__(self, username, reponame):
        self.username = username
        self.reponame = reponame
        self.repo_host = "https://github.com/%s/%s.git" % (username, reponame)
        self.data_base = os.path.join("data", username, reponame)
        self.repo_base = self.data_base + ".repo"
        self.tags_file = self.data_base + ".ctags"

    def lookup(self, symbol_to_find):
        log.info("%s/%s: Looking up %s" % (self.username, self.reponame, symbol_to_find))
        if os.path.exists(self.tags_file):
            locs = []
            for line in file(self.tags_file):
                try:
                    parts = line.split("\t")
                    symbol, filename, excmd = parts[:3]
                    if symbol == symbol_to_find:
                        filename = filename.replace(self.repo_base+"/", "")
                        line_num = excmd.split(";")[0]
                        locs.append(LookupResult(filename, int(line_num)))
                except ValueError:
                    pass
            log.info("%s/%s: %d results found" % (self.username, self.reponame, len(locs)))
            return LookupResults("ok", locs)
        else:
            log.info("%s/%s: Repo not found" % (self.username, self.reponame))
            return LookupResults("no repo")

    def queue_for_update(self):
        connection = get_connection()
        channel = connection.channel()
        body = json.dumps({
            "username": self.username,
            "reponame": self.reponame,
        })
        channel.basic_publish(
            exchange='',
            routing_key='repos-to-fetch',
            body=body,
            properties=pika.BasicProperties(
                content_type="text/json",
                delivery_mode=2,  # make message persistent
            )
        )
        connection.close()
