import requests
import re
import json
import time

def fetch_and_update_tokens():
    # Your API URL and headers
    api_url = "http://34744-remark.cloud-ott.me/server/load.php?type=itv&action=get_all_channels&JsHttpRequest=1-xml"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer D53BEE71093ABC5E41C8713C8C1C4F90",
        "Connection": "Keep-Alive",
        "Cookie": "mac=00:1A:79:75:2f:59; stb_lang=en; timezone=GMT",
        "Host": "34744-remark.cloud-ott.me",
        "Referer": "http://34744-remark.cloud-ott.me:80/c/",
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3",
        "X-User-Agent": "Model: MAG250; Link: WiFi"
    }

    # Fetch the data from the API
    response = requests.get(api_url, headers=headers)
    response_text = response.text

    # Parse the JSON response
    response_data = json.loads(response_text)

    # List of target numbers
    target_numbers = ['280766', '1104672', '1104672', '280744', '155975']  # Add your numbers here
    urls = {}

    for item in response_data['js']['data']:
        for cmd in item['cmds']:
            for target_number in target_numbers:
                if target_number in cmd['url']:
                    # Remove 'ffmpeg ' from the URL
                    cleaned_url = cmd['url'].replace('ffmpeg ', '')
                    urls[target_number] = cleaned_url

    if urls:
        print("\nNew URLs found and updated.")
    else:
        print("\nNo new URLs found.")

    return urls

def update_php_file(urls, php_file_path):
    # Create a new file and write the updated URLs
    with open(php_file_path, 'w') as file:
        for stream_id, url in urls.items():
            file.write(f'#EXTINF:-1 group-title="34744-remark.cloud-ott.me",Stream {stream_id}\n')
            file.write(f'{url}\n')
    print(f"PHP file {php_file_path} created and updated with new URLs.")

# Path to your PHP file
php_file_path = 'play.php'

# Initialize tokens.json if it doesn't exist
try:
    with open('tokens.json', 'x') as token_file:
        json.dump({}, token_file)
except FileExistsError:
    pass

# Call the function every 30 seconds to check for changes
while True:
    urls = fetch_and_update_tokens()
    if urls:
        update_php_file(urls, php_file_path)
    time.sleep(30)  # Wait for 30 seconds before checking again
