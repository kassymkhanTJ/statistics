"""statistics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from statistica import views as s_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^range/', s_views.range),
    url(r'^calculate/', s_views.calculate),
    url(r'^calculate_range/', s_views.calculate_range),
    url(r'^', s_views.main),
]
