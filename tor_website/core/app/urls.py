from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'states', views.StateViewSet)
router.register(r'counties', views.CountyViewSet)
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('privacy/', views.privacy_policy, name='privacy_policy'),  # Privacy policy page
    path('terms/', views.terms_of_service, name='terms_of_service'),  # Terms of service page
    path('states/', views.state_list, name='state_list'),  # State list view
    path('state/<str:state_id>/', views.state_detail, name='state'),  # State detail view
    path('states/map/', views.interactive_map, name='interactive_map'),  # Interactive map view
]
