class LBFunction:
    def __init__(self, versions, value=None):
        self.versions = versions
        self.value = value
    
    def default(self):
        return self.versions["^def"]

    def version(self, version):
        return self.versions[version]
