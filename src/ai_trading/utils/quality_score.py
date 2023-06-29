# Function to calculate state quality for all countries in the world
def average_quality_score(world_state, resource_weights):
    total_quality = 0
    num_countries = len(world_state.countries)

    for country in world_state.countries.values():
        total_quality += calculate_country_quality_score(country, resource_weights)

    if num_countries != 0:
        average_quality = total_quality / num_countries
    else:
        average_quality = 0

    # Keep floating point precision to 2
    average_quality = round(average_quality, 2)

    return average_quality


# Function to calculate state quality by country
def calculate_country_quality_score(country, resource_weights):
    if 'Population' not in country.resources:
        raise ValueError(f"calculate_country_quality_score():: Error - 'Population' resource not found for country {country.name}")

    population = country.resources.get('Population')
    if population <= 0:
        raise ValueError(f"calculate_country_quality_score():: Error - 'Population' must be greater than zero for country {country.name}")

    raw_quality = 0
    for resource, quantity in country.resources.items():
        if resource != 'Population':  # avoid counting population in the raw_quality calculation
            weight = resource_weights.get_weight(resource)
            raw_quality += weight * quantity

    # Quality score is the sum of resource*weight divided by population
    quality = raw_quality / population

    # Keep floating point precision to not more than 4
    quality = round(quality, 4)

    return quality
