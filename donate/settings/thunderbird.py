from .environment import app


class ThunderbirdOverrides(object):
    THUNDERBIRD = True
    INSTALLED_APPS = ['donate.thunderbird']
    TEMPLATES_DIR = [app('thunderbird/templates')]
