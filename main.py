import os
import csv
from dropbox import Dropbox
from dropbox.exceptions import ApiError


FOLDER = "/Games"

access_token = os.getenv("DROPBOX__ACCESS_TOKEN")
assert access_token, "Please set the environment variable DROPBOX__ACCESS_TOKEN"
client = Dropbox(access_token)


files = client.files_list_folder(FOLDER).entries

with open("urls.csv", "w") as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for file in files:
        path = file.path_lower
        share_results = client.sharing_list_shared_links(path, direct_only=True)
        if share_results.links:
            url = share_results.links[0].url
        else:
            try:
                share_link_result = client.sharing_create_shared_link_with_settings(
                    path
                )
            except ApiError:
                print(f"Failed to create share link for {path}")
            url = share_link_result.url.replace("dl=0", "dl=1")

        writer.writerow([path, url.replace("dl=0", "dl=1")])
