# This block complements main.py in order
# to more fully preserve the content of web pages.
# Adds support for loading CSS, JavaScript, and other r
# elated resources (such as images). The block implements:
# Parsing HTML code: Extracting all external resource links.
# Downloading resources: Downloading all related files (CSS, JS, images, etc.).
# Updating links: Modifying links in the HTML code to point to locally saved files.
# Saving all files: Organizing and saving the HTML code and all resources in the local file system.


import os
import urllib.request
import urllib.error
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser


class ResourceParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.resources = []

    def handle_starttag(self, tag, attrs):
        for attr, value in attrs:
            if tag in ['link', 'script', 'img'] and attr in ['href', 'src']:
                resource_url = urljoin(self.base_url, value)
                self.resources.append((tag, attr, resource_url))


def download_resource(url, folder):
    try:
        response = urllib.request.urlopen(url)
        content = response.read()
        parsed_url = urlparse(url)
        path = parsed_url.path.strip("/")
        local_path = os.path.join(folder, path)

        # Ensure the directory exists
        local_path_dir = os.path.dirname(local_path)
        if not os.path.exists(local_path_dir):
            os.makedirs(local_path_dir)

        with open(local_path, 'wb') as file:
            file.write(content)
        return local_path
    except urllib.error.URLError as e:
        print(f"Error downloading resource {url}: {e.reason}")
        return None
    except PermissionError as e:
        print(f"Permission denied: ")
        return None
    except Exception as e:
        print(f"Unexpected error downloading resource {url}: {e}")
        return None


def get_html_code(this_url):
    if not this_url.startswith(('http://', 'https://')):
        this_url = 'http://' + this_url
    try:
        with urllib.request.urlopen(this_url) as response:
            this_html_code = response.read().decode('utf-8')
            return this_html_code
    except urllib.error.URLError as e:
        print(f"Error fetching the page {this_url}: {e.reason}")
        return None
    except ConnectionResetError as e:
        print(f"Connection was reset by the remote host while fetching {this_url}: {e}")
        return None


def save_pages(url_list, folder, output_file):
    if not os.path.exists(folder):
        os.makedirs(folder)

    combined_html = "<html><head></head><body>\n"

    for this_url in url_list:
        print(f"Fetching URL: {this_url}")
        html_code = get_html_code(this_url)
        if html_code is None:
            print(f"Skipping URL due to fetch error: {this_url}")
            continue

        parser = ResourceParser(this_url)
        parser.feed(html_code)

        for tag, attr, resource_url in parser.resources:
            print(f"Downloading resource: {resource_url}")
            local_path = download_resource(resource_url, folder)
            if local_path:
                relative_path = os.path.relpath(local_path, folder)
                html_code = html_code.replace(resource_url, relative_path)

        combined_html += f"<h1>Content from {this_url}</h1>\n" + html_code + "<hr/>\n"

    combined_html += "</body></html>"

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(combined_html)

# a funktion for setting parameters and calling save_pages


def setup_and_save_pages(url_list):
   save_folder = input("Now we save the html file, which will be called “combined.html”, and the styles in one folder."
                    " \nInput the path of folder for saving stiles and press 'ENTER': ")
   output_file = os.path.join(save_folder, 'combined.html')
   save_pages(url_list, save_folder, output_file)

    # block that is executed only from css_js.py


if __name__ == "__main__":
    url_list = ['https://pypi.org/project/pywebcopy/', 'https://github.com/rajatomar788/pywebcopy/']
    setup_and_save_pages(url_list)





