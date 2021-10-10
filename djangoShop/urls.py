"""djangoShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from djangoShop import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dj_rest_auth.views import PasswordResetConfirmView
from django.conf.urls.i18n import i18n_patterns
from product.views import change_lang, Home
from order.views import apply_cupon

urlpatterns = [
    path('change_lang/', change_lang, name='change_lang'),
    path('order/apply_cupon/', apply_cupon, name='apply_cupon'),
    # path('api-token-auth/', views.obtain_auth_token)
    path('api/rest-auth/', include('dj_rest_auth.urls')),
    # path('api/rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/', include('member.api.urls')),
    path('api/rest-auth/password/reset/confirm/<uidb64>/<tocken>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

]
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('home/', Home.as_view(), name='home'),
    path('products/', include('product.urls')),
    path('member/', include('member.urls')),
    path('basket/', include('basket.urls')),
    path('order/', include('order.urls')),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
