# =============================================================================
# Copyright (c) 2015, Cisco Systems, Inc
# All rights reserved.
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
from base import BaseHandler
from utils import import_class
from utils import is_empty
from constants import UNKNOWN
import condoor


def discover_platform_info(ctx):
    conn = condoor.Connection(ctx.hostname, ctx.host_urls)

    try:
        conn.discovery()
        ctx.host.family = conn.family
        ctx.host.platform = conn.platform
        ctx.host.software_platform = get_software_platform(family=conn.family, os_type=conn.os_type)
        ctx.host.software_version = get_software_version(conn.os_version)
        ctx.host.os_type = conn.os_type
        ctx.db_session.commit()
    except condoor.ConnectionError as e:
        pass
    finally:
        conn.disconnect()


def get_software_platform(family, os_type):
    if family == 'ASR9K' and os_type == 'eXR':
        return 'ASR9K-64b'
    else:
        return family


def get_software_version(version):
    # Strip all characters after '[' (i.e., 5.3.2[Default])
    head, sep, tail = version.partition('[')
    return head


class BaseConnectionHandler(BaseHandler):
    def execute(self, ctx):
        conn = condoor.Connection(ctx.hostname, ctx.host_urls)
        try:
            conn.connect()
            ctx.success = True
        except condoor.ConnectionError as e:
            pass


def get_connection_handler():
    return BaseConnectionHandler()


def get_inventory_handler_class(ctx):
    if ctx.host.family == UNKNOWN:
        discover_platform_info(ctx)

    return import_class('handlers.platforms.%s.InventoryHandler' % ctx.host.software_platform)


def get_install_handler_class(ctx):
    if ctx.host.family == UNKNOWN:
        discover_platform_info(ctx)

    return import_class('handlers.platforms.%s.InstallHandler' % ctx.host.software_platform)
