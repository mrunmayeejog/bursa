"""bursa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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


Entry URL mapping
"""

from django.conf.urls import url
import views

urlpatterns = [
    # list Entry
    url(r'^$', views.EntryRest.as_view(), name='list'),

    url(r'/daily$', views.ViewExpenses.as_view(), name='View_Expenses'),
    url(r'/monthly$', views.ViewExpenses.as_view(), name='View_Expenses'),
    url(r'/weekly$', views.ViewExpenses.as_view(), name='View_Expenses'),

    # Get status
    url(r'^(?P<entry_id>.+)/type$',
        views.EntryType.as_view(), name='status'),

    # Entry operations like get, delete, update Entry
    url(r'^(?P<entry_id>.+)$', views.EntryOperations.as_view(), name='Entry_operations'),

    # Check for daily/monthly/weekly expenses

]
