import os
import pandas as pd
import bike_share.utils as ut

# prerequisites: execute $ python entry_points/load_data.py (this produces a file "consolidated_DF_2019_2022.csv")
# assuming we have already a consolidated_DF_2019_2022.csv -> read it and compute daily counts of bikes borrowed

def main():

    data_path = ut.get_data_path()
    log = ut.get_logger()

    outfile = data_path / "daily_counts_2019_2022.csv"
    if os.path.exists(outfile):
        log.info(f"Outfile '{outfile}' already exists ... skipping.")
        return

    wole_df = pd.read_csv(data_path / "consolidated_DF_2019_2022.csv", parse_dates=["trip_start_time", "trip_stop_time"])
    df_grouped = wole_df.groupby("from_station_id").resample("D", on="trip_start_time").count()

    # here, the column "year" is arbitrary ... we did use "count" so all columns have the same value
    daily_counts = df_grouped["year"].reset_index()
    daily_counts = daily_counts.rename(columns = {"year" : "count"})
    daily_counts.to_csv(outfile, index=False)

if __name__ == "__main__":
    main()