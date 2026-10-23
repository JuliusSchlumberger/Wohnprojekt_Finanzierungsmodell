"""Entry point for the browser build; the app itself comes from the installed package."""

from app.main import serve

serve().servable()
