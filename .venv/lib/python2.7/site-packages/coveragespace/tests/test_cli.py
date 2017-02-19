# pylint: disable=unused-variable,expression-not-assigned,singleton-comparison

from mock import patch, Mock
from expecter import expect

from coveragespace import cli


def describe_call():

    @patch('coveragespace.cache.Cache.get', Mock())
    def it_handles_invalid_response():
        expect(cli.call('slug', 'metric', 42)) == False

    @patch('coveragespace.cache.Cache.get', Mock(return_value=None))
    @patch('coveragespace.cache.Cache.set', Mock(return_value=None))
    @patch('time.sleep', Mock())
    @patch('requests.put')
    def it_retries_500s(requests_put):
        requests_put.return_value = Mock(status_code=500)

        cli.call('slug', 'metric', 42)

        expect(requests_put.call_count) == 3
