"""restaurants URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('categories.urls', 'categories'), namespace='categories')),
    path('', include(('cartcodes.urls', 'cartcodes'), namespace='cartcodes')),
    path('', include(('dishes.urls', 'dishes'), namespace='dishes')),
    path('', include(('restaurant_dish_link.urls', 'restaurant_dish_link'), namespace='restaurant_dish_link')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)