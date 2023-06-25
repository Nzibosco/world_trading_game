import pandas as pd

class ResourceWeight:

    def __init__(self, template_file):
        self.template_file = template_file
        self.df = pd.read_csv(self.template_file, delimiter='\t')
        self.weights = self.df.set_index('Resource')['Weight'].to_dict()

    def get_weight(self, res_name):
        return self.weights[res_name]

    def set_weight(self, res_name, weight):
        self.weights[res_name] = weight
        self.df.loc[self.df['Resource'] == res_name, 'Weight'] = weight
        self._write_to_csv()

    def add_resource(self, res_name, weight):
        self.weights[res_name] = weight
        self.df = self.df.append({'Resource': res_name, 'Weight': weight}, ignore_index=True)
        self._write_to_csv()

    def remove_resource(self, res_name):
        if res_name in self.weights:
            del self.weights[res_name]
            self.df = self.df[self.df.Resource != res_name]
            self._write_to_csv()

    def _write_to_csv(self):
        self.df.to_csv(self.template_file, sep='\t', index=False)


#resource_weights = ResourceWeight('../resources/resource_weights.csv')
# print(resource_weights.get_weight('Population'))
# resource_weights.set_weight('MetallicAlloys', 0.7)
# resource_weights.set_weight('Timber', 0.3)
# resource_weights.set_weight('MetallicElements', 0.4)
#resource_weights.set_weight('Population', 0.1)
