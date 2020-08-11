import re

import requests
from flask import request, render_template, Response, redirect

def indexView():
    if 'q' in request.args:
         return redirect('/' + request.args.get('q'))
    return render_template("index.html")

def proxyView(u):
    jsdelivr = 1
    cnpmjs = 1
    size_limit = 1024 * 1024 * 1024 * 999
    CHUNK_SIZE = 1024 * 10
    exp1 = re.compile(r'^(?:https?://)?github\.com/.+?/.+?/(?:releases|archive)/.*$')
    exp2 = re.compile(r'^(?:https?://)?github\.com/.+?/.+?/(?:blob)/.*$')
    exp3 = re.compile(r'^(?:https?://)?github\.com/.+?/.+?/(?:info|git-).*$')
    exp4 = re.compile(r'^(?:https?://)?raw\.githubusercontent\.com/.+?/.+?/.+?/.+$')
    u = u if u.startswith('http') else 'https://' + u
    u = u.replace(':/g', '://g', 1)
    if jsdelivr and exp2.match(u):
        u = u.replace('/blob/', '@', 1).replace('github.com', 'cdn.jsdelivr.net/gh', 1)
        return redirect(u)
    elif cnpmjs and exp3.match(u):
        u = u.replace('github.com', 'github.com.cnpmjs.org', 1) + request.url.replace(request.base_url, '', 1)
        return redirect(u)
    elif jsdelivr and exp4.match(u):
        u = re.sub(r'\.com/.*?/.+?/(.+?/)', '@$1', u, 1)
        u = u.replace('raw.githubusercontent.com', 'cdn.jsdelivr.net/gh', 1)
        return redirect(u)
    else:
        if exp2.match(u):
            u = u.replace('/blob/', '/raw/', 1)
        headers = {}
        r_headers = {}
        for i in ['Range', 'User-Agent']:
            if i in request.headers:
                r_headers[i] = request.headers.get(i)
        try:
            r = requests.request(method=request.method, url=u + request.url.replace(request.base_url, '', 1), data=request.data, headers=r_headers, stream=True)
            for i in ['Content-Type']:
                if i in r.headers:
                    headers[i] = r.headers.get(i)
            if r.status_code == 200:
                headers = dict(r.headers)
            try:
                headers.pop('Transfer-Encoding')
            except KeyError:
                pass

            if int(r.headers['Content-length']) > size_limit:
                return redirect(u + request.url.replace(request.base_url, '', 1))

            def generate():
                for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                    yield chunk

            return Response(generate(), headers=headers, status=r.status_code)
        except Exception as e:
            headers['content-type'] = 'text/html; charset=UTF-8'
            return Response('server error ' + str(e), status=500, headers=headers)
