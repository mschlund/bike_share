import glob
import ftfy
import os
import pandas as pd

#helper-functions for exploratory data analysis
def get_cut_data_minMax(data, col, min=60, max=10000):
    return data[(data[col] <= max) & (data[col] >= min)]

def get_cut_data(data, col, to_keep=0.99):
    """Get the part of the input (series) that covers a high (default: 0.99) share of the data supplied.
    The min/max thresholds are also returned and symmetric in the sense that we cut away the same amount
    of "too large" values as we throw away "too small" values.
    """
    values_sorted = data[col].sort_values().reset_index(drop=True)
    assert(len(values_sorted) != 0)
    thresh_lower = (1-to_keep)/2
    thresh_upper = to_keep - thresh_lower
    min_val = values_sorted[int(len(values_sorted)*thresh_lower)]
    max_val = values_sorted[int(len(values_sorted)*thresh_upper)]
    return get_cut_data_minMax(data, col, min=min_val, max=max_val), min_val, max_val


def get_name2id(data):
    """Uses the supplied 'data' to compute a 2-column-dataframe with
      'Name' and 'ID' that can be used to reconstruct the ID from names via a join."""
    return data[["from_station_name", "from_station_id"]].drop_duplicates(). \
                rename(columns={"from_station_name": "Name", "from_station_id": "ID"}).reset_index(drop=True)

# < 30s does not make sense...
# bike-sharing is 4$ for every 30 mins over the 30/45-minute-plan ... so 2.5h=9000s should be a safe limit to cut

def _get_clean_unified_df(data_path, colname_dict, logger, year=2019, min_trip_time=30, max_trip_time=9000):
    assert(year >= 2017 and year <= 2022)
    year = int(year)
    dfs = get_dfs_for_year(data_path, logger, year)

    renamed_dfs = [d.rename(columns = {x : ftfy.fix_text(x) for x in d.columns}) for d in dfs]
    # 1) concatenate the dataframes
    logger.info("Concat dfs ...")
    whole_year_df = pd.concat(renamed_dfs)
    logger.info("Renaming dataframe, dropping NAs and converting types ...")
    # rename and drop uninteresting columns
    rename_dict = {c : colname_dict[c] for c in whole_year_df.columns if c in colname_dict}
    whole_year_df_renamed = whole_year_df.rename(columns=rename_dict)
    whole_year_df_dropped = whole_year_df_renamed.drop(columns=["from_station_name", "to_station_name"])
    whole_year_df_converted = whole_year_df_dropped.dropna().astype(
        {
            "trip_id" : int,
            "to_station_id" : int,
            "from_station_id" : int,
            "trip_duration_seconds" : int,
            "bike_id" : int,
        })
    whole_year_df_converted["is_casual"] = whole_year_df_converted["user_type"].apply(lambda x: "casual" in x.lower())
    whole_year_df_converted = whole_year_df_converted.drop(columns=["user_type"])
    logger.info("Parsing dates...")
    whole_year_df_converted["trip_start_time"] = pd.to_datetime(whole_year_df_converted["trip_start_time"])
    whole_year_df_converted["trip_stop_time"] = pd.to_datetime(whole_year_df_converted["trip_stop_time"])
    logger.info("Resticting data to min/max and setting year...")
    # 3) restrict the data to those with reasonable durations
    whole_year_df_cut = get_cut_data_minMax(whole_year_df_converted, "trip_duration_seconds", min=min_trip_time, max=max_trip_time) 
    
    # 4) insert a column "year" with the current value
    whole_year_df_cut.insert(0, "year", year)
    logger.info("done.")
    # finally concat all yearly-dataframes
    return whole_year_df_cut

def get_dfs_for_year(data_path, logger, year):
    year_str = str(year)
    logger.info(f"Processing year: {year}")
    csvs = glob.glob( str(data_path.joinpath(year_str)) + "/*.csv" )
    # 0) read in csvs
    #    and fix column-names (use the 2017-style names)
    logger.info("Reading csv ...")
    dfs = [pd.read_csv(f, sep=",", encoding= 'unicode_escape') for f in csvs]
    return dfs

def get_clean_unified_df(data_path, colname_dict, logger, year=2019):
    min_trip_time = 30
    max_trip_time = 9000
    df_filename = f"consolidated_DF_{year}.csv"
    out_df_path = data_path / df_filename
    if os.path.exists(out_df_path):
        logger.info(f"{out_df_path} has already been computed -- reusing it.")
        df = pd.read_csv(out_df_path)
    else:
        logger.info(f"Computing consolidated DF anew and saving it to '{df_filename}' afterwards.")
        # note: this takes ~7-8min to run!
        df = _get_clean_unified_df(data_path, colname_dict, logger=logger, year=year, min_trip_time=min_trip_time, max_trip_time=max_trip_time)
        logger.info("Saving data to csv...")
        df.to_csv(str(data_path) + "/" + df_filename, index=False)
        logger.info("done saving.")
    return df


"""
        # TODO:
        # reconstruct the from/to_station_id from the name
        if any(D_renamed["from_station_id"].isna()):
            D_renamed["from_station_id"] = D_renamed. \
                                            join(name2id.set_index("Name"), how="left", on="from_station_name")["ID"]
        elif any(D_renamed["to_station_id"].isna()):
            D_renamed["to_station_id"] = D_renamed. \
                                            join(name2id.set_index("Name"), how="left", on="to_station_name")["ID"]
"""