from django.urls import path
from soccer.views import HomePageView, DetailPageView, MyAccountPageView, saveMatch, deleteMatch

app_name = 'soccer'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<int:fixtureId>/', DetailPageView.as_view(), name='detail'),
    path('myaccount/', MyAccountPageView.as_view(), name='myaccount'),
    path('match/<int:fixtureId>/save', saveMatch, name='savematch'),
    path('match/<int:fixtureId>/delete', deleteMatch, name='deletematch'),

]
