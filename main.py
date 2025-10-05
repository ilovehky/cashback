import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
# Fetch the webpage content
discover_url = "https://www.nerdwallet.com/article/credit-cards/current-credit-card-bonus-categories?msockid=31cc168329216769183b0310280466f6"
chase_url = "https://www.nerdwallet.com/article/credit-cards/current-credit-card-bonus-categories?msockid=31cc168329216769183b0310280466f6"

# Request the pages
discover_response = requests.get(discover_url)
chase_response = requests.get(chase_url)

# Parse the HTML content
discover_soup = BeautifulSoup(discover_response.text, 'html.parser')
chase_soup = BeautifulSoup(chase_response.text, 'html.parser')

# --- New: find a table in discover_response that contains the text "Chase Freedom" ---
chase_table = None
for table in discover_soup.find_all('table'):
    try:
        text = table.get_text(separator=' ', strip=True).lower()
    except Exception:
        # skip any table that can't be converted to text
        continue
    if 'chase freedom' in text:
        chase_table = table
        break

if chase_table is not None:
    # --- Parse chase_table for the current quarter (Q1/Q2/Q3/Q4) and extract items ---
    month = datetime.now().month
    if month in (1, 2, 3):
        quarter_label = 'q1'
    elif month in (4, 5, 6):
        quarter_label = 'q2'
    elif month in (7, 8, 9):
        quarter_label = 'q3'
    else:
        quarter_label = 'q4'

    quarter_row = None
    for tr in chase_table.find_all('tr'):
        first_cell = tr.find(['th', 'td'])
        if not first_cell:
            continue
        first_text = first_cell.get_text(separator=' ', strip=True).lower()
        # look for the quarter label or month hints in the first cell
        if quarter_label in first_text:
            quarter_row = tr
            break
    chase_items = []
    if quarter_row is not None:
        cells = quarter_row.find_all(['td', 'th'])
        target_cell = cells[1] if len(cells) >= 2 else quarter_row
        for li in target_cell.find_all('li'):
            chase_items.append(li.get_text(strip=True).rstrip('.'))
        if not chase_items:
            raw = target_cell.get_text(separator='|', strip=True)
            parts = [p.strip() for p in raw.split('|') if p.strip()]
            chase_items = parts
    else:
        print(f"No {quarter_label.upper()} row found in chase_table; will fall back to CSS selector if available")
else:
    print("No table containing 'Chase Freedom' found in discover_response")

# --- New: find a table in discover_response that contains the text "Discover" or "Discover it" ---
discover_table = None
for table in discover_soup.find_all('table'):
    try:
        text = table.get_text(separator=' ', strip=True).lower()
    except Exception:
        continue
    if 'discover it' in text or 'discover (' in text or ("discover" in text and "it" in text):
        discover_table = table
        break

if discover_table is not None:
    # parse the current quarter from the discover_table
    month = datetime.now().month
    if month in (1, 2, 3):
        qlabel = 'q1'
    elif month in (4, 5, 6):
        qlabel = 'q2'
    elif month in (7, 8, 9):
        qlabel = 'q3'
    else:
        qlabel = 'q4'

    dquarter_row = None
    for tr in discover_table.find_all('tr'):
        first_cell = tr.find(['th', 'td'])
        if not first_cell:
            continue
        first_text = first_cell.get_text(separator=' ', strip=True).lower()
        if qlabel in first_text:
            dquarter_row = tr
            break

    discover_items = []
    if dquarter_row is not None:
        cells = dquarter_row.find_all(['td', 'th'])
        target_cell = cells[1] if len(cells) >= 2 else dquarter_row
        for li in target_cell.find_all('li'):
            discover_items.append(li.get_text(strip=True).rstrip('.'))
        if not discover_items:
            raw = target_cell.get_text(separator='|', strip=True)
            discover_items = [p.strip() for p in raw.split('|') if p.strip()]
    else:
        print(f"No {qlabel.upper()} row found in discover_table; will fall back to CSS selector if available")
else:
    print("No table containing 'Discover' found in discover_response")


discover_list = []
discover_info = """
    <h2>Discover ($1500/quarter)</h2>
        <ul>
            <b class=\"highlight\">Discover it ($0.01/point)</b>
"""
discover_list = []
# prefer table-parsed discover_items when available
if discover_items:
    for item in discover_items:
        discover_info += "<li><b>5 Pts</b> on " + item + "</li>"
discover_info += "</ul><hr>"

freedom_flex_info = """
    <h2>Chase Freedom Flex ($1500/quarter)</h2>
        <ul>
            <b class=\"highlight\">Chase Freedom Flex ($0.01/point)</b>
"""
chase_list = []
if chase_items:
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
