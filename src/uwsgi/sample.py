def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    yield b"Row One<br>"
    yield b"Row Two<br>"
    yield b"Row Three<br><xmp>"
    for Item in env:
        yield ("%s = %s\n" % (Item, env[Item])).encode('UTF-8')
    yield b"</xmp>"
    # return [b"Hello World :)"]
