class Specs(object):
    Id = None
    ParamName = None
    JsonTag = None
    Min_len = None
    Max_len = None
    IsMandatory = None
    DataType = None

    @classmethod
    def return_fields(cls):
        return cls.Id, cls.Max_len, cls.Min_len, cls.DataType, cls.IsMandatory, cls.ParamName, cls.JsonTag


specs = Specs()
