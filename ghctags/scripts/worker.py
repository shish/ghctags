#!/usr/bin/env python

import pika
import sys
import os
import json
import subprocess
import logging
import multiprocessing

from ghctags.lib import configure_logging, get_connection, RepoMeta

log = logging.getLogger(__name__)

durable_json = pika.BasicProperties(content_type="text/json", delivery_mode=2)  # make message persistent


def main_fetcher(args=sys.argv):
    configure_logging()

    def cb_fetch(ch, method, properties, raw_body):
        try:
            body = json.loads(raw_body)
            repo_meta = RepoMeta(body["username"], body["reponame"])

            log.info("%s/%s: Fetching data" % (repo_meta.username, repo_meta.reponame))

            if os.path.exists(repo_meta.repo_base):
                subprocess.call(["/usr/bin/git", "pull"], cwd=repo_meta.repo_base)
            else:
                os.makedirs(repo_meta.repo_base)
                print ["/usr/bin/git", "clone", repo_meta.repo_host, repo_meta.repo_base]
                subprocess.call(["/usr/bin/git", "clone", repo_meta.repo_host, repo_meta.repo_base])

            log.info("%s/%s: Fetched data" % (repo_meta.username, repo_meta.reponame))

            ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_publish(exchange='', routing_key='repos-to-tag', body=raw_body, properties=durable_json)
        except Exception as e:
            log.exception("Error dealing with message: %r %s", raw_body, e)

    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue='repos-to-fetch', durable=True)
    channel.queue_declare(queue='repos-to-tag', durable=True)
    channel.basic_qos(prefetch_count=1)

    log.info("Waiting for repos to fetch")
    try:
        channel.basic_consume(cb_fetch, queue='repos-to-fetch')
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()


def main_tagger(args=sys.argv):
    configure_logging()

    def cb_fetch(ch, method, properties, raw_body):
        try:
            body = json.loads(raw_body)
            repo_meta = RepoMeta(body["username"], body["reponame"])

            log.info("%s/%s: Making ctags" % (repo_meta.username, repo_meta.reponame))

            subprocess.call([
                "/usr/bin/ctags",
                "--excmd=number",
                "-o", repo_meta.tags_file,
                "--recurse=yes", repo_meta.repo_base
            ])

            log.info("%s/%s: Made ctags" % (repo_meta.username, repo_meta.reponame))

            ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_publish(exchange='', routing_key='repos-to-load', body=raw_body, properties=durable_json)
        except Exception as e:
            log.exception("Error dealing with message: %r %s", raw_body, e)

    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue='repos-to-tag', durable=True)
    channel.queue_declare(queue='repos-to-load', durable=True)
    channel.basic_qos(prefetch_count=1)

    log.info("Waiting for repos to tag")
    try:
        channel.basic_consume(cb_fetch, queue='repos-to-tag')
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()


def main_loader(args=sys.argv):
    configure_logging()

    def cb_fetch(ch, method, properties, raw_body):
        try:
            body = json.loads(raw_body)
            repo_meta = RepoMeta(body["username"], body["reponame"])

            log.info("%s/%s: Loading data" % (repo_meta.username, repo_meta.reponame))

            pass

            log.info("%s/%s: Loaded data" % (repo_meta.username, repo_meta.reponame))

            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            log.exception("Error dealing with message: %r %s", raw_body, e)

    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue='repos-to-load', durable=True)
    channel.basic_qos(prefetch_count=1)

    log.info("Waiting for repos to load")
    try:
        channel.basic_consume(cb_fetch, queue='repos-to-load')
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()


def main(args=sys.argv):
    multiprocessing.Process(target=main_fetcher, args=args).start()
    multiprocessing.Process(target=main_tagger, args=args).start()
    multiprocessing.Process(target=main_loader, args=args).start()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
