from django.conf.urls import include, patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/', include('lists.urls')),
)
