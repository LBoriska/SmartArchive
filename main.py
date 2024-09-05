import urllib.request
import urllib.error
import urllib.parse
import os
import css_js

# Funktion to request URL from User:


def get_user_input_url():
    return input("Input your URL: ")

# Funktion to request a path and name of the file for html-codes:


def get_user_input_file():
    path = input("Enter the path to save the file (fE C:/Users/tn/OneDrive/Desktop): ")
    filename = input("Enter the file name: ")
    return path, filename


# This function get_html_code(this_url) takes URL as argument and
# returns html. If error occurs while requesting the page, the function
# will print an error message and return None. The class urllib.error.URLError
# in urllib.error indicates various errors, fE:
# "Name or service not known" - the specified host was not found
# "Connection refused" - the connection to the server was rejected
# "timed out" - the server did not respond within the set timeout  and others


def get_html_code(this_url):
    try:
        # Open the URL and read its contents
        with urllib.request.urlopen(this_url) as response:
            this_html_code = response.read().decode('utf-8')
            return this_html_code
    except urllib.error.URLError as e:
        print("Error fetching the page: ", e.reason)
        return None
    except ConnectionResetError as e:
        print(f"Connection was reset by the remote host while fetching {this_url}: {e}")
        return None


# ----------------------------------------------------------------------------

# The function create_file_if_not_exists  checks the existence of a file at the given path and name.
# If the file already exists, the user is prompted to enter a different file name until a unique
# file name is found.
# Once a unique file name is found, the function creates the file and returns the full path to
# the created file.
# If the file was created successfully, a message is displayed with the path to the created file,
# otherwise an error message is displayed.

def create_file_if_not_exists(path, filename):
    full_path = os.path.join(path, filename)  # Forming the full path to the file

    # Checking the existence of the file
    if os.path.exists(full_path):  # Checking if the file exists at the specified path
        while True:  # Run a loop until a unique file name is found
            new_filename = input(f"File with this name already exists. Enter a different file name: ")
            new_full_path = os.path.join(path, new_filename)  # Form the full path to the file with a new name

            # Checking the existence of the file with a new name
            if not os.path.exists(new_full_path):  # If the file with the new name does not exist
                full_path = new_full_path  # use a new full path
                filename = new_filename
                break
            else:
              print()

    try:
        # Create a file
        with open(full_path, 'w', encoding='utf-8') as f:  # Open the file for writing
            print(f"File {filename} was successfully created at {path}")   # Print a message
            # about the successful creation of the file
            return full_path  # Return the full path to the created file
    except Exception as e:
        print("Error creating file:", e)   # Print an error message
        return None  # Return None to handle the error further

# ----------------------------------------------------

# The function save_html_codes(urls, this_full_path) takes a list of urls, file path,
# reads the html codes of each web page sequentially and saves all the html codes in
# one html document.


def save_html_codes(urls, this_full_path):
    try:
        # Open file to save HTML-codes
        with open(this_full_path, 'w', encoding='utf-8') as f:
            # Write the start of the HTML file
            f.write("<html>\n<body>\n")
            # Get and write HTML for every site
            for url in urls:
                this_html_code = get_html_code(url)
                if this_html_code:
                    f.write(f"<!-- HTML-code for: {url} -->\n")
                    f.write(this_html_code + "\n\n")
            # End of the HTML file
            f.write("</body>\n</html>")

            print(f"HTML codes are saved in the file {this_full_path}")
    except Exception as e:
        print("Error saving HTML codes:", e)


# ------------------------------------------------------------------------------------
# The creating_list_urls function uses the standard Python library urllib.parse.
# The function takes HTML text as input. The function recursively finds all links
# to subpages and sub-subpages in this text with a default depth of 2, checks them for
# uniqueness and adds them to a list. The function returns a list of unique working links


def creating_list_urls(html_text, main_url, visited_urls=None, depth=0, max_depth=2):
    if visited_urls is None:
        visited_urls = set()
    # Create a list for URLs
    all_links = []

    # Check depth of recursion
    if depth >= max_depth or main_url in visited_urls:
        return all_links

    visited_urls.add(main_url)  # Mark main_url as visited

    # Parsing of HTML-code with urllib.parse
    from html.parser import HTMLParser

    class LinkParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.links = []

        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                for attr, value in attrs:
                    if attr == 'href':
                        self.links.append(value)

    # Create a parser instance and parse the HTML code
    parser = LinkParser()
    parser.feed(html_text)

    # Sort through the links, open them, find new links
    for link in parser.links:
        try:
            if urllib.parse.urlparse(link).scheme == '':
                continue  # Skip relative link

            # Get HTML code of the page from the link
            this_html_code = get_html_code(link)
            # If the HTML code is received successfully, add links to the general list
            if this_html_code:
                all_links.append(link)
                # Recursively call creating_list_urls to process internal links
                inner_links = creating_list_urls(this_html_code, link,
                                                 visited_urls, depth + 1, max_depth)
                all_links.extend(inner_links)
        except Exception as e:
            print("Error processing URL:", link, e)

    # Insert main_url at position 0
    if main_url not in all_links:
        all_links.insert(0, main_url)
    seen_links = {}
    all_links_unique = []
    for link in all_links:
        if link not in seen_links:
            all_links_unique.append(link)
            seen_links[link] = True

    return all_links_unique

# -----------------------------------


base_url = get_user_input_url()  # http://www.sozialatlas-neukoelln.de/index.php/tr/soziallaeden-allgemein/972-gfs-spendenwarenhaus-neukoelln

# http://www.projekt-cib.de/wordpress/    https://pypi.org/project/pywebcopy/

this_path = input("At first wir save only html without stiles."
                  " \nEnter the path to save the html-file and press 'ENTER': ")
# C:/Users/lborisow/tn/OneDrive/Documents/LBor/ZIB_test C:/Users/tn/OneDrive/Dokumente/ZIB_Projekt

this_filename = input("Enter the file name, for example 27.html, and press 'ENTER': ")

created_file = create_file_if_not_exists(this_path, this_filename)

html_code = get_html_code(base_url)

recursion_depth = int(input("Enter recursion depth and press 'ENTER': "))

list_of_links = creating_list_urls(html_code, base_url,  max_depth=recursion_depth)

print(list_of_links)

print("There are ", len(list_of_links), "links in our List")

save_html_codes(list_of_links, created_file)


css_js.setup_and_save_pages(list_of_links)

