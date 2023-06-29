class Country:
    def __init__(self, name, resources):
        self.name = name
        self.resources = resources

    def __repr__(self):
        country = {'Name': self.name, 'Resources': self.resources}
        return country.__str__()

