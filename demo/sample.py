"""A sample module."""


def function(value):
    """A function with branches to demonstrate branch coverage reporting."""
    if value is True:
        return 'True'
    elif value is False:
        return 'False'
    else:
        return 'None'


def another_function(text):
    """Another sample function."""
    print(text)
    if text:
        return True
