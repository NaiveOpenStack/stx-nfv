#
# Copyright (c) 2015-2016 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
import httplib
import urllib2

from nfv_common import debug

DLOG = debug.debug_get_logger('nfv_vim.api.openstack')


def rest_api_request(token, method, url, headers=None, body=None):
    """
    Make a rest-api request
    """
    headers_per_hop = ['connection', 'keep-alive', 'proxy-authenticate',
                       'proxy-authorization', 'te', 'trailers',
                       'transfer-encoding', 'upgrade']

    try:
        request_info = urllib2.Request(url)
        request_info.get_method = lambda: method

        if headers is not None:
            for header_type, header_value in headers.items():
                # Allow the Content-Length to be set by urllib2
                if 'Content-Length' != header_type and 'Host' != header_type:
                    request_info.add_header(header_type, header_value)

        request_info.add_header("Accept", "application/json")

        if token is not None:
            request_info.add_header("X-Auth-Token", token.get_id())

        if body is not None and '' != body:
            request_info.add_data(body)

        # Enable Debug
        # handler=urllib2.HTTPHandler(debuglevel=1)
        # opener = urllib2.build_opener(handler)
        # urllib2.install_opener(opener)

        request = urllib2.urlopen(request_info)

        headers = list()  # list of tuples
        for key, value in request.info().items():
            if key not in headers_per_hop:
                cap_key = '-'.join((ck.capitalize() for ck in key.split('-')))
                headers.append((cap_key, value))

        response = request.read()
        request.close()
        return httplib.OK, headers, response

    except urllib2.HTTPError as e:
        if e.fp is not None:
            headers = list()  # list of tuples
            for key, value in e.fp.info().items():
                if key not in headers_per_hop:
                    cap_key = '-'.join((ck.capitalize()
                                        for ck in key.split('-')))
                    headers.append((cap_key, value))

            response = e.fp.read()
            return e.code, headers, response

        return e.code, None, e.reason
