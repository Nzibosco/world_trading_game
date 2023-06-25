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
    raw_quality = 0

    for resource, quantity in country.resources.items():
        if quantity > 0:  # only consider resources with quantity greater than 0
            weight = resource_weights.get_weight(resource)
            raw_quality += weight * quantity

    # Calculate the minimum and maximum possible quality scores
    min_raw_quality = 0  # when all quantities are zero
    max_raw_quality = sum([weight * max(country.resources.values()) for weight in resource_weights.weights.values()])

    # Linearly normalize the quality score to be between 0 and 1
    if min_raw_quality == max_raw_quality:
        quality = 0
    else:
        quality = (raw_quality - min_raw_quality) / (max_raw_quality - min_raw_quality)

    # Keep floating point precision to 2
    quality = round(quality, 2)

    return quality
