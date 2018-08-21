from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from fmapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home),

    re_path(r'^file(/.*)$', views.file),
    re_path(r'^dir-browser(/.*)$', views.dir_browser),

    path('upload/', views.upload),
    path('queue/', views.queue),
    path('queue-file/<int:id>', views.queue_file),
    path('queue-approve/<int:id>', views.queue_approve),
    path('queue-delete/<int:id>', views.queue_delete),

    re_path(r'^accounts/', include('registration.backends.default.urls')),

    re_path(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
