# txManager functions

import hashlib

from datetime import datetime
from datetime import timedelta

from tx_tools.db_handler import TxDBHandler
from tx_tools.tx_job import TxJob
from tx_tools.tx_module import TxModule
from gogs_tools.gogs_handler import GogsHandler
from aws_tools.aws_handler import AwsHandler

class TxManager(object):
    job_table_name = 'tx-job'
    module_table_name = 'tx-module'
    job_log_prefix = 'tx-manager'

    def __init__(self, api_url, gogs_url, cdn_url, cdn_bucket, aws_access_key_id=None, aws_secret_access_key=None):
        self.api_base_url = api_url
        self.cdn_base_url = cdn_url
        self.cdn_bucket = cdn_bucket

        self.module_db = TxDBHandler(self.job_table_name)
        self.job_db = TxDBHandler(self.module_table_name)
        self.gogs_handler = GogsHandler(gogs_url)
        self.aws_handler = AwsHandler(aws_access_key_id, aws_secret_access_key)

    def get_user(self, user_token):
        return self.gogs_handler.get_user(user_token)

    def get_converter_module(self, job):
        modules = TxDBHandler().query_modules()
        for module in modules:
            if job.resource_type in module['resource_types']:
                if job.input_format in module['input_format']:
                    if job.output_format in module['output_format']:
                        return module
        return None

    def setup_job(self, data):
        if 'user_token' not in data:
            raise Exception('"user_token" not given.')

        user = self.get_user(data['user_token'])

        if not user:
            raise Exception('Invalid user_token. User not found.')

        data['user'] = user
        del data['user_token']

        job = TxJob(data)

        if not job.cdn_bucket:
            raise Exception('"cdn_bucket" not given.')
        if job.source:
            raise Exception('"source" url not given.')
        if not job.resource_type:
            raise Exception('"resource_type" not given.')
        if not job.input_format:
            raise Exception('"input_format" not given.')
        if not job.output_format:
            raise Exception('"output_format" not given.')

        module = self.get_converter_module(job)

        if not module:
            raise Exception('No converter was found to convert {0} from {1} to {2}'.format(job.resource_type, job.input_format, job.output_format))

        job.convert_module = module
        output_file = 'tx/job/{0}.zip'.format(job.job_id)  # All conversions must result in a ZIP of the converted file(s)
        job.output = '{0}/{1}'.format(self.cdn_base_url, output_file)

        created_at = datetime.utcnow()
        expires_at = created_at + timedelta(days=1)
        eta = created_at + timedelta(seconds=20)

        job.created_at = created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        job.expires_at = expires_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        job.eta = eta.strftime("%Y-%m-%dT%H:%M:%SZ")
        job.job_status = 'requested'

        job_id = hashlib.sha256('{0}-{1}-{2}'.format(data['user_token'], user, created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))).hexdigest()
        job.job_id = job_id

        job.links = {
            "href": "{0}/tx/job/{1}".format(self.api_url, job_id),
            "rel": "self",
            "method": "GET"
        }

        # Saving this to the DynamoDB will start trigger a DB stream which will call
        # tx-manager again with the job info (see run() function)
        self.insert_job(job)

        return {
            "job": job.get_db_data(),
            "links": [
                {
                    "href": "{0}/tx/job".format(self.api_url),
                    "rel": "list",
                    "method": "GET"
                },
                {
                    "href": "{0}/tx/job".format(self.api_url),
                    "rel": "create",
                    "method": "POST"
                },
            ],
        }

    def list_jobs(self, data, must_be_authenticated = True):
        if must_be_authenticated:
            if 'user_token' not in data:
                raise Exception('"user_token" not given.')
            user = self.get_user(data['user_token'])
            if not user:
                raise Exception('Invalid user_token. User not found.')
            data['user'] = user
            del data['user_token']
        return self.job_db.query_items(self, data)

    def get_endpoints(self):
        return {
            "version": "1",
            "links": [
                {
                    "href": "{0}/tx/job".format(self.api_url),
                    "rel": "list",
                    "method": "GET"
                },
                {
                    "href": "{0}/tx/job".format(self.api_url),
                    "rel": "create",
                    "method": "POST"
                },
            ]
        }

    def start_job(self, job_id):
        job = self.get_job(job_id)

        if not job:
            raise Exception('Job not found: {0}'.format(job_id))

        # Only start the job if a started timestamp hasn't been set
        if job.job_status != 'requested' or job.start_at:
            return False

        job.start_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        job.status = 'started'
        job.log_message('Started job {0} at {1}'.format(job_id, job.started_at), self.job_log_prefix)

        try:
            self.update_job(job)

            module = self.get_converter_module(job)
            if not module:
                raise Exception('No converter was found to convert {0} from {1} to {2}'.format(job.resourse_type, job.import_format, job.output_format))

            job.converter_module = module
            self.update_job(job)

            payload = {
                'data': {
                    'job': job,
                }
            }
            print("Payload to {0}:".format(module['name']))
            print(payload)

            job.log_message('Telling module {0} to convert {1} and put at {2}'.format(job.converter_module, job.source, job.output), self.job_log_prefix)
            response = self.aws_handler.lambda_invoke(module['name'], payload)
            print("Response payload from {0}:".format(module['name']))
            print(response)

            if 'errorMessage' in response:
                self.errors.append("{0}: {1}".format(module['name'], response['errorMessage']))
            else:
                self.log.extend(response['log'])
                self.errors.extend(response['errors'])
                self.warnings.extend(response['warnings'])

            if response['errors']:
                self.log_message('{0} function returned with errors.'.format(module['name']))
            elif response['warnings']:
                self.log_message('{0} function returned with warnings.'.format(module['name']))
            if response['errors']:
                self.log_message('{0} function returned.'.format(module['name']))
        except Exception as e:
            self.error_message(e.message)

        if len(self.errors):
            success = False
            job_status = "failed"
            message = "Conversion failed"
        elif len(self.warnings) > 0:
            success = True
            job_status = "warnings"
            message = "Conversion successful with warnings"
        else:
            success = True
            job_status = "success"
            message = "Conversion successful"

        self.log_message(message)

        ended_at_timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.log_message('Finished job {0} at {1}'.format(job['job_id'], ended_at_timestamp))

        response = self.job_db.update_item({'job_id': job['job_id'],
            },
            UpdateExpression="set ended_at = :ended_at, success = :success, job_status = :job_status, message = :message, logs = :logs, errors = :errors, warnings = :warnings, deployed = :deployed",
            ExpressionAttributeValues={
                ':ended_at': ended_at_timestamp,
                ':success': success,
                ':job_status': job_status,
                ':message': message,
                ':logs': json.dumps(self.log),
                ':errors': json.dumps(self.errors),
                ':warnings': json.dumps(self.warnings),
                ':deployed': False
            }
        )
        print("Updated tx-job with ended_timestamp, success, job_status, message, logs, errors and warnings.")

        response = job_table.get_item(
            Key={
                'job_id': job['job_id']
            }
        )
        job = response['Item']

        response = {
            "job_id": job["job_id"],
            "identifier": job["identifier"],
            "success": success,
            "status": job_status,
            "message": message,
            "output": job["output"],
            "ouput_expiration": job["output_expiration"],
            "log": self.log,
            "warnings": self.warnings,
            "errors": self.errors,
            "created_at": job["created_at"],
            "started_at": job["started_at"],
            "ended_at": ended_at_timestamp
        }

        if 'callback' in job and job['callback'] and job['callback'].startswith('http'):
            callback_url = job['callback']
            headers = {"content-type": "application/json"}
            print('Making callback to {0} with payload:'.format(callback_url))
            print(response)
            response = requests.post(callback_url, json=response, headers=headers)
            print('finished.')

        return response


    def insert_job(self, job):
        job_data = job.get_db_data()
        self.job_db.insert_item(job_data)

    def get_job(self, job_id):
        return self.job_db.get_item({'job_id':job_id})

    def update_job(self, job):
        return self.job_db.update_item({'job_id':job.job_id}, job.get_db_data())

    def delete_job(self, job):
        return self.job_db.delete_item({'job_id':job.job_id})
