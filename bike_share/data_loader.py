import os
import pathlib
import requests
import shutil
import glob

# Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:
# https://docs.ckan.org/en/latest/api/


def download_bikeshare_data():
    """Download the 'Toronto bikeshare' dataset from the city's open-data-server.
    Unzip the downloaded zip-files, generate directories "2017", ...,"2022"
    in the "data" dir and move the unzipped data there.
    """
    data_path = (pathlib.Path.cwd() / ".." / "data").resolve()
    # Toronto Open Data is stored in a CKAN instance. It"s APIs are documented here:
    # https://docs.ckan.org/en/latest/api/
    # To hit our API, you"ll be making requests to:
    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    # Datasets are called "packages". Each package can contain many "resources"
    # To retrieve the metadata for this package and its resources, use the package name in this page"s URL:
    url = base_url + "/api/3/action/package_show"
    params = {"id": "bike-share-toronto-ridership-data"}
    package = requests.get(url, params=params).json()
    # To get resource data:
    for idx, resource in enumerate(package["result"]["resources"]):
        # To get metadata for non datastore_active resources:
        if not resource["datastore_active"]:
            url = base_url + "/api/3/action/resource_show?id=" + resource["id"]
            resource_metadata = requests.get(url).json()
            print(resource_metadata)
            # From here, you can use the "url" attribute to download this file
            name = resource["name"]
            extension = resource["format"].lower()
            file_to_save = data_path / f"{name}.{extension}"
            if (os.path.exists(file_to_save)):
                print(
                    f"File {file_to_save} already exists -- skipping download.")
                continue
            with open(file_to_save, "wb") as data_file:
                f = requests.get(resource["url"])
                data_file.write(f.content)

    for y in range(2017, 2023):
        year_str = str(y)
        zipfile_list = glob.glob(str(data_path) + f"/*{year_str}*.zip")
        assert (len(zipfile_list) == 1)
        print(f"Found {zipfile_list}.")

        year_dir = data_path.joinpath(year_str)
        if (os.path.exists(year_dir)):
            print(f"Path {year_dir} already exists -- skipping extraction.")
        else:
            print(f"Extracting {zipfile_list}...")
            shutil.unpack_archive(zipfile_list[0], data_path)
            unzipped_year_dir = glob.glob(str(data_path) + f"/*{year_str}*/")
            if unzipped_year_dir == []:
                os.mkdir(year_dir)
                csvs = glob.glob(str(data_path) + f"/*{year_str}*.csv")
                for csv in csvs:
                    shutil.move(csv, year_dir)
            else:
                assert (len(unzipped_year_dir) == 1)
                os.rename(unzipped_year_dir[0], year_dir)
