""" This file provide some utility functions for Arch Linux specific rules."""
import thefuck.utils
import subprocess


@thefuck.utils.memoize
def get_pkgfile(command):
    """ Gets the packages that provide the given command using `pkgfile`.

    If the command is of the form `sudo foo`, searches for the `foo` command
    instead.
    """
    try:
        command = command.strip()

        if command.startswith('sudo '):
            command = command[5:]

        command = command.split(" ")[0]

        packages = subprocess.check_output(
            ['pkgfile', '-b', '-v', command],
            universal_newlines=True, stderr=thefuck.utils.DEVNULL
        ).splitlines()

        return [package.split()[0] for package in packages]
    except subprocess.CalledProcessError:
        return None


def archlinux_env():
    if thefuck.utils.which('yaourt'):
        pacman = 'yaourt'
    elif thefuck.utils.which('pacman'):
        pacman = 'sudo pacman'
    else:
        return False, None

    enabled_by_default = thefuck.utils.which('pkgfile')

    return enabled_by_default, pacman