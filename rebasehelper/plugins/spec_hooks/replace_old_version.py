# -*- coding: utf-8 -*-
#
# This tool helps you rebase your package to the latest version
# Copyright (C) 2013-2019 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Authors: Petr Hráček <phracek@redhat.com>
#          Tomáš Hozza <thozza@redhat.com>
#          Nikola Forró <nforro@redhat.com>
#          František Nečas <fifinecas@seznam.cz>

import urllib.parse

from rebasehelper.types import Options
from rebasehelper.plugins.spec_hooks import BaseSpecHook


class ReplaceOldVersion(BaseSpecHook):
    """SpecHook for replacing occurrences of old version string."""

    OPTIONS: Options = [
        {
            "name": ["--replace-old-version-with-macro"],
            "default": False,
            "switch": True,
            "help": "replace old version string with %%{version} instead of new version string",
        },
    ]

    @classmethod
    def _is_local_source(cls, line):
        """Checks if a line contains a local source.

        Args:
            line (str): Line to be checked.

        Returns:
            bool: Whether the line contains a local source

        """
        if not (line.startswith('Patch') or line.startswith('Source')):
            return False
        source = line.split()[1]
        return not urllib.parse.urlparse(source).scheme

    @classmethod
    def _replace(cls, line, old, new, replace_with_macro=False):
        """Replaces occurrences of old version on a line with new version.

        Args:
            line (str): String to replace the version in.
            old (str): Old version string.
            new (str): New version string.
            replace_with_macro (bool): Whether %{version} macro should
                be used as a substitution.

        Returns:
            str: Modified line with replaced old version strings.

        """
        if cls._is_local_source(line):
            return line
        return line.replace(old, '%{version}' if replace_with_macro else new)

    @classmethod
    def run(cls, spec_file, rebase_spec_file, **kwargs):
        old_version = spec_file.get_version()
        new_version = rebase_spec_file.get_version()
        replace_with_macro = kwargs.get('replace_old_version_with_macro')
        for sec_name, section in rebase_spec_file.spec_content.sections:
            if sec_name.startswith('%changelog'):
                continue
            for index, line in enumerate(section):
                start, end = spec_file.spec_content.get_comment_span(line, sec_name)
                updated_line = cls._replace(line[:start], old_version, new_version, replace_with_macro)
                section[index] = updated_line + line[start:end]

        rebase_spec_file.save()