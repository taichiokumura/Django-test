from django.urls import path
from .views import card_create
from .views import home
from .views import card_info
from .views import view_map
from .views import river_registration

app_name = 'webtestapp'

urlpatterns = [
    path('', home.home_header, name='header'),
    path('card_view', card_info.CardListView, name='card'),
    path('map_view', view_map.map_confirmation, name='map'),
    path('cutout_fish', card_create.index, name='index'),
    path('river_registration', river_registration.river_view, name='river'),
    # path('cutout_fish/<int:image_id>/', card_create.cutout_fish, name='cutout_fish'),
    # path('home', login.login_card, name='login'),
]