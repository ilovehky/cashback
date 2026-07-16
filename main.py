from bs4 import BeautifulSoup
from datetime import datetime
from playwright.sync_api import sync_playwright

style_tag = """
    <style>
      body {
        font-family: Arial, sans-serif;
        position: relative;
        margin: 0;
        padding: 0;
        height: 100vh;
        overflow: hidden;
      }
      body::before {
        content: "";
        background-image: url('money.jpeg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        opacity: 0.5;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: -1;
      }
      h1 {
        font-size: 30px;
        font-weight: bold;
      }
      h2 {
        font-size: 20px;
        font-weight: bold;
      }
      ul {
        list-style-type: disc;
        padding-left: 20px;
      }
      .highlight {
        background-color: yellow;
      }
    </style>
"""

title_tag = """
    <h1>DuoKey's Cashback Dashboard</h1><hr>
"""
# Source page (rendered in a headless browser because NerdWallet blocks plain
# HTTP requests and loads its tables with JavaScript).
source_url = "https://www.nerdwallet.com/article/credit-cards/current-credit-card-bonus-categories"

# Current quarter label, e.g. "q3". Derived from today's date so the dashboard
# always shows the active quarter without any manual updates.
current_quarter = 'q' + str((datetime.now().month - 1) // 3 + 1)


def fetch_rendered_html(url):
    """Load the page in headless Chromium and return the fully rendered HTML."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        )
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(2500)  # let client-side tables render
        html = page.content()
        browser.close()
    return html


def extract_quarter_items(soup, card_keyword, quarter_label):
    """Return the bonus categories for the given card and quarter from the page.

    Finds the table mentioning ``card_keyword`` (e.g. "chase freedom" or
    "discover"), locates the row for ``quarter_label`` (e.g. "q3") and splits the
    category cell into individual items.
    """
    for table in soup.find_all('table'):
        table_text = table.get_text(separator=' ', strip=True).lower()
        if card_keyword not in table_text:
            continue
        for tr in table.find_all('tr'):
            cells = tr.find_all(['td', 'th'])
            if not cells:
                continue
            if quarter_label not in cells[0].get_text(separator=' ', strip=True).lower():
                continue
            category_cell = cells[1] if len(cells) >= 2 else cells[0]
            items = [li.get_text(strip=True).rstrip('.')
                     for li in category_cell.find_all('li')]
            if not items:
                raw = category_cell.get_text(separator='.', strip=True)
                items = [part.strip().rstrip('.') for part in raw.split('.') if part.strip()]
            return items
    return []


rendered_html = fetch_rendered_html(source_url)
soup = BeautifulSoup(rendered_html, 'html.parser')

discover_items = extract_quarter_items(soup, 'discover', current_quarter)
chase_items = extract_quarter_items(soup, 'chase freedom', current_quarter)

if not discover_items:
    raise RuntimeError("Could not extract Discover bonus categories from source page")
if not chase_items:
    raise RuntimeError("Could not extract Chase Freedom bonus categories from source page")

discover_info = """
    <h2>Discover ($1500/quarter)</h2>
        <ul>
            <b class=\"highlight\">Discover it ($0.01/point)</b>
"""
for item in discover_items:
    discover_info += "<li><b>5 Pts</b> on " + item + "</li>"
discover_info += "</ul><hr>"

freedom_flex_info = """
    <h2>Chase Freedom Flex ($1500/quarter)</h2>
        <ul>
            <b class=\"highlight\">Chase Freedom Flex ($0.01/point)</b>
"""
for item in chase_items:
    freedom_flex_info += "<li><b>5 Pts</b> on " + item + "</li>"
freedom_flex_info += "<li><b>5 Pts</b> on Travel</li><li><b>3 Pts</b> on Dining and Delivery</li></ul><hr>"

# Create additional cashback information
apple_info = """
<h2>Apple (Unlimited)</h2>
<ul>
    <b class="highlight">Apple Card (0.01/point)</b>
    <li><b>3 Pts</b> on Apple, Nike, Uber, Panera, ExxonMobil, Walgreens, Uber Eats, Booking.com, T-Mobile</li>
    <li><b>2 Pts</b> on Apple Pay</li>
</ul>
<hr>
"""
us_bank_info = """
<h2>US Bank ($2000/quarter)</h2>
<ul>
    <b class="highlight">US Bank Cash+ (0.01/point)</b>
    <li><b>5 Pts</b> on Fast Food / Utilities / Internet / Department Stores / Cell Phone / Electronic Stores / Movie Theaters / Ground Transportation</li>
    <li><b>2 Pts</b> on Grocery / Restaurant / Gas</li>
    <br>
    <b class="highlight">US Bank Altitude Connect ($0.008/point)</b>
    <li><b>5 Pts</b> on Travel </li>
    <li><b>4 Pts</b> on Gas ($1000/quarter)</li>
    <li><b>2 Pts</b> on Grocery / Restaurant / Streaming</li>
</ul>
<hr>
"""
boa_info = """
<h2>Bank of America ($833/month)</h2>
<ul>
    <b class="highlight">BOA Customized Cash ($0.01/point)</b>:
    <li><b>3 Pts</b> on Restaurant / Gas / Online / Travel / Drug Stores / Home Improvement</li>
    <li><b>2 Pts</b> on Grocery and Wholesale Clubs</li>
</ul>
<hr>
"""
citi_info = """
<h2>Citi Bank ($500/month)</h2>
<ul>
    <b class="highlight">Citi Custom Cash ($0.01/point)</b>
    <li><b>5 Pts</b> on Restaurant / Grocery / Gas / Travel / Transit / Streaming / Drugstores / Home Improvement / Fitness Clubs / Live Entertainment</li>
</ul>
<hr>
"""
paypal_info = """
<h2>Paypal ($1000/month)</h2>
<ul>
    <b class="highlight">Paypal Debit ($0.01/point)</b>
    <li><b>5 Pts</b> on Restaurant / Grocery / Gas / Clothing / Health & Beauty</li>
</ul>
<hr>
"""
wells_fargo_info = """
<h2>Wells Fargo (Unlimited)</h2>
<ul>
    <b class="highlight">One Key ($0.01/point)</b>
    <li><b>3 Pts</b> on Expedia / Hotels.com / Vrbo</li>
    <li><b>3 Pts</b> on Restaurant / Grocery / Gas / Food Delivery</li>
    <br>
    <b class="highlight">Wells Fargo Active Cash ($0.01/point)</b>
    <li><b>2 Pts</b> on Everything</li>
</ul>
<hr>
"""
sapphire_preferred_info = """
<h2>Chase Sapphire Preferred (Unlimited)</h2>
<ul>
    <b class="highlight">Chase Sapphire Preferred ($0.01/point)</b>
    <li><b>5 Pts</b> on Chase Travel</li>
    <li><b>3 Pts</b> on Restaurant / Food Delivery / Streaming</li>
    <li><b>2 Pts</b> on Other Travel</li>
    <li><b>1 Pts</b> on Everything Else</li>
    <li><b>Notes:</b> Annual Fee $95 / Hotel credit $50</li>
</ul>
<hr>
"""
# Combine the result into HTML output
result_html = f"""
<html>
    <body>
        {style_tag}
        {title_tag}
        {discover_info}
        {freedom_flex_info}
        {sapphire_preferred_info}
        {paypal_info}
        {citi_info}
        {us_bank_info}
        {boa_info}
        {apple_info}
        {wells_fargo_info}
    </body>
</html>
"""

# Output the final result
with open("index.html", "w") as index_file:
    print(result_html, file=index_file)
