from typing import List, Dict, Any, Optional
from django.http import HttpResponse, HttpRequest, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from fmapp import settings, models
import os, shutil
from wsgiref.util import FileWrapper
from haystack.views import SearchView
from haystack.query import SearchQuerySet

class HighlightedSearchView(SearchView):

    def get_results(self):
        return SearchQuerySet().filter(text=self.get_query()).highlight()

def home(request: HttpRequest) -> HttpResponse:
    return redirect('/file/')

def check_path(path):
    if not path.startswith('/'): return
    path = path[1:]
    if path.endswith('/'):
        path = path[:-1]
    if path == '': return
    if '\\' in path: raise ValueError('bad path')
    if '\0' in path: raise ValueError('bad path')

    s = path.split('/')

    for part in s:
        if part in ('', '.', '..'):
            raise ValueError('bad path')

def get_content_type(path):
    exts = {
        '.pdf': 'application/pdf',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
    }
    for k, v in exts.items():
        if path.lower().endswith(k):
            return v

    return 'application/octet-stream'

def get_icon(full_path):
    if os.path.isdir(full_path):
        return 'folder'

    exts = {
        '.pdf': 'file-pdf',
    }
    for k, v in exts.items():
        if full_path.lower().endswith(k):
            return v

    return 'file'

def dir_browser(request: HttpResponse, path) -> HttpResponse:
    check_path(path)

    full_path = settings.FILES_ROOT + '/' + path

    if not path.endswith('/'):
        return redirect('/dir-browser' + path + '/')

    children: List[Dict] = []
    for name in os.listdir(full_path):
        child_full_path = full_path + name
        if os.path.isdir(child_full_path):
            child_path = path + name
            children.append({
                'name': name,
                'path': child_path,
            })

    children.sort(key=lambda c: c['name'])

    return render(request, 'dir_browser.html', {
        'children': children,
        'is_root': path == '/',
        'path': path,
    })

def local_file_response(path, force_name=None):
    resp = StreamingHttpResponse(
        FileWrapper(open(path, 'rb'), 10000),
        content_type=get_content_type(path))
    resp['X-Content-Type-Options'] = 'nosniff'
    if force_name:
        resp['Content-Disposition'] = 'inline; filename="%s"' % (force_name.split('"')[-1])
    return resp

@login_required
def file(request: HttpRequest, path) -> HttpResponse:
    check_path(path)

    full_path = settings.FILES_ROOT + '/' + path

    if os.path.isdir(full_path):
        if not path.endswith('/'):
            return redirect('/file' + path + '/')

        children: List = []

        for name in os.listdir(full_path):
            child_full_path = full_path + name
            child_path = path + name
            icon = get_icon(child_full_path)
            children.append({
                'name': name,
                'path': child_path,
                'icon_name': icon,
            })

        children.sort(key=lambda c: (c['icon_name'] != 'folder', c['name']))

        return render(request, 'tree.html', {
            'children': children,
            'is_root': path == '/',
            'path': path,
        })
    else:
        return local_file_response(full_path)

@login_required
def upload(request: HttpRequest) -> HttpResponse:
    if request.POST:
        models.QueuedFile(
            uploader=request.user,
            comment=request.POST.get('comment'),
            file=request.FILES['file'],
            target_dir=request.POST['target_dir']
        ).save()
        return redirect('/upload/')

    return render(request, 'upload.html', {
        'your_queue': models.QueuedFile.objects.filter(uploader=request.user)
    })

@login_required
def queue(request: HttpRequest) -> HttpResponse:
    return render(request, 'queue.html', {
        'files': models.QueuedFile.objects.all()
    })

@login_required
def queue_file(request: HttpRequest, id: int) -> HttpRequest:
    file = models.QueuedFile.objects.get(id=id)

    return local_file_response(file.file.path, force_name=file.file.path.split('/')[-1])

@login_required
def queue_approve(request: HttpRequest, id: int) -> HttpRequest:
    file = models.QueuedFile.objects.get(id=id)

    target_path = request.POST['target_path']
    check_path(target_path)

    shutil.move(file.file.path, settings.FILES_ROOT + '/' + target_path)
    file.delete()

    return redirect('/queue/')

@login_required
def queue_delete(request: HttpRequest, id: int) -> HttpRequest:
    file = models.QueuedFile.objects.get(id=id)
    file.file.delete()
    file.delete()

    return redirect('/queue/')

def context_processor(request: HttpRequest):
    return {
        'user': request.user if request.user.is_authenticated else None,
        'profile': models.UserProfile.get(request.user) if request.user.is_authenticated else None,
    }
