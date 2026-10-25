/* Kyle White Links: broker referral map (REF). Every ticker price and the "Open an account" strip read this.
   ref: Kyle's approved referral/affiliate link. While ref is empty the tap goes to the broker's plain signup (url),
   which earns nothing, so fill ref as soon as a program approves Kyle. coins: per-coin broker override (default below). */
window.KW_REF = {
 "default": "coinbase",
 "brokers": {
  "coinbase": {"name": "Coinbase", "tag": "Crypto", "url": "https://www.coinbase.com/signup", "ref": ""},
  "kraken": {"name": "Kraken", "tag": "Crypto", "url": "https://www.kraken.com/sign-up", "ref": ""},
  "robinhood": {"name": "Robinhood", "tag": "Stocks & crypto", "url": "https://join.robinhood.com/", "ref": ""}
 },
 "strip": ["coinbase", "kraken", "robinhood"],
 "coins": {"tron": "kraken", "hyperliquid": "kraken", "binancecoin": "kraken"}
};
