# -*- coding: utf8 -*-
#
#  Copyright (c) 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Richard Mahn <richard_mahn@wycliffeassociates.org>

import os
import boto3

from boto3.session import Session


class S3Handler(object):
    
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, aws_region_name='us-west-2'):
        if aws_access_key_id and aws_secret_access_key:
            session = Session(aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   region_name=aws_region_name)
            self.resource = session.resource('s3')
            self.resource = session.resource('s3')
        else:
            self.resource = boto3.resource('s3')
            self.client = boto3.client('s3')

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
                    self.resource.meta.client.download_file(bucket, f.get('Key'), local + os.sep + f.get('Key'))

