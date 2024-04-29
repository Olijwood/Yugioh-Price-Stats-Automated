from datetime import date

def stats_for_simulated_set(simulated_values, set_booster_price):
    num_values = len(simulated_values)

    mean_value = round((sum(simulated_values) / len(simulated_values)),2)
    
    sorted_values = sorted(simulated_values)
    if num_values % 2 == 0:
        median_value = (sorted_values[num_values // 2 - 1] + sorted_values[num_values // 2]) / 2
    else:
        median_value = sorted_values[num_values // 2]


    higher_values = sum(value > set_booster_price for value in simulated_values)
    chance_higher_value = higher_values / num_values

    date_updated = date.today()

    set_data = {
        'mean_value': mean_value,
        'median_value': median_value,
        'chance_higher_value': chance_higher_value,
        'date_updated': date_updated
    }
    return set_data