# home/views.py

from django.shortcuts import render
from django.db.models import Avg, Count, OuterRef, Subquery
# Import your Property model (This line is correct)
from properties.models import Property, PropertyPhoto

def index(request):
    # Get the ID of the first photo for each property
    first_photo_subquery = PropertyPhoto.objects.filter(
        property=OuterRef('pk')
    ).order_by('uploaded_at').values('image')[:1]

    # Query for top properties
    top_properties = Property.objects.filter(
        is_active=True # Only show active properties
    ).annotate(
        avg_rating=Avg('ratings__score'), # Calculate average rating
        total_ratings=Count('ratings'), # Count total ratings
        first_photo_url=Subquery(first_photo_subquery) # Get the first photo URL
    ).filter(
        total_ratings__gt=0 # Only include properties with at least one rating
    ).order_by(
        '-avg_rating' # Order by highest rating first
    )[:3] # Get the top 3

    context = {
        'top_properties': top_properties
    }
    # Make sure your template path is correct (e.g., 'home/index.html' or just 'index.html')
    return render(request, 'home/index.html', context)