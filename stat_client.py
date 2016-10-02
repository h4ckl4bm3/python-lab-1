#!/usr/bin/env python
"""Simple client to test stat_server."""

import time
import xmlrpclib

PROXY = xmlrpclib.ServerProxy("http://localhost:8000/")
print "Start value:", PROXY.server_status("status")
print "Add path."
PROXY.add_path("/Users/reuteras/tmp")
print "Sleep 2."
time.sleep(2)
print "End value:", PROXY.server_status("status")

