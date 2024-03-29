#!/usr/bin/env python
#
# Simple HTTP Server With Upload.
#
# This module builds on BaseHTTPServer by implementing the standard GET and HEAD requests in a fairly straightforward manner.
# @author   Ben
#
__version__   = "0.2"
__all__       = ["SimpleHTTPRequestHandler"]
__author__    = "ben"
__home_page__ = "http://localhost/"

import os
import sys
import posixpath
import http.server
import urllib.request, urllib.parse, urllib.error
import cgi
import shutil
import mimetypes
import re
from   io import BytesIO

# Simple HTTP request handler with GET/HEAD/POST commands.
# This serves files from the current directory and any of its subdirectories.
# The MIME type for files is determined by calling the .guess_type() method and can reveive file uploaded by client.
# The GET/HEAD/POST requests are identical except that the HEAD request omits the actual contents of the file.
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    server_version = "SimpleHTTPWithUpload/" + __version__
 
    # Override constructor's method
    def log_message(self, format, *args):
        sys.stderr.write("> %s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args))

    # Serve a GET request
    def do_GET(self):
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
 
    # Serve a HEAD request
    def do_HEAD(self):
        f = self.send_head()
        if f:
            f.close()
 
    # Serve a POST request
    def do_POST(self):
        r, info = self.deal_post_data()
        print(f'- {r} {info}  [Client:{self.client_address}]')
        f = BytesIO()
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'.encode())
        f.write("\n<html>\n  <head><title>Upload Result Page</title></head>\n".encode())
        f.write("  <body>\n    <h2>Upload Result Page</h2><hr>\n    ".encode())
        if r:
            f.write("<strong>SUCCESS</strong><br>".encode())
        else:
            f.write("<strong>FAILED</strong><br>".encode())
        f.write("\n    ".encode()+info.encode())
        f.write(f"<br><a href=\"{self.headers['referer']}\">back</a>".encode())
        f.write(f"<hr><small>{__author__}, check new version at <a href=\"{__home_page__}?s=SimpleHTTPServerWithUpload\">here</a>.</small>\n".encode())
        f.write(b"  </body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
        
    def deal_post_data(self):
        httpheader = self.headers.as_string().strip().splitlines()
        print('\n'+'\n'.join([f'< {i}' for i in httpheader]) )
        print(f"- Content-Type: {self.headers['content-type']}")

        # Detecting 'Content-Type'. If boundary separator '=' is missing from multipart/form-data upload might be a real mess,
        # it should always be something like "Content-Type: multipart/form-data; boundary=------------------------2cb079591d06d033"
        content_type = self.headers['content-type']
        if not content_type:
            return (False, "Content-Type header doesn't contain boundary")
        if len(content_type.split('=')) > 1:
            boundary = content_type.split("=")[1].encode()
        else:
            print("! No 'boundary' found in content type")
            boundary = b''

        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")
                
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith(b'\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")
 
    # Common code for GET and HEAD commands.
    # This sends the response code and MIME headers.

    # Return value is either a file object (which has to be copied
    # to the outputfile by the caller unless the command was HEAD,
    # and must be closed by the caller under all circumstances), or
    # None, in which case the caller has nothing further to do.
    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f
 
    # Helper to produce a directory listing (absent index.html).
    #
    # Return value is either a file object, or None (indicating an
    # error).  In either case, the headers are sent, making the
    # interface the same as for send_head().
    def list_directory(self, path):
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = BytesIO()
        displaypath = cgi.escape(urllib.parse.unquote(self.path))
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(("<html>\n<title>Directory listing for %s</title>\n" % displaypath).encode())
        f.write(("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath).encode())
        f.write(b"<hr>\n")
        f.write(b"<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write(b"<input name=\"file\" type=\"file\"/>")
        f.write(b"<input type=\"submit\" value=\"upload\"/></form>\n")
        f.write(b"<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write(('<li><a href="%s">%s</a>\n'
                    % (urllib.parse.quote(linkname), cgi.escape(displayname))).encode())
        f.write(b"</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f
 

    # Translate a /-separated PATH to the local filename syntax.
    #
    # Components that mean special things to the local file system
    # (e.g. drive or directory names) are ignored.  (XXX They should probably be diagnosed)
    def translate_path(self, path):
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = [_f for _f in words if _f]
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path
 

    # Copy all data between two file objects.
    #
    # The SOURCE argument is a file object open for reading (or anything with a read() method) and the DESTINATION
    # argument is a file object open for writing (or anything with a write() method).
    #
    # The only reason for overriding this would be to change the block size or perhaps to replace newlines by CRLF
    # -- note however that this the default server uses this to copy binary data as well.
    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)
 

    # Guess the type of a file.
    #
    # Argument is a PATH (a filename).
    # Return value is a string of the form type/subtype, usable for a MIME Content-type header.
    # The default implementation looks the file's extension up in the table self.extensions_map, 
    # using application/octet-stream  as a default; however it would be permissible (if slow)
    # to look inside the data to make a better guess.
    def guess_type(self, path):
 
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']
 
    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
    })
 
 
def test(HandlerClass=SimpleHTTPRequestHandler, ServerClass=http.server.HTTPServer, tcpPort=8080):
    http.server.test(HandlerClass, ServerClass, port=tcpPort)

if __name__ == '__main__':
    tcpPort = 9090
    if len(sys.argv) > 1:
        tcpPort = int(sys.argv[1])
    print('\nStarting TCP Server on port {}.\n'.format(tcpPort))
    print("Server:   {} <port>                 To specify listening port on startup".format(sys.argv[0]))
    print("Client:   'curl -F \"file=@FILEtoUPLOAD\" http://localhost/'    to upload files\n")
    test(tcpPort=tcpPort)
