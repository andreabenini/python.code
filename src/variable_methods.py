# ------------------------------------------------------------------------------
class Foo(object):
    def __init__(self):
        self._attr_path = []

    def __getattr__(self, attr):
        self._attr_path.append(attr)
        return self

    def __call__(self, *args, **kw):
        print ".".join(self._attr_path)
        print args, kw
        del self._attr_path[:]

f = Foo()
f.a.b.c(1,2,3)
# Output
# a.b.c
# (1, 2, 3) {}

# ------------------------------------------------------------------------------
class Bar(object):
    def __init__(self, foo, attr):
        self.foo = foo
        self._attr_path = [attr]

    def __getattr__(self, attr):
        self._attr_path.append(attr)
        return self

    def __call__(self, *args, **kw):
        print self
        print args, kw

    def __str__(self):
        return ".".join(self._attr_path)

class Foo(object):

    def __getattr__(self, attr):
        return Bar(self, attr)

f = Foo()
f.a.b.c(1,2,3)

# ------------------------------------------------------------------------------
class Foo(object):

    def __init__(self, parent=None, name=""):
        self.parent = parent
        self.name = name

    def __getattr__(self, attr):
        return Foo(parent=self, name=attr)

    def __call__(self, *args, **kw):
        print self
        print args, kw    

    def __str__(self):
        nodes = []
        node = self
        while node.parent:
            nodes.append(node)
            node = node.parent
        return ".".join(node.name for node in nodes[::-1])

f = Foo()
x = f.a.b
y = f.a.c
x()
y()

g = f.a
f.b
g.b.c()
