import pathlib
import shutil
import glob
import os
import re
import ftfy
import pandas as pd

import bike_share.data_loader as dl
import bike_share.utils as ut
import bike_share.data_cleaning_sol as dc

def main():
    dl.download_bikeshare_data()
    data_path = ut.get_data_path()
    log = ut.get_logger()

    colname_dict = {
        "Trip Id" : "trip_id",
        "Trip  Duration" : "trip_duration_seconds",
        "Start Station Id" : "from_station_id",
        "Start Station Name" : "from_station_name",
        "End Station Id" : "to_station_id",
        "End Station Name" : "to_station_name",
        "Start Time" : "trip_start_time",
        "End Time" : "trip_stop_time",
        "Bike Id" : "bike_id",
        "User Type" : "user_type"
    }

    dfs = []
    start_year = 2019
    end_year = 2022
    for y in range(start_year, end_year + 1):
        # clean the dataframe for this year only and save it
        d = dc.get_clean_unified_df(data_path.absolute(), colname_dict, log, year=y)
        dfs.append(d)
    whole_df = pd.concat(dfs)
    whole_df.to_csv(data_path / f"consolidated_DF_{start_year}_{end_year}.csv")

if __name__ == "__main__":
    main()