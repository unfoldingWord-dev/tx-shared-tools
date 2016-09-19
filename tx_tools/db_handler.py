# -*- coding: utf8 -*-
#
#  Copyright (c) 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Richard Mahn <richard_mahn@wycliffeassociates.org>

import boto3

from six import iteritems
from boto3.dynamodb.conditions import Attr, Key

class TxDBHandler(object):

    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_item(self, key):
        response = self.table.get_item(
            Key=key
        )
        if 'Item' in response:
            return response['Item']
        else:
            return None

    def insert_item(self, data):
        self.table.put_item(
            Item=data
        )

    def update_item(self, key, data):
        expressions = []
        values = {}

        for field, value in iteritems(data):
            expressions.append('{0} = :{0}'.format(field))
            values[':{0}'.format(field)] = value

        return self.table.update_item(
            Key=key,
            UpdateExpression='SET {0}'+format(', '.join(expressions)),
            ExpressionAttributeValues=values
        )

    def delete_item(self, key):
        return self.table.delete_item(
            Key=key
        )

    def query_items(self, query=None, only_fields_with_values=True):
        filter_expression = None
        if query and len(query) > 1:
            for field, value in iteritems(query):
                if isinstance(value, dict) and 'condition' in value and 'value' in value:
                    condition = value['condition']
                    value = value['value']
                else:
                    condition = 'eq'

                if not value and only_fields_with_values:
                    continue

                if condition == 'eq':
                    filter_expression &= Attr(field).eq(value)
                if condition == 'ne':
                    filter_expression &= Attr(field).ne(value)
                if condition == 'lt':
                    filter_expression &= Attr(field).lt(value)
                if condition == 'lte':
                    filter_expression &= Attr(field).lte(value)
                if condition == 'gt':
                    filter_expression &= Attr(field).gt(value)
                if condition == 'gte':
                    filter_expression &= Attr(field).gte(value)
                if condition == 'begins_with':
                    filter_expression &= Attr(field).begins_with(value)
                if condition == 'between':
                    filter_expression &= Attr(field).between(value)
                if condition == 'ne':
                    filter_expression &= Attr(field).ne(value)
                if condition == 'is_in':
                    filter_expression &= Attr(field).is_in(value)
                if condition == 'contains':
                    filter_expression &= Attr(field).contains(value)
                else:
                    raise Exception('Invalid filter condition: {0}'.format(condition))

        response = self.table.scan(
            FilterExpression=filter
        )
        if response and 'Items' in response:
            return response['Items']
        else:
            return None
