/* Kyle White Links: looks data. The single source of truth for "Shop my outfits".
   LINKS: one entry per product (key -> brand, name, price USD, url, img, live).
   LOOKS: each look lists LINKS keys. A piece whose key is missing or live:false hides itself;
   a look with fewer than 2 live pieces hides itself. CI fails on any look pointing to a missing key.
   To add a look: add products to LINKS, then add a look below. Rebuild with python3 build.py. */
window.KW_LOOKS = {
 "version": 1,
 "LINKS": {
  "faloni-blazer": {
   "brand": "Luca Faloni",
   "name": "Cashmere blazer",
   "price": 1695.0,
   "url": "https://lucafaloni.com/en/us/shop/blazers-and-suits/charcoal-grey-cashmere-blazer",
   "img": "img/faloni-blazer.webp",
   "category": "Tailoring",
   "live": true
  },
  "faloni-crew": {
   "brand": "Luca Faloni",
   "name": "Silk-cashmere crew",
   "price": 425.0,
   "url": "https://lucafaloni.com/en/us/shop/navy-blue-silk-cashmere-crew-neck",
   "img": "img/faloni-crew.webp",
   "category": "Knitwear",
   "live": true
  },
  "velasca-loafer": {
   "brand": "Velasca",
   "name": "Maester penny loafer",
   "price": 500.0,
   "url": "https://www.velasca.com/products/maester-m",
   "img": "img/velasca-loafer.webp",
   "category": "Shoes",
   "live": true
  },
  "faloni-poplin": {
   "brand": "Luca Faloni",
   "name": "White poplin shirt",
   "price": 260.0,
   "url": "https://lucafaloni.com/en/us/shop/shirts/white-poplin-cotton-shirt",
   "img": "img/faloni-poplin.webp",
   "category": "Shirting",
   "live": true
  },
  "viola-tie": {
   "brand": "Viola Milano",
   "name": "Cashmere tie, navy",
   "price": 114.0,
   "url": "https://www.violamilano.com/product/solid-handrolled-100-cashmere-tie-navy/",
   "img": "img/viola-tie.webp",
   "category": "Neckwear",
   "live": true
  },
  "sunspel-merino": {
   "brand": "Sunspel",
   "name": "Extra-fine merino crew",
   "price": 275.0,
   "url": "https://us.sunspel.com/products/mens-extra-fine-merino-crew-neck-jumper-in-bakelite-mjum8332-rdel",
   "img": "img/sunspel-merino.webp",
   "category": "Knitwear",
   "live": true
  },
  "dents-gloves": {
   "brand": "Dents",
   "name": "Cashmere-lined gloves",
   "price": 391.0,
   "url": "https://us.dentsgloves.com/products/mens-cashmere-lined-deerskin-leather-gloves",
   "img": "img/dents-gloves.webp",
   "category": "Leather",
   "live": true
  },
  "velasca-belt": {
   "brand": "Velasca",
   "name": "Cognac calf belt",
   "price": 90.0,
   "url": "https://www.velasca.com/products/cinta-c",
   "img": "img/velasca-belt.webp",
   "category": "Leather",
   "live": true
  },
  "pantherella-socks": {
   "brand": "Pantherella",
   "name": "Cashmere socks",
   "price": 80.0,
   "url": "https://www.pantherella.com/us/6250-dgy-13",
   "img": "img/pantherella-socks.webp",
   "category": "Hosiery",
   "live": true
  }
 },
 "LOOKS": [
  {
   "id": "boardroom",
   "name": "The Boardroom",
   "line": "Charcoal cashmere, white poplin, a navy tie. Monday through Thursday.",
   "pieces": [
    "faloni-blazer",
    "faloni-poplin",
    "viola-tie",
    "velasca-belt",
    "velasca-loafer"
   ]
  },
  {
   "id": "friday",
   "name": "Friday in Cashmere",
   "line": "No tie, no jacket. Silk-cashmere and a penny loafer.",
   "pieces": [
    "faloni-crew",
    "velasca-belt",
    "velasca-loafer",
    "pantherella-socks"
   ]
  },
  {
   "id": "november",
   "name": "Ohio in November",
   "line": "Fine merino, cashmere-lined deerskin, warm feet.",
   "pieces": [
    "sunspel-merino",
    "dents-gloves",
    "pantherella-socks",
    "velasca-loafer"
   ]
  }
 ]
};
