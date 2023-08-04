def standardize_name(name):
    # Remove any periods
    name_without_periods = name.replace('.', '')
    # Split the name by whitespace, take the first two parts if they exist, and join them back together
    return ' '.join(name_without_periods.split()[:2])
