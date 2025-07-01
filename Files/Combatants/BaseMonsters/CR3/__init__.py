# from os.path import dirname, basename, isfile
# import glob
# items = glob.glob(f"{dirname(__file__)}/*")
# dirs = [basename(f) for f in items if not isfile(f) and not basename(f).startswith(".") and not basename(f).startswith("__")]
# files = [basename(f)[:-3] for f in items if isfile(f) and f.endswith('.py') and not f.endswith('__init__.py')]
# __all__ = dirs + files