from functools import lru_cache

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


@lru_cache(maxsize=2)
def get_supabase_client(use_service_role: bool = False):
    """
    Build and cache a Supabase client from environment-backed Django settings.
    """
    supabase_url = settings.SUPABASE_URL
    api_key = (
        settings.SUPABASE_SERVICE_ROLE_KEY
        if use_service_role
        else settings.SUPABASE_ANON_KEY
    )

    if not supabase_url:
        raise ImproperlyConfigured('SUPABASE_URL is not configured.')
    if not api_key:
        key_name = 'SUPABASE_SERVICE_ROLE_KEY' if use_service_role else 'SUPABASE_ANON_KEY'
        raise ImproperlyConfigured(f'{key_name} is not configured.')

    try:
        from supabase import create_client
    except ImportError as exc:  # pragma: no cover
        raise ImproperlyConfigured(
            'supabase package is not installed. Install it with "pip install supabase".'
        ) from exc

    return create_client(supabase_url, api_key)
