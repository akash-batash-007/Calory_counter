from django.urls import path
from calory_counter_app.views import *


urlpatterns = [
    path('', login_view, name='login_view'),
    path('register/', register_view, name='register_view'),
    path('logout/', logout_view, name='logout_view'),

    path('dashboard/', dashboard, name='dashboard'),

    path('profile/', profile_view, name='profile_view'),
    path('profile-update/', profile_update, name='profile_update'),

    path('consumed-calorie-list/', calorie_list, name='calorie_list'),
    path('add-consumed-calorie/', add_consumed_calorie, name='add_consumed_calorie'),
    path('edit-consumed-calorie/<str:c_id>/', edit_consumed_calorie, name='edit_consumed_calorie'),
    path('delete-consumed-calorie/<str:c_id>/', delete_consumed_calorie, name='delete_consumed_calorie'),
]