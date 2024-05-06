'''
Default: create wheel
'''
import glob
from doit.tools import create_folder

DOIT_CONFIG = {'default_tasks': ['setup']}
LOCALE_DEST = 'src/cybermarket_client/locale'


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
        'actions': ['git clean -xdf'],
    }


def task_pot():
    """Re-create .pot ."""
    return {
        'actions': ['pybabel extract -o ./locale/locale.pot src'],
        'file_dep': glob.glob('src/*.py'),
        'targets': ['./locale/locale.pot'],
    }


def task_po():
    """Update translations."""
    return {
        'actions':
        [
            'pybabel update -D Chinese -d locale -i ./locale/locale.pot',
            'pybabel update -D Russian -d locale -i ./locale/locale.pot',
        ],
        'task_dep': ['pot'],
        'file_dep': ['./locale/locale.pot'],
        'targets':
        [
            './locale/zh_CN/LC_MESSAGES/Chinese.po',
            './locale/ru_RU/LC_MESSAGES/Russian.po',
        ],
    }


def task_mo():
    """Compile translations."""
    return {
        'actions':
        [
            (create_folder, [
                '{}/zh_CN/LC_MESSAGES'.format(LOCALE_DEST),
            ]),
            (create_folder, [
                '{}/ru_RU/LC_MESSAGES'.format(LOCALE_DEST),
            ]),
            'pybabel compile -D Chinese -l zh_CN -i ./locale/zh_CN/LC_MESSAGES\
/Chinese.po -d {}'.format(LOCALE_DEST),
            'pybabel compile -D Russian -l ru_RU -i ./locale/ru_RU/LC_MESSAGES\
/Russian.po -d {}'.format(LOCALE_DEST),
        ],
        'task_dep': ['po'],
        'file_dep':
        [
            './locale/zh_CN/LC_MESSAGES/Chinese.po',
            './locale/ru_RU/LC_MESSAGES/Russian.po',
        ],
        'targets':
        [
            '{}/zh_CN/LC_MESSAGES/Chinese.mo'.format(LOCALE_DEST),
            '{}/ru_RU/LC_MESSAGES/Russian.mo'.format(LOCALE_DEST),
        ],
    }


def task_html():
    """Make HTML documentation."""
    return {
        'actions': ['sphinx-build -M html ./docs/source ./docs/build'],
        'task_dep': ['mo']
    }


def task_style():
    """Check style against flake8."""
    return {
            'actions': ['flake8 src']
           }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
            'actions': ['pydocstyle src']
           }


def task_test():
    """Preform tests."""
    return {
        'actions': ['python -m unittest -v ./tests/unit_test.py'],
        'task_dep': ['mo']
    }


def task_check():
    """Perform all checks."""
    return {
            'actions': None,
            'task_dep': ['style', 'docstyle', 'mo']
           }


def task_sdist():
    """Create source distribution."""
    return {
            'actions': ['python -m build -s -n'],
            'task_dep': ['gitclean'],
           }


def task_wheel():
    """Create binary wheel distribution."""
    return {
            'actions': ['python -m build -n -w'],
            'task_dep': ['mo'],
           }


def task_setup():
    """Perform all build task."""
    return {
            'actions': None,
            'task_dep': ['check', 'html']
           }


def task_app():
    """Run application."""
    return {
        'actions': ["python -m src.cybermarket_client"],
        'task_dep': ['mo'],
    }
