# TOKENIZE PATH - Split a path (full/partial) in an array
# @param Path (string) Path to be parsed (full or partial path)
# @return (array) the parsed path
def TokenizePath(Path, Result=[]):
    if len(Path) > 0 and Path != os.sep:
        Result = [os.path.basename(Path)] + Result
        Path   = os.path.dirname(Path)
        return TokenizePath(Path, Result)
    return Result

# print("Output = %s" % TokenizePath(sys.argv[1]))

