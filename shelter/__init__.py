import os
import re
import sys
import shutil
import subprocess

import click

__version__ = '0.0.2'

TO_COMPILE = r'.*\.py$'
FILES_TO_EXCLUDE = r'.*\.(pyc|py)$'
DIRS_TO_EXCLUDE = r'^__pycache__$'


@click.command()
@click.option(
    '--path', '-p', help='Module to build.', required=True,
    type=click.Path(exists=True, readable=True))
@click.option(
    '--output', '-o', help='Build output.',
    required=True, type=click.Path(writable=True))
@click.option(
    '--include-data', is_flag=True,
    help='Include module data (like templates/statics for Django).')
@click.option('--python-version', help='Python version to use.', default='3.4')
@click.option(
    '--nuitka-bin', help='Nuitka binary path.',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default='/usr/bin/nuitka', envvar='NUITKA_BIN')
@click.version_option(version=__version__)
def main(
        path, output, include_data=False,
        python_version='3.4', nuitka_bin='/usr/bin/nuitka'):
    if not os.path.exists(output):
        os.makedirs(output)

    base_cmd = [
        nuitka_bin, '--python-version', python_version, '--remove-output']

    for basedir, dirs, files in os.walk(path):
        output_d = os.path.join(output, os.path.relpath(basedir, path))

        cmd = base_cmd + ['--output-dir', output_d]

        for d in dirs:
            if re.match(DIRS_TO_EXCLUDE, d):
                continue
            d_path = os.path.join(output_d, d)
            if not os.path.exists(d_path):
                click.echo(' :: Creating {} directory...'.format(d_path))
                os.mkdir(d_path)

        for f in files:
            f_path = os.path.join(basedir, f)
            o_path = os.path.join(output_d, f)
            if f == '__init__.py':
                click.echo(' :: Copying {} file...'.format(f_path))
                shutil.copyfile(f_path, o_path)
                continue
            if re.match(TO_COMPILE, f):
                subprocess.call(cmd + ['--module', f_path])
                if not include_data:
                    continue
            if re.match(FILES_TO_EXCLUDE, f):
                continue

            click.echo(' :: Copying {} data file...'.format(f_path))
            shutil.copyfile(f_path, o_path)

    click.echo('\nCompiled output: {}'.format(output_d))
    click.echo('Done.')
    sys.exit(0)
