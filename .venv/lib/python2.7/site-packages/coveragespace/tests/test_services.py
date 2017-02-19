# pylint: disable=missing-docstring,unused-variable,unused-argument,expression-not-assigned,singleton-comparison

from expecter import expect

from coveragespace import services


def describe_detected():

    def when_off_ci(monkeypatch):
        monkeypatch.delenv('CI', raising=False)
        monkeypatch.delenv('CONTINUOUS_INTEGRATION', raising=False)
        monkeypatch.delenv('TRAVIS', raising=False)
        monkeypatch.delenv('APPVEYOR', raising=False)

        expect(services.detected()) == False

    def when_on_ci(monkeypatch):
        monkeypatch.setenv('TRAVIS', 'true')

        expect(services.detected()) == True
