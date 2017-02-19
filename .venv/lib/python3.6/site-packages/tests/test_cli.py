# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned

from __future__ import unicode_literals

import os
import sys

import pytest
import scripttest
from expecter import expect
import six

SLUG = "jacebrowning/coverage-space-cli-demo"


@pytest.fixture
def env(tmpdir):
    path = str(tmpdir.join('test'))
    env = scripttest.TestFileEnvironment(path)
    env.environ.pop('CI', None)
    env.environ.pop('CONTINUOUS_INTEGRATION', None)
    env.environ.pop('TRAVIS', None)
    env.environ.pop('APPVEYOR', None)
    return env


def cli(env, *args):
    prog = os.path.join(os.path.dirname(sys.executable), 'coverage.space')
    cmd = env.run(prog, *args, expect_error=True)
    six.print_(cmd)
    return cmd


def describe_cli():

    def it_fails_when_missing_arguments(env):
        cmd = cli(env)

        expect(cmd.returncode) == 1
        expect(cmd.stderr).contains("Usage:")

    def describe_update():

        @pytest.fixture
        def slug():
            return SLUG + "/update"

        def it_can_update_metrics(env, slug):
            cmd = cli(env, slug, 'unit', '100')

            expect(cmd.returncode) == 0
            expect(cmd.stderr) == ""
            expect(cmd.stdout) == ""

        def it_indicates_when_metrics_decrease(env, slug):
            cmd = cli(env, slug, 'unit', '0')

            expect(cmd.returncode) == 0
            expect(cmd.stderr) == ""
            expect(cmd.stdout).contains("coverage decreased")
            expect(cmd.stdout).contains(
                "To reset metrics, run: coverage.space " + slug + " --reset"
            )

        def it_fails_when_metrics_decrease_if_requested(env, slug):
            cmd = cli(env, slug, 'unit', '0', '--exit-code')

            expect(cmd.returncode) == 1
            expect(cmd.stderr) == ""
            expect(cmd.stdout).contains("coverage decreased")

        def it_always_display_metrics_when_verbose(env, slug):
            cmd = cli(env, slug, 'unit', '100', '--verbose')

            expect(cmd.returncode) == 0
            expect(cmd.stderr) != ""  # expect lots of logging
            expect(cmd.stdout).contains("coverage increased")

        def it_skips_when_running_on_ci(env, slug):
            env.environ['CI'] = 'true'

            cmd = cli(env, slug, 'unit', '0', '--exit-code')

            expect(cmd.returncode) == 0
            expect(cmd.stderr).contains("Coverage check skipped")
            expect(cmd.stdout) == ""

    def describe_reset():

        @pytest.fixture
        def slug():
            return SLUG + "/reset"

        def it_can_reset_metrics(env, slug):
            cmd = cli(env, slug, '--reset')

            expect(cmd.returncode) == 0
            expect(cmd.stderr) == ""
            expect(cmd.stdout).contains("coverage reset")
