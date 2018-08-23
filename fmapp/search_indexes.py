from haystack import indexes
from fmapp.models import DiskFile
from fmapp import settings
import requests

class DiskFileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    path = indexes.CharField(model_attr='path')

    def get_model(self):
        return DiskFile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare(self, obj):
        print('indexing', settings.FILES_ROOT + obj.path)
        data = super().prepare(obj)
        f = open(settings.FILES_ROOT + obj.path, 'rb')
        data['text'] = obj.path + '\n\n' + tika_extract(f)
        # print('result:', data['text'])

        return data

def tika_extract(file):
    resp = requests.post('http://localhost:9998/tika/form',
                         files={'upload': file},
                         headers={'accept': 'text/plain'})
    if resp.status_code == 422: return ''
    resp.raise_for_status()
    return resp.content.decode('utf8')
