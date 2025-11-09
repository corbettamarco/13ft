import flask
import requests
import cloudscraper
from flask import request
from flask_cors import CORS
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

app = flask.Flask(__name__)
CORS(app)

# Create a cloudscraper session for sites with Cloudflare protection
scraper = cloudscraper.create_scraper()

googlebot_headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.119 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="theme-color" content="#6a0dad">
    <title>13ft Ladder</title>
    <link rel="manifest" href="/manifest.json">
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet" async>
    <style>
        body {
            font-family: 'Open Sans', sans-serif;
            background-color: #FFF;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 90vh;
            transition: background-color 0.3s, color 0.3s;
        }

        h1 {
            font-size: 1.5rem;
            margin-bottom: 20px;
            text-align: center;
            color: #333;
        }

        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
        }

        input[type=text] {
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            width: 100%;
            font-size: 1rem;
            box-sizing: border-box;
        }

        input[type="submit"] {
            padding: 10px;
            background-color: #6a0dad;
            color: #fff;
            border: none;
            border-radius: 5px;
            width: 100%;
            text-transform: uppercase;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        input[type="submit"]:hover {
            background-color: #4e0875;
        }

        /* Toggle switch styles */
        .dark-mode-toggle {
            position: absolute;
            top: 10px;
            right: 10px;
        }

        .dark-mode-toggle input {
            display: none;
        }

        .dark-mode-toggle label {
            cursor: pointer;
            text-indent: -9999px;
            width: 52px;
            height: 27px;
            background: grey;
            display: block;
            border-radius: 100px;
            position: relative;
        }

        .dark-mode-toggle label:after {
            content: '';
            position: absolute;
            top: 2px;
            left: 2px;
            width: 23px;
            height: 23px;
            background: #fff;
            border-radius: 90px;
            transition: 0.3s;
        }

        .dark-mode-toggle input:checked+label {
            background: #6a0dad;
        }

        .dark-mode-toggle input:checked+label:after {
            left: calc(100% - 2px);
            transform: translateX(-100%);
        }

        /* Responsive adjustments */
        @media only screen and (max-width: 600px) {
            form {
                padding: 10px;
            }

            h1 {
                font-size: 1.2rem;
            }
        }

        /* Dark mode styles */
        body.dark-mode {
            background-color: #333;
            color: #FFF;
        }

        body.dark-mode h1 {
            color: #FFF;
        }

        body.dark-mode input[type=text] {
            background-color: #555;
            border: 1px solid #777;
            color: #FFF;
        }

        body.dark-mode input[type="submit"] {
            background-color: #9b30ff;
        }

        body.dark-mode input[type="submit"]:hover {
            background-color: #7a1bb5;
        }
    </style>
</head>

<body>
    <div class="dark-mode-toggle">
        <input type="checkbox" id="dark-mode-toggle">
        <label for="dark-mode-toggle" title="Toggle Dark Mode"></label>
    </div>
    <form action="/article" method="post">
        <h1>Enter Website Link</h1>
        <label for="link">Link of the website you want to remove paywall for:</label>
        <input type="text" id="link" name="link" required autofocus>
        <input type="submit" value="Submit">
    </form>

    <script>
        // Register service worker for WebAPK installation
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(reg => console.log('Service Worker registered'))
                .catch(err => console.log('Service Worker registration failed'));
        }

        const toggleSwitch = document.getElementById('dark-mode-toggle');
        const currentTheme = localStorage.getItem('theme') || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");

        if (currentTheme === "dark") {
            document.body.classList.add("dark-mode");
            toggleSwitch.checked = true;
        }

        toggleSwitch.addEventListener('change', function () {
            if (this.checked) {
                document.body.classList.add("dark-mode");
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.classList.remove("dark-mode");
                localStorage.setItem('theme', 'light');
            }
        });
    </script>
</body>

</html>
"""

def add_base_tag(html_content, original_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    parsed_url = urlparse(original_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    
    # Handle paths that are not root, e.g., "https://x.com/some/path/w.html"
    if parsed_url.path and not parsed_url.path.endswith('/'):
        base_url = urljoin(base_url, parsed_url.path.rsplit('/', 1)[0] + '/')
    base_tag = soup.find('base')
    
    print(base_url)
    if not base_tag:
        new_base_tag = soup.new_tag('base', href=base_url)
        if soup.head:
            soup.head.insert(0, new_base_tag)
        else:
            head_tag = soup.new_tag('head')
            head_tag.insert(0, new_base_tag)
            soup.insert(0, head_tag)
    
    return str(soup)

def bypass_paywall(url):
    """
    Bypass paywall for a given url
    """
    if url.startswith("http"):
        # Try with Googlebot headers first
        try:
            response = requests.get(url, headers=googlebot_headers, timeout=10)
            response.encoding = response.apparent_encoding
            
            # Check if we got a Cloudflare challenge page
            if 'cdn-cgi/challenge-platform' in response.text or response.status_code == 403:
                # Fallback to cloudscraper for Cloudflare-protected sites
                response = scraper.get(url, timeout=10)
                response.encoding = response.apparent_encoding
            
            return add_base_tag(response.text, response.url)
        except Exception as e:
            # If requests fails, try cloudscraper
            try:
                response = scraper.get(url, timeout=10)
                response.encoding = response.apparent_encoding
                return add_base_tag(response.text, response.url)
            except Exception as scraper_error:
                raise e  # Raise original error if both fail

    try:
        return bypass_paywall("https://" + url)
    except requests.exceptions.RequestException as e:
        return bypass_paywall("http://" + url)


@app.route("/")
def main_page():
    return html


@app.route("/manifest.json")
def serve_manifest():
    return flask.send_from_directory(".", "manifest.json")


@app.route("/sw.js")
def serve_sw():
    return flask.send_from_directory(".", "sw.js")


@app.route("/icon-192.png")
@app.route("/icon-512.png")
def serve_icon():
    # Generate a ladder icon
    from PIL import Image, ImageDraw
    import io
    
    size = 512 if "512" in request.path else 192
    img = Image.new('RGB', (size, size), color='#6a0dad')
    draw = ImageDraw.Draw(img)
    
    # Draw ladder
    line_width = max(size // 40, 2)
    padding = size // 6
    
    # Left rail
    left_x = padding
    draw.rectangle([left_x, padding, left_x + line_width, size - padding], fill='white')
    
    # Right rail
    right_x = size - padding - line_width
    draw.rectangle([right_x, padding, right_x + line_width, size - padding], fill='white')
    
    # Rungs (horizontal bars)
    num_rungs = 8
    rung_spacing = (size - 2 * padding) // (num_rungs + 1)
    for i in range(1, num_rungs + 1):
        y = padding + i * rung_spacing
        draw.rectangle([left_x, y, right_x + line_width, y + line_width], fill='white')
    
    # Serve as PNG
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return flask.send_file(img_io, mimetype='image/png')


@app.route("/article", methods=["POST"])
def show_article():
    # Support both 'link' (from form) and 'url' (from share target)
    link = flask.request.form.get("link") or flask.request.form.get("url") or flask.request.form.get("text")
    if not link:
        return "No URL provided", 400
    try:
        return bypass_paywall(link)
    except requests.exceptions.RequestException as e:
        return str(e), 400
    except Exception as e:
        raise e


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["GET"])
def get_article(path):
    full_url = request.url
    parts = full_url.split("/", 4)
    if len(parts) >= 5:
        actual_url = "https://" + parts[4].lstrip("/")
        try:
            return bypass_paywall(actual_url)
        except requests.exceptions.RequestException as e:
            return str(e), 400
        except e:
            raise e
    else:
        return "Invalid URL", 400


app.run(host="0.0.0.0", port=5000, debug=False)
