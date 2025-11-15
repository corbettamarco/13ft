import flask
import requests
import cloudscraper
from flask import request
from flask_cors import CORS
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

app = flask.Flask(__name__)
CORS(app)

# Create a cloudscraper session that mimics a modern Chrome client
scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
        "desktop": True,
    }
)

googlebot_headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.119 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
scraper.headers.update(googlebot_headers)
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet" async>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow: hidden;
            transition: background 0.3s ease;
        }

        /* Animated background elements */
        .bg-animation {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: 0;
            overflow: hidden;
        }

        .floating-circle {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            animation: float 20s infinite ease-in-out;
        }

        .circle1 {
            width: 300px;
            height: 300px;
            top: -150px;
            left: -150px;
            animation-delay: 0s;
        }

        .circle2 {
            width: 200px;
            height: 200px;
            bottom: -100px;
            right: -100px;
            animation-delay: 5s;
        }

        .circle3 {
            width: 150px;
            height: 150px;
            top: 50%;
            right: 10%;
            animation-delay: 10s;
        }

        @keyframes float {
            0%, 100% {
                transform: translate(0, 0) scale(1);
            }
            33% {
                transform: translate(30px, -50px) scale(1.1);
            }
            66% {
                transform: translate(-20px, 20px) scale(0.9);
            }
        }

        /* Main container */
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 48px;
            max-width: 520px;
            width: 100%;
            position: relative;
            z-index: 1;
            animation: slideUp 0.6s ease-out;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .logo {
            text-align: center;
            margin-bottom: 32px;
        }

        .logo-icon {
            font-size: 48px;
            margin-bottom: 8px;
            display: inline-block;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-10px);
            }
        }

        h1 {
            font-size: 2rem;
            font-weight: 700;
            color: #1a202c;
            text-align: center;
            margin-bottom: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .subtitle {
            text-align: center;
            color: #718096;
            font-size: 0.95rem;
            margin-bottom: 32px;
        }

        label {
            display: block;
            margin-bottom: 12px;
            font-weight: 600;
            color: #2d3748;
            font-size: 0.95rem;
        }

        input[type=text] {
            padding: 16px 20px;
            margin-bottom: 20px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            width: 100%;
            font-size: 1rem;
            font-family: inherit;
            transition: all 0.3s ease;
            background: #f7fafc;
        }

        input[type=text]:focus {
            outline: none;
            border-color: #667eea;
            background: #fff;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        input[type="submit"] {
            padding: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            border: none;
            border-radius: 12px;
            width: 100%;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        input[type="submit"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(102, 126, 234, 0.4);
        }

        input[type="submit"]:active {
            transform: translateY(0);
        }

        /* Dark mode toggle */
        .dark-mode-toggle {
            position: absolute;
            top: 24px;
            right: 24px;
            z-index: 10;
        }

        .dark-mode-toggle input {
            display: none;
        }

        .dark-mode-toggle label {
            cursor: pointer;
            width: 60px;
            height: 32px;
            background: rgba(255, 255, 255, 0.3);
            display: block;
            border-radius: 100px;
            position: relative;
            transition: background 0.3s;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .dark-mode-toggle label:after {
            content: '';
            position: absolute;
            top: 4px;
            left: 4px;
            width: 24px;
            height: 24px;
            background: #fff;
            border-radius: 90px;
            transition: 0.3s;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }

        .dark-mode-toggle input:checked+label {
            background: rgba(102, 126, 234, 0.6);
        }

        .dark-mode-toggle input:checked+label:after {
            left: calc(100% - 28px);
        }

        /* Dark mode styles */
        body.dark-mode {
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        }

        body.dark-mode .container {
            background: rgba(45, 55, 72, 0.95);
        }

        body.dark-mode h1 {
            color: #fff;
            -webkit-text-fill-color: #fff;
        }

        body.dark-mode .subtitle {
            color: #cbd5e0;
        }

        body.dark-mode label {
            color: #e2e8f0;
        }

        body.dark-mode input[type=text] {
            background: #2d3748;
            border-color: #4a5568;
            color: #fff;
        }

        body.dark-mode input[type=text]:focus {
            border-color: #667eea;
            background: #374151;
        }

        body.dark-mode .floating-circle {
            background: rgba(102, 126, 234, 0.1);
        }

        /* Responsive */
        @media only screen and (max-width: 600px) {
            .container {
                padding: 32px 24px;
            }

            h1 {
                font-size: 1.75rem;
            }

            .dark-mode-toggle {
                top: 16px;
                right: 16px;
            }
        }
    </style>
</head>

<body>
    <div class="bg-animation">
        <div class="floating-circle circle1"></div>
        <div class="floating-circle circle2"></div>
        <div class="floating-circle circle3"></div>
    </div>
    
    <div class="dark-mode-toggle">
        <input type="checkbox" id="dark-mode-toggle">
        <label for="dark-mode-toggle" title="Toggle Dark Mode"></label>
    </div>
    
    <div class="container">
        <div class="logo">
            <div class="logo-icon">🪜</div>
        </div>
        <h1>13ft Ladder</h1>
        <p class="subtitle">Break through paywalls and access articles freely</p>
        
        <form action="/article" method="post">
            <label for="link">Enter Article URL</label>
            <input type="text" id="link" name="link" placeholder="https://example.com/article" required autofocus>
            <input type="submit" value="Remove Paywall">
        </form>
    </div>

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

def expand_shortened_url(url):
    """
    Expand shortened URLs (Google share links, bit.ly, etc.) to get the actual URL
    """
    shortened_domains = ['share.google', 'goo.gl', 'bit.ly', 't.co', 'tinyurl.com', 'ow.ly']
    
    try:
        # Check if it's a shortened URL
        if any(domain in url for domain in shortened_domains):
            # Follow redirects to get final URL
            response = requests.head(url, allow_redirects=True, timeout=10)
            return response.url
    except Exception as e:
        print(f"Failed to expand URL: {e}")
    
    return url

def bypass_paywall(url):
    """
    Bypass paywall for a given url
    """
    if url.startswith("http"):
        # Expand shortened URLs first
        url = expand_shortened_url(url)
        
        # Try with Googlebot headers first
        try:
            response = requests.get(url, headers=googlebot_headers, timeout=10)
            response.encoding = response.apparent_encoding
            
            # Check if we got a Cloudflare challenge page
            if 'cdn-cgi/challenge-platform' in response.text or response.status_code == 403 or 'Invalid domain' in response.text:
                # Fallback to cloudscraper for Cloudflare-protected sites
                response = scraper.get(url, timeout=10, headers=googlebot_headers)
                response.encoding = response.apparent_encoding
            
            return add_base_tag(response.text, response.url)
        except Exception as e:
            # If requests fails, try cloudscraper
            try:
                response = scraper.get(url, timeout=10, headers=googlebot_headers)
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
    # Generate a realistic 3D ladder icon with perspective
    from PIL import Image, ImageDraw
    import io
    import math
    
    size = 512 if "512" in request.path else 192
    
    # Create image with gradient background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw circular gradient background
    for y in range(size):
        for x in range(size):
            # Distance from center
            dx = x - size / 2
            dy = y - size / 2
            distance = math.sqrt(dx * dx + dy * dy)
            max_distance = size / 2
            
            if distance <= max_distance:
                # Radial gradient from center
                factor = distance / max_distance
                r = int(102 + (118 - 102) * factor)
                g = int(126 + (75 - 126) * factor)
                b = int(234 + (162 - 234) * factor)
                draw.point((x, y), fill=(r, g, b, 255))
    
    # Create ladder with perspective (slightly wider at bottom)
    padding_top = size // 4
    padding_bottom = size // 6
    padding_side = size // 4.5
    
    rail_width = max(size // 28, 4)
    
    # Left rail (tapered perspective)
    left_top = padding_side
    left_bottom = padding_side - size // 15
    
    # Right rail (tapered perspective)
    right_top = size - padding_side
    right_bottom = size - padding_side + size // 15
    
    # Draw rails with gradient for 3D effect
    def draw_rail_with_gradient(x_top, x_bottom, is_left=True):
        steps = size - padding_top - padding_bottom
        for i in range(steps):
            y = padding_top + i
            progress = i / steps
            x = x_top + (x_bottom - x_top) * progress
            
            # Darker on sides, lighter in middle for cylindrical effect
            for offset in range(-rail_width // 2, rail_width // 2 + 1):
                brightness = 1.0 - abs(offset) / (rail_width / 2) * 0.4
                color_val = int(255 * brightness)
                draw.point((int(x + offset), int(y)), fill=(color_val, color_val, color_val, 255))
    
    draw_rail_with_gradient(left_top, left_bottom, True)
    draw_rail_with_gradient(right_top, right_bottom, False)
    
    # Draw rungs with 3D effect
    num_rungs = 8
    for i in range(num_rungs):
        progress = (i + 1) / (num_rungs + 1)
        y = padding_top + progress * (size - padding_top - padding_bottom)
        
        # Calculate X positions based on perspective
        x_left = left_top + (left_bottom - left_top) * progress
        x_right = right_top + (right_bottom - right_top) * progress
        
        rung_height = max(size // 50, 3)
        
        # Shadow
        shadow_offset = max(size // 120, 2)
        draw.ellipse([
            x_left - rail_width // 2 + shadow_offset,
            y - rung_height // 2 + shadow_offset,
            x_right + rail_width // 2 + shadow_offset,
            y + rung_height // 2 + shadow_offset
        ], fill=(0, 0, 0, 40))
        
        # Draw rung with gradient for cylindrical look
        for dy in range(-rung_height // 2, rung_height // 2 + 1):
            brightness = 1.0 - abs(dy) / (rung_height / 2) * 0.3
            color_val = int(220 * brightness)
            draw.line([
                (int(x_left - rail_width // 2), int(y + dy)),
                (int(x_right + rail_width // 2), int(y + dy))
            ], fill=(color_val, color_val, color_val, 255), width=1)
        
        # Highlight on top edge
        draw.line([
            (int(x_left - rail_width // 2), int(y - rung_height // 2)),
            (int(x_right + rail_width // 2), int(y - rung_height // 2))
        ], fill=(255, 255, 255, 180), width=1)
    
    # Add highlights to rails for shiny effect
    for i in range(0, size - padding_top - padding_bottom, 3):
        progress = i / (size - padding_top - padding_bottom)
        y = padding_top + i
        
        x_left = left_top + (left_bottom - left_top) * progress
        x_right = right_top + (right_bottom - right_top) * progress
        
        # Left rail highlight
        draw.point((int(x_left - rail_width // 4), int(y)), fill=(255, 255, 255, 160))
        # Right rail highlight
        draw.point((int(x_right + rail_width // 4), int(y)), fill=(255, 255, 255, 160))
    
    # Serve as PNG
    img_io = io.BytesIO()
    img.save(img_io, 'PNG', quality=95)
    img_io.seek(0)
    return flask.send_file(img_io, mimetype='image/png')
    
    # Serve as PNG
    img_io = io.BytesIO()
    img.save(img_io, 'PNG', quality=95)
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
        except Exception as e:
            raise e
    else:
        return "Invalid URL", 400


app.run(host="0.0.0.0", port=5000, debug=False)
