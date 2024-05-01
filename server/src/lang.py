"""Language configuration of server information."""
import gettext
import locale

LOCALES = {
    ("en_US", "UTF-8"): gettext.NullTranslations(),
    ("zh_CN", "UTF-8"): gettext.translation(
        "Chinese", "locale", ["zh_CN"]
        ),
    ("ru_RU", "UTF-8"): gettext.translation(
        "Russian", "locale", ["ru_RU"]
        )
}


def _(text):
    """Call this function to obtain the language pack."""
    return LOCALES[locale.getlocale()].gettext(text)


def ngettext(*args):
    """Call this function to get the language convention setting."""
    return LOCALES[locale.getlocale()].ngettext(*args)
