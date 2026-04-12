import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from openai import OpenAI
from .models import Profile, Opportunity, Event

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_embedding(text):
    """Sends text to OpenAI and returns the 1536-dimension math vector"""

    response = client.embeddings.create(
        input= text
        model='text-embedding-3-small'
    )

    return response.data[0].embedding

@receiver(post_save, sender=Opportunity)
def auto_embed_opportunity(sender, instance, creaetd, **kwargs):
        #prevent infinite loop
    if kwargs.get('update_fields') and 'embedding' in kwargs.get('update_fields'):
        return
    
    # Combine the text you want the AI to "read" to understand the gig
    text_to_embed = f"{instance.title} at {instance.organization}. Location: {instance.location}. Description: {instance.description}"

    try:
        instance.embedding = get_embedding(text_to_embed)
        instance.save(update_fields=['embedding'])
    except Exception as e:
        print(f"Embedding failed for {instance.title}: {e}")


@receiver(post_save,sender=Profile, )
def auto_embed_profile(sender, instance, created, **kwargs):
    if kwargs.get('update_fields') and 'embedding' in kwargs.get('update_fields'):
        return
    
    text_to_embed = f'Major:{instance.major}. Bio:{instance.bio}'
    try:
        instance.embedding = get_embedding(text_to_embed)
        instance.save(update_fields=['embedding'])
    except Exception as e:
        print(f"Embedding failed for Profile {instance.user.username}: {e}")
    