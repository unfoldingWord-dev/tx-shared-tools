# -*- coding: utf8 -*-
#
#  Copyright (c) 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Richard Mahn <richard_mahn@wycliffeassociates.org>

import os

from boto3.session import Session


class S3Handler(object):
    
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region_name='us-west-2'):
        self.session = Session(aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               region_name=aws_region_name)
        self.client = self.session.client('s3')
        self.resource = self.session.resource('s3')

    # Downloads all the files in S3 that have a prefix of `dist` from `bucket` to the `local` directory
    def download_dir(self, bucket, dist, local):
        paginator = self.client.get_paginator('list_objects')
        for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
            if result.get('CommonPrefixes') is not None:
                for subdir in result.get('CommonPrefixes'):
                    self.download_dir(bucket, subdir.get('Prefix'), local)
            if result.get('Contents') is not None:
                for f in result.get('Contents'):
                    if not os.path.exists(os.path.dirname(local + os.sep + f.get('Key'))):
                        os.makedirs(os.path.dirname(local + os.sep + f.get('Key')))
                    self.resource.meta.self.client.download_file(bucket, f.get('Key'), local + os.sep + f.get('Key'))

