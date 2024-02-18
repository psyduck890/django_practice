from django.contrib import admin
from django.urls import path, reverse_lazy, include, re_path
from . import views
from django.contrib.auth import views as auth_views # Handles user login, rego, logout, reset?
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

app_name = 'core' # Must add this here to be showed up in base.html
#

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('pricing/', views.pricing, name='pricing'),
    path('logout/', views.logout_user, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html', success_url=reverse_lazy('core:password_reset_done'), html_email_template_name='core/password_reset_email.txt'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html', success_url=reverse_lazy('core:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='core/password_change.html', success_url=reverse_lazy('core:password_change_done')), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='core/password_change_done.html'), name='password_change_done'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'pages.views.error_404_view'