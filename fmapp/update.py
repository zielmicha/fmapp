import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'fmapp.settings'
import django
django.setup()

from fmapp import settings, models
from typing import NamedTuple
import stat, os

class Entry(NamedTuple):
    path: str
    mtime: int
    size: int

def get_files():
    result = []
    for root, dirs, files in os.walk(settings.FILES_ROOT):
        for f in files:
            s = os.stat(root + '/' + f)
            result.append(Entry(
                '/' + os.path.relpath(root + '/' + f, settings.FILES_ROOT),
                int(s.st_mtime * 1000),
                s.st_size))

    return result

def main():
    db_files = {
        f.path:f
        for f in models.DiskFile.objects.all()
    }

    for entry in get_files():
        if entry.path in db_files:
            f = db_files[entry.path]
            if (f.mtime, f.size) != (entry.mtime, entry.size):
                f.mtime, f.size = (entry.mtime, entry.size)
                f.save()
                print('update file', entry.path)
            del db_files[entry.path]
        else:
            print('create file', entry.path)
            models.DiskFile(path=entry.path, mtime=entry.mtime, size=entry.size).save()

    for f in db_files.values():
        print('delete file', f.path)
        f.delete()

if __name__ == '__main__':
    main()
