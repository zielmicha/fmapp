from typing import List, Dict, Any, Optional
from django.http import HttpResponse, HttpRequest, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from fmapp import settings, models
import os
from wsgiref.util import FileWrapper

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
    }
    for k, v in exts.items():
        if path.endswith(k):
            return v

    return 'application/octet-stream'

def get_icon(full_path):
    if os.path.isdir(full_path):
        return 'folder'

    exts = {
        '.pdf': 'file-pdf',
    }
    for k, v in exts.items():
        if full_path.endswith(k):
            return v

    return 'file'

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
            'is_root': not path,
            'path': path,
        })
    else:
        resp = StreamingHttpResponse(
            FileWrapper(open(full_path, 'rb'), 10000),
            content_type=get_content_type(path))
        resp['X-Content-Type-Options'] = 'nosniff'
        return resp

def upload(request: HttpRequest) -> HttpResponse:
    return render(request, 'upload.html', {})

def queue(request: HttpRequest) -> HttpResponse:
    return render(request, 'queue.html', {})

def context_processor(request: HttpRequest):
    return {
        'user': request.user if request.user.is_authenticated else None,
        'profile': models.UserProfile.get(request.user),
    }
