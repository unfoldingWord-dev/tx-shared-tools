# -*- coding: utf8 -*-
#
#  Copyright (c) 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Richard Mahn <richard_mahn@wycliffeassociates.org>

import json

from boto3 import Session

class LambdaHandler(object):
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region_name='us-west-2'):
        self.session = Session(aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               region_name=aws_region_name)
        self.client = self.session.client('lambda')

    def invoke(self, function_name, payload):
        return self.client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(payload)
        )
