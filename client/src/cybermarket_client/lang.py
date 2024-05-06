"""Language configuration of server information."""
import os
import gettext
import locale

module_path = os.path.abspath(__file__)
module_dir = os.path.dirname(module_path)
locale_path = os.path.join(module_dir, 'locale')

LOCALES = {
    ("en_US", "UTF-8"): gettext.NullTranslations(),
    ("zh_CN", "UTF-8"): gettext.translation(
        "Chinese", locale_path, ["zh_CN"], fallback=True
        ),
    ("ru_RU", "UTF-8"): gettext.translation(
        "Russian", locale_path, ["ru_RU"], fallback=True
        )
}

# Language setting
lang = locale.setlocale(locale.LC_ALL, ("zh_CN", "UTF-8"))


def _(text):
    """Call this function to obtain the language pack."""
    return LOCALES[locale.getlocale()].gettext(text)


def ngettext(*args):
    """Call this function to get the language convention setting."""
    return LOCALES[locale.getlocale()].ngettext(*args)
