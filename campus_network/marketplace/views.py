from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pgvector.django import CosineDistance
from .models import Profile, Opportunity, Event

@login_required
def student_feed(request):
    try:
        student_profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect ("onboarding")
    
    student_vector = student_profile.embedding

    if not student_vector:
        opportunities = Opportunity.objects.all().order_by("-id") [:10]
        events = Event.objects.all().order_by('-date_time')[:10]

    else:
        #matching cosine distance
        opportunities = Opportunity.objects.annotate(
                distance = CosineDistance("embedding", student_vector)
        ).order_by("distance")[:10]

        events = Event.objects.annotate(
            distance = CosineDistance("embedding", student_vector)

        ).order_by('distance')[:10]


    context = {
        "opportunities" : opportunities,
        "events" : events, 
    }

    return render(request, "marketplace/feed.html", context )

   

# Create your views here.


