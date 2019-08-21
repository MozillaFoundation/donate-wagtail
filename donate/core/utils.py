from django.conf import settings
from django.urls import LocalePrefixPattern, URLResolver
from django.utils.translation.trans_real import (
    check_for_language, get_languages, get_language_from_path,
    get_supported_language_variant, parse_accept_lang_header, language_code_re
)


class ISO3166LocalePrefixPattern(LocalePrefixPattern):
    """LocalePrefixPattern subclass that enforces URL prefixes in the form en-US"""

    def match(self, path):
        language_prefix = language_code_to_iso_3166(self.language_prefix)
        if path.startswith(language_prefix):
            return path[len(language_prefix):], (), {}
        return None


def i18n_patterns(*urls, prefix_default_language=True):
    """
    Replacement for django.conf.urls.i18_patterns that uses ISO3166LocalePrefixPattern
    instead of django.urls.resolvers.LocalePrefixPattern.
    """
    if not settings.USE_I18N:
        return list(urls)
    return [
        URLResolver(
            ISO3166LocalePrefixPattern(prefix_default_language=prefix_default_language),
            list(urls),
        )
    ]


def language_code_to_iso_3166(language):
    """Turn a language name (en-us) into an ISO 3166 format (en-US)."""
    language, _, country = language.lower().partition('-')
    if country:
        return language + '-' + country.upper()
    return language


def get_language_from_request(request, check_path=False):
    """
    Replacement for django.utils.translation.get_language_from_request.
    The portion of code that is modified is identified below with a comment.
    """
    if check_path:
        lang_code = get_language_from_path(request.path_info)
        if lang_code is not None:
            return lang_code

    lang_code = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    if lang_code is not None and lang_code in get_languages() and check_for_language(lang_code):
        return lang_code

    try:
        return get_supported_language_variant(lang_code)
    except LookupError:
        pass

    accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    for accept_lang, unused in parse_accept_lang_header(accept):
        if accept_lang == '*':
            break

        # Convert lowercase region to uppercase before attempting to find a variant.
        # This is the only portion of code that is modified from the core function.
        accept_lang = language_code_to_iso_3166(accept_lang)

        if not language_code_re.search(accept_lang):
            continue

        try:
            return get_supported_language_variant(accept_lang)
        except LookupError:
            continue

    try:
        return get_supported_language_variant(settings.LANGUAGE_CODE)
    except LookupError:
        return settings.LANGUAGE_CODE
