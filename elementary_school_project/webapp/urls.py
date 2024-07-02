from django.urls import path
from .views import card_create
from .views import home
from .views import card_info
from .views import river_registration

app_name = 'webtestapp'

urlpatterns = [
    path('', home.home_header, name='header'),
    path('card_view', card_info.CardListView, name='card'),
    path('cutout_fish', card_create.index, name='index'),
    path('river_registration', river_registration.river_view, name='river'),
    path('map/<str:location>/', river_registration.map_view, name='map'),
    path('save_position/', river_registration.save_position, name='save_position'),
    path('display_position/', river_registration.display_position, name='display_position'),
    path('get_card_info/<str:card_info_unique_id>/', river_registration.get_card_info, name='get_card_info'),
]