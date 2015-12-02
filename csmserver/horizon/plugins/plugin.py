# =============================================================================
# plugin.py - Generic Plugin Class
#
# Copyright (c) 2015, Cisco Systems
# All rights reserved.
#
# Author: Klaudiusz Staniek
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
# =============================================================================


class PluginError(Exception):
    pass


class IPlugin(object):

    """
    This is a main Plugin template class providing interface to other plugins
    """
    NAME = "GENERIC"
    DESCRIPTION = "Generic Plugin Template"
    TYPE = None
    VERSION = "1.0.0"
    FAMILY = ["ASR9K"]

    @staticmethod
    def save_to_file(data, outfile):
        with open(outfile, "w") as f:
            f.write(data)
        return

    @staticmethod
    def start(manger, device, *args, **kwargs):
        """
        Start the plugin
        Must be overridden by the plugin class child implementation
        """
        raise NotImplementedError

    @property
    def description(self):
        return (self.DESCRIPTION[:35] + '..') if len(self.DESCRIPTION) > 37 else self.DESCRIPTION