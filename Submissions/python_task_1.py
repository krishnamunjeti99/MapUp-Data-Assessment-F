import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

    df = df.pivot(index='id_1', columns='id_2', values='car')
    df.values[[range(len(df))], [range(len(df))]] = 0
    
    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

  
    type_counts = df['car_type'].value_counts().to_dict()

    Dict = dict(sorted(type_counts.items()))

    return Dict



def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    
    bus_mean = df['bus'].mean()

    bus_indices = df[df['bus'] > 2 * bus_mean].index.tolist()

    bus_indices.sort()

    return bus_indices


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    truck_avg = df['truck'].mean()
    
    filtered_df = df[df['truck'] > 7]
    
    unique_routes = filtered_df['route'].unique()

    sorted_routes = sorted(unique_routes)

    return sorted_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    
    matrix = matrix.round(1)

    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
     df1['start_timestamp'] = pd.to_datetime(df1['startDay'] + ' ' + df1['startTime'], errors = 'coerce')

    df1['end_timestamp'] = pd.to_datetime(df1['endDay'] + ' ' + df1['endTime'], errors = 'coerce')

    grouped = df1.groupby(['id', 'id_2'])
    
    completeness = grouped.apply(lambda x: (x['end_timestamp'].max() - x['start_timestamp'].min()).total_seconds() >= 86400 * 7)

    return completeness
