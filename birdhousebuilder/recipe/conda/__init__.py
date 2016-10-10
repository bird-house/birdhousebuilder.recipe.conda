# -*- coding: utf-8 -*-

"""Recipe conda"""
import os
from os.path import join
import yaml
from subprocess import check_output, check_call, CalledProcessError

from zc.buildout.buildout import bool_option

import logging


def split_args(args):
    if args is None:
        return []

    all_args = []
    args = args.strip()
    if args:
        lines = args.split('\n')
        lines = [l.strip() for l in lines]
        for line in lines:
            arg_list = line.split(' ')
            arg_list = [arg.strip() for arg in arg_list]
            all_args.extend(arg_list)
    return all_args


def conda_info(prefix):
    """returns conda infos"""
    cmd = [join(prefix, 'bin', 'conda')]
    cmd.extend(['info', '--json'])
    output = check_output(cmd)
    return yaml.load(output)


def conda_envs(prefix):
    info = conda_info(prefix)
    env_names = [a_env.split('/')[-1] for a_env in info['envs']]
    return dict(zip(env_names, info['envs']))


def conda_env_exists(prefix, env=None):
    """returns True if environment exists otherwise False."""
    if env:
        return env in conda_envs(prefix)
    else:
        return False


class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs conda packages."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.name = options.get('name', name)
        self.options['name'] = self.name

        self.logger = logging.getLogger(self.name)

        # buildout option anaconda-home overwrites default anaconda path
        # TODO: do i realy need this?
        # TODO: guess with "which conda"?
        b_options['anaconda-home'] = b_options.get(
            'anaconda-home', join(os.environ.get('HOME', '/opt'), 'anaconda'))

        # conda prefix
        # either prefix option or CONDA_PREFIX (set by conda env) or
        # anaconda_home
        # TODO: check if prefix is a valid argument (not '' or None)
        self.prefix = self.options.get(
            'prefix',
            os.environ.get('CONDA_PREFIX',
                           os.environ.get('CONDA_ENV_PATH',
                                          b_options['anaconda-home'])))

        # env option can be overwritten by buildout conda-env option
        self.env = self.options.get('env', b_options.get('conda-env', ''))
        self.options['env'] = self.env

        if self.env:
            self.prefix = conda_envs(self.prefix).get(self.env, self.prefix)
        self.options['prefix'] = self.prefix

        # Offline mode, don't connect to the Internet.
        self.offline = bool_option(b_options, 'offline', False)
        if not self.offline:
            self.offline = bool_option(b_options, 'conda-offline', False)

        # Newest mode, don't update dependencies
        self.newest = bool_option(b_options, 'newest', True)

        # Do not search default or .condarc channels. Requires channels.
        self.override_channels = bool_option(
            self.options, 'override-channels', True)

        # Ignore pinned file.
        self.no_pin = bool_option(self.options, 'no-pin', False)

        # channels option or buildout conda-channels option
        self.channels = split_args(
            options.get(
                'channels',
                b_options.get('conda-channels', 'defaults')))

        # make channel list unique
        self.channels = list(set(self.channels))

        # packages
        self.default_pkgs = split_args(
            options.get('default-pkgs', 'python=2 pip'))
        self.pkgs = split_args(options.get('pkgs'))
        self.pip_pkgs = split_args(options.get('pip'))

    def install(self, update=False):
        """
        install conda packages
        """
        offline = self.offline or update
        self.create_env(offline)
        self.install_pkgs(offline)
        self.install_pip(offline)
        return tuple()

    def update(self):
        return self.install(update=True)

    def create_env(self, offline=False):
        if not self.env or conda_env_exists(self.prefix, self.env) or not self.default_pkgs:
            return

        self.logger.info("Creating conda environment %s ...", self.env)

        cmd = [join(self.prefix, 'bin', 'conda')]
        cmd.extend(['create', '-n', self.env])
        if offline:
            cmd.append('--offline')
            self.logger.info("... offline mode ...")
        if not self.newest:
            cmd.append('--no-update-deps')
            self.logger.info("... no update dependencies ...")
        cmd.append('--yes')
        if self.no_pin:
            cmd.append('--no-pin')
            self.logger.info("... no pin ...")
        if self.channels:
            if self.override_channels:
                cmd.append('--override-channels')
            for channel in self.channels:
                cmd.extend(['-c', channel])
        cmd.extend(self.default_pkgs)
        check_call(cmd)

    def install_pkgs(self, offline=False):
        """
        TODO: maybe use conda as python package
        """
        if self.pkgs:
            self.logger.info("Installing conda packages ...")
            cmd = [join(self.prefix, 'bin', 'conda')]
            cmd.append('install')
            if offline:
                cmd.append('--offline')
                self.logger.info("... offline mode ...")
            if not self.newest:
                cmd.append('--no-update-deps')
                self.logger.info("... no update dependencies ...")
            if self.env:
                self.logger.info("... in conda environment %s ...", self.env)
                cmd.extend(['-n', self.env])
            cmd.append('--yes')
            if self.no_pin:
                cmd.append('--no-pin')
                self.logger.info("... no pin ...")
            if self.channels:
                if self.override_channels:
                    self.logger.info('... override channels ...')
                    cmd.append('--override-channels')
                self.logger.info("... with conda channels: %s ...",
                                 ', '.join(self.channels))
                for channel in self.channels:
                    cmd.append('-c')
                    cmd.append(channel)
            cmd.extend(self.pkgs)
            try:
                check_call(cmd)
            except CalledProcessError as err:
                self.logger.error("Conda exited with errors: %s", err.output)
        return self.pkgs

    def install_pip(self, offline=False):
        if not offline and self.pip_pkgs:
            self.logger.info("Installing pip packages in conda env path %s",
                             self.prefix)

            cmd = [join(self.prefix, 'bin', 'pip')]
            cmd.append('install')
            cmd.extend(self.pip_pkgs)
            check_call(cmd)
        return self.pip_pkgs


def uninstall(name, options):
    pass
