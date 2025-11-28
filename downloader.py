import requests

def download_files(url_list):
    downloaded = {}

    for url in url_list:
        try:
            response = requests.get(url)
            response.raise_for_status()

            filename = url.split("/")[-1]
            content_type = response.headers.get("Content-Type", "text/plain")

            downloaded[filename] = (content_type, response.text)

        except Exception as e:
            print("Failed to download:", url, e)

    return downloaded
