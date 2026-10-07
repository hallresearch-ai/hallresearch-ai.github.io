#!/usr/bin/env python3
"""Preview public/ over HTTP, including a real custom 404 response."""
import argparse
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import posixpath
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8000);parser.add_argument('--directory',type=Path,default=ROOT/'public');parser.add_argument('--base-path',default='/');args=parser.parse_args()
base='/' + args.base_path.strip('/') if args.base_path.strip('/') else ''
class Handler(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  requested=unquote(urlsplit(path).path)
  if base:
   if requested!=base and not requested.startswith(base+'/'):return str(args.directory/'__outside_preview_base__')
   requested=requested[len(base):]
  parts=[x for x in posixpath.normpath(requested).split('/') if x not in ('','.','..')]
  return str(args.directory.resolve().joinpath(*parts))
 def send_error(self,code,message=None,explain=None):
  if code==404 and (args.directory/'404.html').exists():
   data=(args.directory/'404.html').read_bytes();self.send_response(404);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers()
   if self.command!='HEAD':self.wfile.write(data)
  else:super().send_error(code,message,explain)
 def log_message(self,format,*values):pass
print(f'Preview at http://127.0.0.1:{args.port}{base}/',flush=True)
ThreadingHTTPServer(('127.0.0.1',args.port),partial(Handler,directory=str(args.directory))).serve_forever()
