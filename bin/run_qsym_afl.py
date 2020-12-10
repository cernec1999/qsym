#!/usr/bin/env python2
import atexit
import argparse
import logging
import functools
import hashlib
import json
import os
import pickle
import shutil
import subprocess as sp
import sys
import tempfile
import time
import pyinotify
import qsym

logger = logging.getLogger('qsym.afl')

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("-o", dest="output", required=True, help="AFL output directory")
    p.add_argument("-b", dest="trace_bin", required=True, help="Instrumented tracing binary")
    p.add_argument("-a", dest="afl", required=True, help="AFL name")
    p.add_argument("-n", dest="name", required=True, help="Qsym name")
    p.add_argument("-f", dest="filename", default=None)
    p.add_argument("-m", dest="mail", default=None)
    p.add_argument("cmd", nargs="+", help="cmdline, use %s to denote a file" % qsym.utils.AT_FILE)
    return p.parse_args()

def check_args(args):
    if not os.path.exists(args.output):
        logger.debug("Waiting for AFL output dir...")
        t_wait = time.time() + 900

        # Give AFL ample time to set up.

        while time.time() < t_wait:
            if os.path.exists(args.output):
                break
            else:
                continue

    if not os.path.exists(args.output):
        logger.debug("Missing AFL output dir!")
        exit(0)

    logger.debug("Found AFL output dir")

def main():
    args = parse_args()
    check_args(args)

    e = qsym.afl.AFLExecutor(args.cmd, args.trace_bin, args.output, args.afl,
            args.name, args.filename, args.mail)   
    
    try:
        e.run()
    finally:
        e.cleanup()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
