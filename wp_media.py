import base64
import requests
import fnmatch
import urllib3

urllib3.disable_warnings()


# get auth from username & application password
def header(user, password):
    credentials = user + ":" + password
    token = base64.b64encode(credentials.encode())
    header_json = {
        "Authorization": "Basic " + token.decode("utf-8"),
        "accept": "application/json",
    }
    return header_json


# get the post catagories dictonary from wordpress
def get_logo(url, user, password):
    params = {"per_page": 100, "order": "asc"}
    resp = requests.get(
        url + "wp-json/wp/v2/media",
        headers=header(user, password),
        params=params,
        verify=False,
    )
    response = resp.json()
    # print(response)
    url = url.lower()
    subdomain = url.split("//")[1].split(".")[0]
    basedomain = url.split("//")[1].split(".")[1]
    url_pattern = (
        f"http*://{subdomain}.{basedomain}.jp/wp-content/uploads/*/*/*{subdomain}-*.png"
    )
    # print(url_pattern)
    logo_url = None
    for d in response:
        # print(type(response))
        # print(d)
        url = d.get("guid", {}).get("rendered", "")
        matched_url = fnmatch.fnmatch(url, url_pattern)
        if matched_url:
            logo_url = url
            break
    if logo_url:
        # print(logo_url)
        return logo_url
    else:
        print("No matching dictionary found")
        return logo_url


if __name__ == "__main__":
    wp_user = "admin"
    wp_pass = "pass"
    wp_url = "https://wpurl/"
    print(get_logo(wp_url, wp_user, wp_pass))
