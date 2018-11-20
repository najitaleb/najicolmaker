def convertPath(path):
    sep= os.sep
    if sep != '/':
          path = path.replace(sep, '/')
    return path