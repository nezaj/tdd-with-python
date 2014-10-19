from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/one-list/$', 'lists.views.view_list', name='view_list'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
