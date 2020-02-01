from django.urls import path
from soccer.views import HomePageView, DetailPageView, MyAccountPageView, saveMatch, deleteMatch, Index

app_name = 'soccer'
urlpatterns = [
    # Home page link
    path('home/', HomePageView.as_view(), name='home'),
    # Home page link
    path('', Index.as_view(), name='index'),
    # Detail page link with match id
    path('<int:fixtureId>/', DetailPageView.as_view(), name='detail'),
    # myaccount link
    path('myaccount/', MyAccountPageView.as_view(), name='myaccount'),
    # path to save a match
    path('match/<int:fixtureId>/save', saveMatch, name='savematch'),
    # path to delete a match
    path('match/<int:fixtureId>/delete', deleteMatch, name='deletematch'),

]
