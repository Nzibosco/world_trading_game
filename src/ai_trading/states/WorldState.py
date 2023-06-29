import pandas as pd
import os

from src.ai_trading.states.Country import Country


class WorldState:

    def __init__(self, world_state_file):
        if not os.path.isfile(world_state_file):
            raise Exception(f"File {world_state_file} does not exist")

        self.state_file = world_state_file
        self.df = pd.read_csv(world_state_file, delimiter='\t')
        self.countries = self.create_country_dict()

    def create_country_dict(self):
        countries = {}
        for _, row in self.df.iterrows():
            country_name = row['Country']
            resources = row.drop('Country').to_dict()
            countries[country_name] = Country(country_name, resources)

        return countries

    def get_country_resources(self, country_name):
        if country_name not in self.countries:
            raise Exception(f"Country {country_name} does not exist")
        return self.countries[country_name].resources

    def get_country_resource_qty(self, country_name, resource_name):
        if country_name not in self.countries:
            raise Exception(f"Country {country_name} does not exist")
        return self.countries[country_name].resources[resource_name]

    def remove_resource(self, resource_name):
        self.df = self.df.drop(resource_name, axis=1)
        self.save()

    def add_resource(self, resource_name, location, values):
        self.df.insert(loc=location, column=resource_name, value=values)
        self.save()

    def update_country_resources(self, resource_name, value, country_name):
        if country_name not in self.countries:
            raise Exception(f"Country {country_name} does not exist")

        self.df.loc[self.df['Country'] == country_name, resource_name] = value
        self.countries[country_name].resources[resource_name] = value  # update the Country object

    def update_save_resources(self, resource_name, value, country_name):
        self.update_country_resources(resource_name, value, country_name)
        self.save()

    def save(self):
        self.df.to_csv(self.state_file, sep='\t', index=False)
