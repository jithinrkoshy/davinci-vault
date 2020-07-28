from django.conf.urls import url
from davinci import views

app_name ='davinci'

urlpatterns = [

    url(r'^$',views.index,name = 'index'),
    url(r'^sign_in/$',views.login_request,name = 'login'),
    url(r'^gallery/info/$',views.info_request,name = 'info'),
    url(r'^gallery/$',views.gallery,name = 'gallery'),
    url(r'^logout/$',views.logout_request,name = 'logout'),
    url(r'^gallery/vault/root/',views.vault_request,name = 'vault'),
    url(r'^gallery/vault/add_files/$',views.add_files,name = 'add_files'),
    url(r'^gallery/vault/edit_files/$',views.edit_files,name = 'edit_files'),
    url(r'^gallery/edit/root/$',views.collage_page,name = 'collage_page'),
    url(r'^gallery/edit/root/collage/(?P<value>[\w\-]+)/$',views.collage_second_page,name = 'collage_second'),
    url(r'^gallery/edit/root/collage_load/load_vault/$',views.load_vault,name = 'load_vault'),
    url(r'^gallery/format/root/$',views.format_page_one,name = 'format_page_one'),
    url(r'^gallery/format/root/(?P<value>[\w\-]+)/$',views.format_page_one,name = 'format_page_one'),
    url(r'^gallery/format/convert/(?P<value>[\w\-]+)/$',views.format_process,name = 'format_process'),
    url(r'^gallery/format/result/(?P<val>[\w\-]+)/$',views.format_page_third,name = 'format_page_third'),
]
