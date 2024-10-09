from django.urls import path
from .views import card_create
from .views import home
from .views import card_info
from .views import river_registration
from .views import aquatic_life_discovery
from .views import teacher_registration
from .views import teacher_delete

app_name = 'webtestapp'

urlpatterns = [
    path('', home.home_header, name='header'),
    path('teacher_registration/', teacher_registration.account_registration, name='account_registration'),
    path('delete_student/<str:student_id>/', teacher_delete.delete_student, name='delete_student'),
    path('aquatic_life_encyclopedia/', aquatic_life_discovery.aquatic_discovery_view, name='aquatic_life'),
    path('card_view/', card_info.CardListView, name='card'),
    path('cutout_fish/', card_create.index, name='index'),
    path('river_registration/', river_registration.river_view, name='river'),
    path('map/<str:location>/', river_registration.map_view, name='map'),
    path('save_position/', river_registration.save_position, name='save_position'),
    path('save_position_and_redirect/', river_registration.save_position_and_redirect, name='save_position_and_redirect'), 
    path('display_position/<str:location>/<int:year>/', river_registration.display_position, name='display_position'),
    path('get_card_info/<str:card_info_unique_id>/', river_registration.get_card_info, name='get_card_info'),
    path('reset/', aquatic_life_discovery.reset_searched_life, name='reset_searched_life'),
    path('aquatic_life_discovery/', aquatic_life_discovery.aquatic_discovery_view, name='aquatic_discovery_view'),
]
