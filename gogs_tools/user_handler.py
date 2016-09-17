# -*- coding: utf8 -*-
#
#  Copyright (c) 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Richard Mahn <richard_mahn@wycliffeassociates.org>

import gogs_client


def authenticate_user_token(gogs_url, user_token):
    gogs_api = gogs_client.GogsApi(gogs_url)
    return gogs_api.valid_authentication(gogs_client.GogsToken(user_token))
