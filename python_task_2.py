import pandas as pd
import networkx as nx


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    G = nx.Graph()

    for index, row in df.iterrows():
        G.add_edge(row['id_start'], row['id_end'], weight=row['distance'])

    distance_matrix = nx.floyd_warshall_numpy(G)

    index=[int(item) for item in G.nodes]
    
    df = pd.DataFrame(distance_matrix, index=index, columns=index)

    return df


def unroll_distance_matrix(distance_df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    columns = distance_df.columns

    unrolled_data = []

    for id_start in columns:
        for id_end in columns:
            if id_start != id_end:
                distance = distance_df.loc[id_start, id_end]
                unrolled_data.append([id_start, id_end, distance])

    unrolled_df = pd.DataFrame(unrolled_data, columns=['id_start', 'id_end', 'distance'])

    return unrolled_df

def find_ids_within_ten_percentage_threshold(dataframe, reference_value)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
   
    reference_rows = dataframe[dataframe['id_start'] == reference_value]
    
    avg_distance = reference_rows['distance'].mean()

    lower_bound = avg_distance - (0.1 * avg_distance)
    
    upper_bound = avg_distance + (0.1 * avg_distance)
    
    within_threshold = dataframe[(dataframe['distance'] >= lower_bound) & (dataframe['distance'] <= upper_bound)]
    
    result_ids = sorted(within_threshold['id_start'])
    
    return result_ids



def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }


    for vehicle_type, rate in rate_coefficients.items():
        
        df[vehicle_type] = df['distance'] * rate

    return df



def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    weekday_time_ranges = [
        (time(0, 0, 0), time(10, 0, 0), 0.8),
        (time(10, 0, 0), time(18, 0, 0), 1.2),
        (time(18, 0, 0), time(23, 59, 59), 0.8)
    ]

    weekend_discount_factor = 0.7

    unrolled_df['start_day'] = "Monday"
    unrolled_df['start_time'] = datetime.strptime('00:00:00', '%H:%M:%S').time()
    unrolled_df['end_day'] = "Friday"
    unrolled_df['end_time'] = datetime.strptime('23:59:59', '%H:%M:%S').time()


    for index, row in unrolled_df.iterrows():
        
        id_start = row['id_start']
        
        id_end = row['id_end']

        if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            
            time_ranges = weekday_time_ranges
        else:
            
            time_ranges = [(time(0, 0, 0), time(23, 59, 59), weekend_discount_factor)]

        for start_time, end_time, discount_factor in time_ranges:
            unrolled_df.loc[index, 'start_day'] = row['start_day']
            unrolled_df.loc[index, 'start_time'] = start_time
            unrolled_df.loc[index, 'end_day'] = row['end_day']
            unrolled_df.loc[index, 'end_time'] = end_time

            mask = ((row['start_time'] >= start_time) & (row['end_time'] <= end_time))
            unrolled_df.loc[index, ['moto', 'car', 'rv', 'bus', 'truck']] *= discount_factor

    return unrolled_df
