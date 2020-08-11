# -*- coding:utf-8 -*-
import os
import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing

chdir = "/opt/gitProxy"
debug = False
loglevel = "info"
bind = "0.0.0.0:5000"
pidfile = "log/gunicorn.pid"
accesslog = "log/access.log"
errorlog = "log/error.log"
daemon = True
workers = multiprocessing.cpu_count()*2+1
worker_class = "gevent"
x_forwarded_for_header = "X-FORWARDED-FOR"
