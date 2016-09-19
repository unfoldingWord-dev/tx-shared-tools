# -*- coding: utf8 -*-
#
#  Copyright (c) 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Richard Mahn <richard_mahn@wycliffeassociates.org>

import boto3
import json


class AwsHandler(object):
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.lambda_client = lambda_client = boto3.client('lambda')

    def lambda_invoke(self, function_name, payload):
        return self.lambda_client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(payload)
        )
