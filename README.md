Millib - Phase One
======
A simplistic Bitcoin pricer checker website in mBTC.

## Quick Info
* Price API: https://api.bitcoinaverage.com/ticker/USD
* Template Used: https://wrapbootstrap.com/theme/light-blue-responsive-admin-template-WB0T41TX4
* Run By: Python + Flask
* Database: SQLite
* OS: Debian 7 

## Phase One Process
1. Download the [Light Blue Responsive Template](https://wrapbootstrap.com/theme/light-blue-responsive-admin-template-WB0T41TX4)
2. Install Python + Flask + SQLite to your environment. Must run on Debian 7.
3. Using a CronJob + Python Script grab price data from the [Bitcoin Average API](https://api.bitcoinaverage.com/ticker/USD) and store it in a table in SQLite
4. We can store the full json dump 24h_avg, ask, bid, last, timestamp, and total_vol. Add an id as the table key for good measure.
5. Parse the table data to create a chart using the template (use the "visits" box in the template)
6. Parse the table data to show the price on the right box. Average should be big, and include the bid and ask under  it(use the "feed" box in the template)
7. Use the magic of Ajax and/or Javascript to update the chart + price box from the database. Don't refresh!
8. ???
9. Profit
