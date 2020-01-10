from django.urls import path
from soccer.views import HomePageView, DetailPageView, MyAccountPageView, saveMatch

app_name = 'soccer'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<int:fixtureId>/', DetailPageView.as_view(), name='detail'),
    path('myaccount/', MyAccountPageView.as_view(), name='myaccount'),
    path('<int:fixtureId>/savematch', saveMatch, name='savematch'),

]
