"""
this script cleans and merges csv files for usage in 
airline network generation and ford fulkerson algorithm implementation

"""
import pandas as pd

#file paths
AIRLINE_DETAILS_PATH  = "a_data_cleaning/datasets/airline_details.csv"
COUNTRY_REGIONS_PATH  = "a_data_cleaning/datasets/country_regions.csv"
IATA_ICAO_PATH  = "a_data_cleaning/datasets/iata_icao.csv"
AIRCRAFT_CAPACITIES_PATH  = "a_data_cleaning/datasets/aircraft_capacities.csv"

#loading dataframes from csv files
airline_details_df = pd.read_csv(AIRLINE_DETAILS_PATH)
country_regions_df = pd.read_csv(COUNTRY_REGIONS_PATH)
iata_icao_df = pd.read_csv(IATA_ICAO_PATH)
aircraft_capacities_df = pd.read_csv(AIRCRAFT_CAPACITIES_PATH)

#merging airport geographical data
geographic_merge_df = pd.merge(
    iata_icao_df[['country_code', 'iata','airport', 'latitude', 'longitude']],
    country_regions_df[['name', 'alpha-2', 'region', 'sub-region']],
    left_on='country_code',
    right_on='alpha-2'
)
geographic_merge_df.drop(axis=1, columns=['alpha-2', 'country_code'], inplace=True)

#cleaning airline flight routes dataset for merging
airline_details_df.drop(axis=1, columns=[
    'Date', 
    'Flight_Number',
    'Seat',
    'Seat_Type',
    'Class',
    'Reason',
    'Registration',
    'Trip',
    'Note',
    'From_OID',
    'To_OID', 
    'Airline_OID', 
    'Plane_OID'
], inplace=True)
airline_details_df.dropna(inplace=True)

airline_details_df['Plane'] = airline_details_df['Plane'].str.split()
airline_details_df = airline_details_df.explode('Plane')

#merging flight routes network dataset with geographical information of airports
#merging for source airports
cleaned_df = pd.merge(
    airline_details_df,
    geographic_merge_df,
    left_on='From',
    right_on='iata',
    suffixes=("", "_from")
)

#merging for destination airports
cleaned_df = pd.merge(
    cleaned_df,
    geographic_merge_df,
    left_on='To',
    right_on='iata',
    suffixes=("_from", "_to")
)

#merging aircraft capacities dataset with flight routes network dataset
cleaned_df = pd.merge(
    cleaned_df,
    aircraft_capacities_df,
    left_on='Plane',
    right_on='model_code'
)

# converting flight duration from HH:MM to hours in decimal format
def convert_to_hours(duration):
    """converts HH:MM to hrs in decimals"""
    hours, minutes = map(int, duration.split(':'))
    return hours + minutes / 60

cleaned_df['Duration'] = cleaned_df['Duration'].apply(convert_to_hours)
cleaned_df.dropna(subset=['Duration'], inplace=True)


#cleaning by removing redundant colums from the merge
cleaned_df.drop(axis=1, columns=[
    'From', 'To', 'model_code'
], inplace=True)

cleaned_df.dropna(inplace=True)

#renaming columns
cleaned_df.rename(columns={
    #source airport information
    'iata_from':'src_airport_code',
    'airport_from':'src_airport_name',
    'latitude_from':'src_airport_lat',
    'longitude_from':'src_airport_lon',
    'name_from':'src_airport_ctry',
    'region_from':'src_airport_rgn',
    'sub-region_from':'src_airport_sbrgn',

    #destinaiton airport information
    'iata_to':'dstn_airport_code',
    'airport_to':'dstn_airport_name',
    'latitude_to':'dstn_airport_lat',
    'longitude_to':'dstn_airport_lon',
    'name_to':'dstn_airport_ctry',
    'region_to':'dstn_airport_rgn',
    'sub-region_to':'dstn_airport_sbrgn',

    #flight information
    'Airline':'airline', 
    'Distance':'flight_distance', 
    'Duration':'flight_duration', 
    'Plane':'aircraft_model_code',
    'model_name':'aircraft_model_name',
    'seating_cap':'capacity'
}, inplace=True)

#reordering columns
cleaned_df = cleaned_df[[
    # Source airport information
    'src_airport_code', 'src_airport_name', 'src_airport_lat', 'src_airport_lon',
    'src_airport_ctry', 'src_airport_rgn', 'src_airport_sbrgn',

    # Destination airport information
    'dstn_airport_code', 'dstn_airport_name', 'dstn_airport_lat', 'dstn_airport_lon',
    'dstn_airport_ctry', 'dstn_airport_rgn', 'dstn_airport_sbrgn',

    # Flight information
    'airline', 'flight_distance', 'flight_duration',
    'aircraft_model_code', 'aircraft_model_name', 'capacity'
]]

#exporting to csv
cleaned_df.to_csv('a_data_cleaning/flight_network.csv', sep=',')
