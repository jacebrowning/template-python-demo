from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("TemplateDemo").version
except DistributionNotFound:
    __version__ = "(local)"

del DistributionNotFound
del get_distribution
