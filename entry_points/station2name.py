# parses the trip-data and builds a mapping id -> name as a dataframe (and finally saves it)

import os
import pandas as pd
import bike_share.utils as ut
import bike_share.data_cleaning as dc


def main():
    id2name = "id2name.csv"
    log = ut.get_logger
    if os.path.exists(id2name):
        log.info(f"File {id2name} already exists -- doing nothing.")
        return

    for y in range(2019, 2022 + 1):
        df = pd.concat(dc.get_dfs_for_year())
        
    # TODO: continue?

if __name__ == "__main__":
    main()