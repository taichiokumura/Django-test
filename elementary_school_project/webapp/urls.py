from django.urls import path
from .views import card_create
from .views import home
from .views import card_info
from .views import login

app_name = 'webtestapp'

urlpatterns = [
    path('', home.home_header, name='header'),
    path('card_view', card_info.CardListView, name='card'),
    path('cutout_fish', card_create.index, name='index'),
    # path('cutout_fish/<int:image_id>/', card_create.cutout_fish, name='cutout_fish'),
    # path('home', login.login_card, name='login'),
]