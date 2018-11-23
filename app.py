#!/usr/bin/env python

import argparse
import base64
from dotenv import load_dotenv
from flask import Flask, abort, make_response
import io
from ldap3 import Server, Connection
import logging
import os
from pathlib import Path
import sys

# Set up the logger
logger = logging.getLogger()
handler = logging.StreamHandler(stream=sys.stdout)
formatter_debug = logging.Formatter(
    '%(asctime)s [%(levelname)8s](%(funcName)s:%(lineno)d): %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
formatter = logging.Formatter(
    '%(asctime)s  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Flask app
app = Flask(__name__)

# Test if data is base64 encoded or not


def isBase64(s):
  try:
    return base64.b64encode(base64.b64decode(s)) == s
  except Exception:
    return False


@app.route('/<user>')
def get_thumbnail(user):
  logger.debug("Got request for user: {}".format(user))
  try:
    server = Server(os.getenv("LDAP_SERVER"), port=os.getenv("LDAP_PORT", 389))
    conn = Connection(server, os.getenv("LDAP_USER"), os.getenv("LDAP_PASS"), auto_bind=True)
  except Exception as e:
    abort(500)

  logger.debug("Connection: {}".format(conn))

  attribPhoto = os.getenv("LDAP_ATTRIBUTE", 'thumbnailPhoto')
  conn.search(os.getenv("LDAP_BASE"), "({}={})".format(os.getenv("LDAP_LOOKUP"), user),
              attributes=['objectclass', 'cn', attribPhoto])

  if conn.entries:
    logger.debug("Entries: {}".format(conn.entries))
    if attribPhoto in conn.entries[0].entry_attributes:
      image_binary = conn.entries[0][attribPhoto].value
      if image_binary:
        if isBase64(image_binary):
          image_binary = base64.b64decode(image_binary)
        response = make_response(image_binary)
        response.headers.set('Content-Type', 'image/jpeg')
        response.headers.set('Content-Disposition', 'attachment',
                             filename='{}.jpg'.format(conn.entries[0]['cn']))
        return response
      else:
        abort(404)
    else:
      abort(404)
  else:
    abort(404)


def init():
  parser = argparse.ArgumentParser(description="Jabber Pic Server")
  parser.add_argument("-c", "--config", help="Directory for .env file",
                      default=Path("/srv/jabber-pic-server"))
  parser.add_argument("-d", "--debug", action="store_true",
                      help="Enable debug info")
  args = parser.parse_args()

  if args.debug:
    logger.setLevel(logging.DEBUG)
    handler.setFormatter(formatter_debug)
    logger.debug("Enabling DEBUG output")

  main(args)


def main(args):
  logger.debug("Args: {}".format(args))
  # Load .env file
  load_dotenv(dotenv_path=args.config)
  logger.debug("LDAP Server: {}".format(os.getenv("LDAP_SERVER")))
  logger.debug("LDAP Port: {}".format(os.getenv("LDAP_PORT")))
  logger.debug("LDAP SSL: {}".format(os.getenv("LDAP_SSL")))
  logger.debug("LDAP User: {}".format(os.getenv("LDAP_USER")))
  logger.debug("LDAP Base: {}".format(os.getenv("LDAP_BASE")))
  logger.debug("LDAP Lookup: {}".format(os.getenv("LDAP_LOOKUP")))
  logger.debug("LDAP Photot Attribute: {}".format(os.getenv("LDAP_ATTRIBUTE")))
  app.run(debug=args.debug)


if __name__ == '__main__':
  init()
