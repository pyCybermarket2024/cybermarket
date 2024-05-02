from setuptools import setup, Command


class DoitAllCommand(Command):
    """Setuptools command to run 'doit all'."""
    description = 'run doit all'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        import os
        os.system('doit')


setup(
    cmdclass={
        'doit': DoitAllCommand,
    },
)
