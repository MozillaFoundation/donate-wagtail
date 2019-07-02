from wagtail.core.models import Page


class HomePage(Page):
    template = 'pages/home/home_page.html'

    # Only allow creating HomePages at the root level
    parent_page_types = ['wagtailcore.Page']
