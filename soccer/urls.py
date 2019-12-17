from django.urls import path
from soccer.views import HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    # path('<str:slug>/', PageDetailView.as_view(), name='wiki-details-page'),
    # path('/new/', NewWikiView.as_view(), name='new-wiki'),

]
