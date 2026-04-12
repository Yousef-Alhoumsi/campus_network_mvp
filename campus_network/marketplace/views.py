from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pgvector.django import CosineDistance
from .models import Profile, Opportunity, Event
from django.core.mail import send_mail
from django.contrib import messages


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

   

@login_required
def apply_to_gig(request, gig_id):

    gig = get_object_or_404(Opportunity, id=gig_id)
    student = request.user.profile

    subject = f"New Student Interest: {gig.title}"

    message = f"Hello {gig.organization},\n\n" \
              f"A student is interested in your opportunity: {gig.title}.\n\n" \
              f"Student Name: {request.user.first_name} {request.user.last_name}\n" \
              f"Major: {student.major}\n" \
              f"Contact Email: {request.user.email}\n\n" \
              f"Student Bio:\n{student.bio}\n\n" \
              f"Please reach out to them directly at {request.user.email} to connect!"
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email="yousefalhomsi89@gmail.com",
            recipient_list=[gig.organization],
            fail_silently=False
            )
        
        messages.success(request, f"Your profile was successfully sent to {gig.organization}!")
    except Exception as e:
        messages.error(request, "Oops! There was an issue sending your application.")

    return redirect("student_feed")





