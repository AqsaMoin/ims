from django.urls import path
from inventory.views import room_incharge

app_name = 'room_incharge'

urlpatterns = [
    path('rooms/<slug:room_slug>/categories/', room_incharge.CategoryListView.as_view(), name='category_list'),
    path('rooms/<slug:room_slug>/categories/<slug:category_slug>/update/', room_incharge.CategoryUpdateView.as_view(), name='category_update'),
    path('rooms/<slug:room_slug>/categories/<slug:category_slug>/delete/', room_incharge.CategoryDeleteView.as_view(), name='category_delete'),
    path('rooms/<slug:room_slug>/categories/create/', room_incharge.CategoryCreateView.as_view(), name='category_create'),
    path('rooms/<slug:room_slug>/dashboard/', room_incharge.RoomDashboardView.as_view(), name='room_dashboard'),
]