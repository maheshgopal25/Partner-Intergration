from .Specs import Specs


class SpecsMaster(object):
    Request = list(Specs.return_fields())


specsmaster = SpecsMaster()
