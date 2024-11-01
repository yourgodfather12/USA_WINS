from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import State, County, Post
from .serializers import StateSerializer, CountySerializer, PostSerializer

# API ViewSets
class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'abbreviation']
    ordering_fields = ['name', 'abbreviation']
    ordering = ['name']

class CountyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'state__name': ['exact', 'icontains'],
        'name': ['exact', 'icontains']
    }
    search_fields = ['name']
    ordering_fields = ['name', 'state__name']
    ordering = ['name']

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'county__name': ['exact', 'icontains'],
        'county__state__name': ['exact', 'icontains']
    }
    search_fields = ['content']
    ordering_fields = ['timestamp', 'county__name', 'county__state__name']
    ordering = ['-timestamp']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Webpage views
def homepage(request):
    return render(request, 'app/homepage.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

def privacy_policy(request):
    return render(request, 'app/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'app/terms_of_service.html')

def new_post(request):
    if request.method == 'POST':
        # Placeholder for form processing
        pass
    return render(request, 'app/new_post.html')

def state_list(request):
    states = State.objects.all()
    return render(request, 'app/state_list.html', {'states': states})

# Detail view for an individual state
def state_detail(request, state_id):
    state = get_object_or_404(State, abbreviation=state_id)
    counties = County.objects.filter(state=state)
    return render(request, 'app/state_detail.html', {'state': state, 'counties': counties})

# Interactive map view
def interactive_map(request):
    states = State.objects.all()  # You may want to filter or limit this if the map becomes too crowded
    return render(request, 'app/interactive_map.html', {'states': states})
