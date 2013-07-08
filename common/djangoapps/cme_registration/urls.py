from django.conf.urls import patterns, url


urlpatterns = patterns(
    
    #CME Registration
    url(r'^register/cme$', 'cme_registration.views.register_user', name='cme_register_user'),
)