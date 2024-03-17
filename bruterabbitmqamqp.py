#!/usr/bin/env python
import socket
from kombu import Connection
host = "localhost"
port = 5672
user = ""
password = ""
vhost = "/"
with open("alive.txt") as file:
  for host in file:
    print(host)
    url = 'amqp://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, vhost)
    with Connection(url) as c:
        try:
            c.connect()
        except:
            pass
        else:
            print "Credentials are valid"+str(host)