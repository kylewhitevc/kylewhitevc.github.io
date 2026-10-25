/* Kyle White Links: looks data, the single source for "Shop my outfits".
   Same contract as EREDO's looks.json: links{KEY:{url,brand,name,price(now),was(original or null),img,live}},
   looks[{id,name,note,pieces:[KEY]}]. Prices read off each merchant page (Oct 25 2026).
   A piece whose key is missing or live:false hides itself; a look with fewer than 2 live pieces hides itself.
   CI fails on a missing key, a non-https url, a missing image, or was < price. */
window.KW_LOOKS = {
 "house": "kyle",
 "links": {
  "brioni-shirt": {
   "url": "https://italist.com/products/brioni-shirt-navy-1876860043",
   "brand": "Brioni",
   "name": "Navy cotton shirt",
   "price": 488.6,
   "was": 1453.55,
   "img": "img/deal-s3.webp",
   "live": true
  },
  "dg-silk-tie": {
   "url": "https://www.italist.com/products/dolce-gabbana-necktie-blue-390219",
   "brand": "Dolce & Gabbana",
   "name": "Blue silk necktie",
   "price": 132.56,
   "was": 530.23,
   "img": "img/deal-i2.webp",
   "live": true
  },
  "zegna-oasi-coat": {
   "url": "https://italist.com/products/zegna-cashmere-coat-navy-6411339915",
   "brand": "Zegna",
   "name": "Oasi cashmere coat",
   "price": 3032.69,
   "was": 9189.97,
   "img": "img/deal-s2.webp",
   "live": true
  },
  "gobi-turtleneck": {
   "url": "https://us.gobicashmere.com/products/mens-cashmere-turtleneck-charcaol",
   "brand": "GOBI Cashmere",
   "name": "Cashmere turtleneck",
   "price": 159.5,
   "was": 319.0,
   "img": "img/deal-k4.webp",
   "live": true
  },
  "brioni-desert-jacket": {
   "url": "https://italist.com/products/brioni-jacket-navy-2821015691",
   "brand": "Brioni",
   "name": "Navy desert jacket",
   "price": 1732.13,
   "was": 4441.36,
   "img": "img/deal-s6.webp",
   "live": true
  },
  "tods-gommino": {
   "url": "https://italist.com/products/tod-s-loafer-gray-2238466187",
   "brand": "Tod's",
   "name": "Gommino driving loafer",
   "price": 357.6,
   "was": 1117.49,
   "img": "img/deal-s5.webp",
   "live": true
  },
  "naadam-quarter-zip": {
   "url": "https://naadam.co/products/cotton-cashmere-textured-quarter-zip",
   "brand": "Naadam",
   "name": "Cotton-cashmere quarter zip",
   "price": 68.88,
   "was": 168.0,
   "img": "img/deal-k1.webp",
   "live": true
  },
  "missoni-scarf": {
   "url": "https://www.italist.com/products/missoni-scarf-gray-267019",
   "brand": "Missoni",
   "name": "Striped wool scarf",
   "price": 127.54,
   "was": 607.31,
   "img": "img/deal-i1.webp",
   "live": true
  },
  "corneliani-polo": {
   "url": "https://italist.com/products/corneliani-polo-gray-338699",
   "brand": "Corneliani",
   "name": "Long-sleeve cotton polo",
   "price": 126.11,
   "was": 630.56,
   "img": "img/deal-s1.webp",
   "live": true
  }
 },
 "looks": [
  {
   "id": "boardroom",
   "name": "The Boardroom",
   "note": "Navy on navy under a Zegna Oasi cashmere coat.",
   "pieces": [
    "brioni-shirt",
    "dg-silk-tie",
    "zegna-oasi-coat"
   ]
  },
  {
   "id": "friday",
   "name": "Friday in Cashmere",
   "note": "Cashmere turtleneck, a Brioni desert jacket, Gomminos.",
   "pieces": [
    "gobi-turtleneck",
    "brioni-desert-jacket",
    "tods-gommino"
   ]
  },
  {
   "id": "november",
   "name": "Ohio in November",
   "note": "Soft layers and a Missoni scarf for the cold.",
   "pieces": [
    "corneliani-polo",
    "naadam-quarter-zip",
    "missoni-scarf"
   ]
  }
 ]
};
