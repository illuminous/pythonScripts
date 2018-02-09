import urllib, os, fnmatch
root = 'https://fpa.nwcg.gov/FPACommonREST/fpaservices/LF/SimRun/download'
url = urllib.urlopen(root)
patterns = '*.zip'
def all_files(root, patterns = '*', single_level=False, yield_folders=False):
    #Expand patterns from semicolon-seperated string to list
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break
            if single_level:
                break

