class Prepper:
    column_mapping = None

    def __init__(self, ifile):
        self.ifile = ifile

    def prep_file(self):
        return NotImplemented

    def __init_subclass__(cls):
        setattr(Prepper, cls.__name__, cls)

    @classmethod
    def from_file(cls, ifile, file_type):
        return {
            'ups': cls.UpsPrepper,
            'givens': cls.GivensPrepper,
            'freight': cls.FreightPrepper,
        }.get(file_type)(ifile)
