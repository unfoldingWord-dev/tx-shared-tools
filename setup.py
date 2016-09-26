import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(f_name):
    return open(os.path.join(os.path.dirname(__file__), f_name)).read()

setup(
    name="tx-shared-tools",
    packages=['aws_tools', 'client_tools', 'door43_tools', 'general_tools', 'gogs_tools'],
    version="0.1.23",
    author="unfoldingWord",
    author_email="unfoldingword.org",
    description="A collection of useful scripts abd classes for tX",
    url="https://github.org/unfoldingWord-dev/tx-shared-tools",
    license="MIT",
    keywords=['unfoldingWord', 'tx', 'tools'],
    long_description=read('README.rst'),
    classifiers=[],
    install_requires=[
        'boto3',
        'bs4',
        'gogs_client'
    ]
)



{"data": {"job": {"input_format": "md", "convert_module": "tx-md2html_convert", "started_at": "2016-09-26T16:04:48Z", "errors": [], "job_id": "8cbc485e80f61f922384870ff9776d1c146f255bfcaf33de0e4a5fde185a80ff", "output_expiration": null, "links": {"href": "https://test-api.door43.org/tx/job/8cbc485e80f61f922384870ff9776d1c146f255bfcaf33de0e4a5fde185a80ff", "method": "GET", "rel": "self"}, "source": "https://s3-us-west-2.amazonaws.com/test-tx-webhook/tx-webhook-client/f1aee2ed-8402-11e6-a525-938e985896fb.zip", "status": "started", "warnings": [], "output_format": "html", "expires_at": "2016-09-27T16:04:47Z", "user": "txwebhook", "cdn_file": "tx/job/f1ff9afd-8402-11e6-ac98-4561c4f27191.zip", "cdn_bucket": "test-cdn.door43.org", "log": ["Started job 8cbc485e80f61f922384870ff9776d1c146f255bfcaf33de0e4a5fde185a80ff at 2016-09-26T16:04:48Z"], "ended_at": null, "success": false, "created_at": "2016-09-26T16:04:47Z", "callback": "https://test-api.door43.org/client/callback", "eta": "2016-09-26T16:05:07Z", "output": "https://test-cdn.door43.org/tx/job/f1ff9afd-8402-11e6-ac98-4561c4f27191.zip", "identifier": "richmahn/en-obs/f395e46e0e", "resource_type": "obs"}}}