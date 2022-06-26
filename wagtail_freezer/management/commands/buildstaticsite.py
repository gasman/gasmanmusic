from pathlib import Path
from shutil import rmtree

from django.core.exceptions import ImproperlyConfigured
from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import WSGIRequest
from django.core.management.base import BaseCommand
from django.conf import settings
from wagtail.models import Site

class Command(BaseCommand):
    help = "Generate a static HTML version of this Wagtail site"

    def handle(self, *args, **options):
        try:
            static_root = Path(settings.FREEZER_BUILD_DIR)
        except AttributeError:
            raise ImproperlyConfigured("FREEZER_BUILD_DIR must be defined in settings")

        sites = Site.objects.all()

        for site in sites:
            site_static_root = static_root / site.hostname
            rmtree(site_static_root, ignore_errors=True)

            pages = site.root_page.get_descendants(inclusive=True).live().order_by('path').specific()
            for page in pages:
                relative_path = page.url_path[len(site.root_page.url_path):]
                page_path = site_static_root / relative_path 

                dummy_meta = page._get_dummy_headers()
                request = WSGIRequest(dummy_meta)

                # Add a flag to let middleware know that this is a dummy request.
                request.is_dummy = True

                # Build a custom django.core.handlers.BaseHandler subclass that invokes serve() as
                # the eventual view function called at the end of the middleware chain, rather than going
                # through the URL resolver
                class Handler(BaseHandler):
                    def _get_response(self, request):
                        response = page.serve(request)
                        if hasattr(response, "render") and callable(response.render):
                            response = response.render()
                        return response

                # Invoke this custom handler.
                handler = Handler()
                handler.load_middleware()
                response = handler.get_response(request)

                page_path.mkdir(parents=True)
                with (page_path / "index.html").open(mode='wb') as f:
                    f.write(response.content)
 