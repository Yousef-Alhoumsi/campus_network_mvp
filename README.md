# Campus Network MVP

## Link Supabase to this Django project

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Copy the environment template and fill in your Supabase values:

   ```bash
   cp .env.example .env
   ```

3. Run Django:

   ```bash
   python campus_network/manage.py runserver
   ```

## Supabase client usage

Use the helper in `campus_network/campus_network/supabase_client.py`:

```python
from campus_network.supabase_client import get_supabase_client

supabase = get_supabase_client()  # Uses SUPABASE_ANON_KEY
admin_client = get_supabase_client(use_service_role=True)
```
