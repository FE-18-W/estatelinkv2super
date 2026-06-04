# Render deployment notes

1. Push the repository to GitHub.
2. In Render, create a new Web Service connected to the GitHub repo.
3. Use the included `render.yaml` for the service setup. Render will install dependencies, run `collectstatic`, and start the app with Gunicorn.
4. Set environment variables in Render if needed:
   - `SECRET_KEY` (auto-generated or custom)
   - `DEBUG=0`
   - `ALLOWED_HOSTS=*`
   - `CSRF_TRUSTED_ORIGINS=https://<your-render-hostname>`
5. Render will provision the PostgreSQL database defined in `render.yaml` and inject `DATABASE_URL` automatically.
6. After deployment, visit the service URL and run migrations if Render does not apply them automatically:
   - `python manage.py migrate`
