import glob
import ftfy
import pandas as pd
import os
import bike_share.data_cleaning_sol as dc

import logging

# https://stackoverflow.com/questions/18786912/get-output-from-the-logging-module-in-ipython-notebook

def get_logger():
    logger = logging.getLogger()
    fhandler = logging.FileHandler(filename='mylog.log', mode='a')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(logging.INFO)
    return logger


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
    m = values_sorted[int(len(values_sorted)*thresh_lower)]
    M = values_sorted[int(len(values_sorted)*thresh_upper)]
    return get_cut_data_minMax(data, col, min=m, max=M), m, M


def get_name2id(data):
    """Uses the supplied 'data' to compute a 2-column-dataframe with
      'Name' and 'ID' that can be used to reconstruct the ID from names via a join."""
    return data[["from_station_name", "from_station_id"]].drop_duplicates(). \
                rename(columns={"from_station_name": "Name", "from_station_id": "ID"}).reset_index(drop=True)

def _get_clean_unified_df(data_path, colname_dict, logger, start_year=2019, end_year=2022):
    assert(start_year >= 2017)
    end_year = 2022 if end_year > 2022 else end_year
    res = []
    for year in range(start_year, end_year+1):
        year = int(year)
        year_str = str(year)
        logger.info(f"Processing year: {year}")
        csvs = glob.glob( str(data_path.joinpath(year_str)) + "/*.csv" )
        # 0) read in csvs
        #    and fix column-names (use the 2017-style names)
        logger.info("Reading csv ...")
        dfs = [pd.read_csv(f, sep=",", encoding= 'unicode_escape') for f in csvs]
        renamed_dfs = [d.rename(columns = {x : ftfy.fix_text(x) for x in d.columns}) for d in dfs]
        # 1) concatenate the dataframes
        logger.info("Concat dfs ...")
        D = pd.concat(renamed_dfs)
        logger.info("Renaming dataframe, dropping NAs and converting types ...")
        # rename and drop uninteresting columns
        rename_dict = {c : colname_dict[c] for c in D.columns if c in colname_dict}
        D_renamed = D.rename(columns=rename_dict)
        D_dropped = D_renamed.drop(columns=["from_station_name", "to_station_name"])
        D_converted = D_dropped.dropna().astype(
            {
                "trip_id" : int,
                "to_station_id" : int,
                "from_station_id" : int,
                "trip_duration_seconds" : int,
                "bike_id" : int,
            })
        D_converted["is_casual"] = D_converted["user_type"].apply(lambda x: "casual" in x.lower())
        D_converted = D_converted.drop(columns=["user_type"])
        logger.info("Parsing dates...")
        D_converted["trip_start_time"] = pd.to_datetime(D_converted["trip_start_time"])
        D_converted["trip_stop_time"] = pd.to_datetime(D_converted["trip_stop_time"])
        logger.info("Resticting data to min/max and setting year...")
        # 3) restrict the data to those within 0.99 of the durations
        d = get_cut_data_minMax(D_converted, "trip_duration_seconds", min=30, max=10000) # < 30s does not make sense... >10k is more than ~2.5h.. should be ok to disregard
        # 4) insert a column "year" with the current value
        d.insert(0, "year", year)
        logger.info("done.")
        res.append(d.reset_index(drop=True))
    # finally concat all yearly-dataframes
    return pd.concat(res, axis=0).reset_index(drop=True)

def get_clean_unified_df(data_path, colname_dict, logger, start_year=2019, end_year=2022):
    df_filename = f"consolidated_DF_{start_year}_{end_year}.csv"
    if os.path.exists(df_filename):
        logger.info(f"{df_filename} has already been computed -- reusing it.")
        D = pd.read_csv(df_filename)
    else:
        logger.info(f"Computing consolidated DF anew and saving it to '{df_filename}' afterwards.")
        # note: this takes ~7-8min to run!
        D = _get_clean_unified_df(data_path, colname_dict, logger=logger, start_year=start_year, end_year=end_year)
        logger.info("Saving data to csv...")
        D.to_csv(df_filename, index=False)
        logger.info("done saving.")
    return D

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