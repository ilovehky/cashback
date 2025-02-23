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

# Get the current month
current_month = datetime.now().strftime('%B')

# Check if web elements are found
try:
    if current_month in ["January", "February", "March"]:
        discover_element = discover_soup.select_one(
            '#react-root > div > div > div > div > div.BgIPML > div._3Oxhw4._1p_Xo-._1voSX6._3VAeaP.oE4ByK._2nwJWz._3WHk4h > div > div._2-kWs- > div > div._2Ru-tk._11Xx7n > div > div:nth-child(4) > div > main > div._2_Pyfm._1gun6R > div > div:nth-child(7) > div > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > div > ul')
        chase_element = chase_soup.select_one(
            '#react-root > div > div > div > div > div.BgIPML > div._3Oxhw4._1p_Xo-._1voSX6._3VAeaP.oE4ByK._2nwJWz._3WHk4h > div > div._2-kWs- > div > div._2Ru-tk._11Xx7n > div > div:nth-child(4) > div > main > div._2_Pyfm._1gun6R > div > div:nth-child(12) > div > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > div > ul')
    elif current_month in ["April", "May", "June"]:
        discover_element = discover_soup.select_one(
            '#react-root > div > div > div > div > div.BgIPML > div._3Oxhw4._1p_Xo-._1voSX6._3VAeaP.oE4ByK._2nwJWz._3WHk4h > div > div._2-kWs- > div > div._2Ru-tk._11Xx7n > div > div:nth-child(4) > div > main > div._2_Pyfm._1gun6R > div > div:nth-child(7) > div > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div > ul')
        chase_element = chase_soup.select_one(
            '#react-root > div > div > div > div > div.BgIPML > div._3Oxhw4._1p_Xo-._1voSX6._3VAeaP.oE4ByK._2nwJWz._3WHk4h > div > div._2-kWs- > div > div._2Ru-tk._11Xx7n > div > div:nth-child(4) > div > main > div._2_Pyfm._1gun6R > div > div:nth-child(12) > div > div > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div > ul')
    elif current_month in ["July", "August", "September"]:
        discover_element = discover_soup.select_one(
            '#react-root > div > div > div > div > div.BgIPML > div._3Oxhw4._1p_Xo-._1voSX6._3VAeaP.oE4ByK._2nwJWz._3WHk4h > div > div._2-kWs- > div > div._2Ru-tk._11Xx7n > div > div:nth-child(4) > div > main > div._2_Pyfm._1gun6R > div > div:nth-child(7) > div > div > div > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > div > div > ul')
        chase_element = chase_soup.select_one(
            '#react-root > div > div > div > div > div.BgIPML > div._3Oxhw4._1p_Xo-._1voSX6._3VAeaP.oE4ByK._2nwJWz._3WHk4h > div > div._2-kWs- > div > div._2Ru-tk._11Xx7n > div > div:nth-child(4) > div > main > div._2_Pyfm._1gun6R > div > div:nth-child(12) > div > div > div > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > div > div > ul')
    elif current_month in ["October", "November", "December"]:
        discover_element = discover_soup.select_one(
            '#react-root > div > div > div > div > div.BgIPML > div._3Oxhw4._1p_Xo-._1voSX6._3VAeaP.oE4ByK._2nwJWz._3WHk4h > div > div._2-kWs- > div > div._2Ru-tk._11Xx7n > div > div:nth-child(4) > div > main > div._2_Pyfm._1gun6R > div > div:nth-child(7) > div > div > div > div > table > tbody > tr:nth-child(4) > td:nth-child(2) > div > div > ul')
        chase_element = chase_soup.select_one(
            '#react-root > div > div > div > div > div.BgIPML > div._3Oxhw4._1p_Xo-._1voSX6._3VAeaP.oE4ByK._2nwJWz._3WHk4h > div > div._2-kWs- > div > div._2Ru-tk._11Xx7n > div > div:nth-child(4) > div > main > div._2_Pyfm._1gun6R > div > div:nth-child(12) > div > div > div > div > table > tbody > tr:nth-child(4) > td:nth-child(2) > div > div > ul')
    discover_list = []
    discover_info = """
        <h2>Discover ($1500/quarter)</h2>
            <ul>
                <b class=\"highlight\">Discover it (0.01/point)</b>
    """
    for li in discover_element.find_all('li'):
        discover_list.append(li)
        discover_info += "<li><b>5 Pts</b> on " + li.get_text().strip(".") + "</li>"
    discover_info += "</ul><hr>"

    chase_info = """
        <h2>Chase ($1500/quarter)</h2>
            <ul>
                <b class=\"highlight\">Chase Freedom Flex (0.01/point)</b>
    """
    chase_list = []
    for li in chase_element.find_all('li'):
        chase_list.append(li)
        chase_info += "<li><b>5 Pts</b> on " + li.get_text().strip(".") + "</li>"
    chase_info += "<li><b>5 Pts</b> on Travel</li><li><b>3 Pts</b> on Dining and Delivery</li></ul><hr>"

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
        <li><b>2 Pts</b> on Grocery / Dining / Streaming</li>
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
        <li><b>5 Pts</b> on Restaurants / Grocery / Gas / Travel / Transit / Streaming / Drugstores / Home Improvement / Fitness Clubs / Live Entertainment</li>
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
        <li><b>3 Pts</b> on Dining / Grocery / Gas / Food Delivery</li>
        <br>
        <b class="highlight">Wells Fargo Active Cash ($0.01/point)</b>
        <li><b>2 Pts</b> on Everything</li>
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
            {chase_info}
            {citi_info}
            {paypal_info}
            {us_bank_info}
            {boa_info}
            {apple_info}
            {wells_fargo_info}
        </body>
    </html>
    """

    # Output the final result
    with open("index.html", "w") as test:
        print(result_html, file=test)
except Exception as e:
    print("Error:")
    print(e)
