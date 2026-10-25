/* Kyle White Links: the single outfit for "Shop the look" (CEO order Oct 25 2026: one complete, coherent outfit).
   Same contract as EREDO's looks.json: links{KEY:{url,brand,name,price(now),was(original or null),img,live}},
   looks[{id,name,note,pieces:[KEY]}]. Prices and in-stock sizes read off each product page Oct 25 2026.
   CI fails on a missing key, a non-https url, a missing image, or was < price. */
window.KW_LOOKS = {
 "house": "kyle",
 "links": {
  "tagliatore-navy-blazer": {
   "url": "https://italist.com/products/tagliatore-blazer-blue-7169182859",
   "brand": "Tagliatore",
   "name": "Montecarlo navy wool blazer",
   "price": 619.06,
   "was": 965.73,
   "img": "img/look-jacket.webp",
   "live": true
  },
  "gobi-taupe-rollneck": {
   "url": "https://us.gobicashmere.com/products/mens-turtle-neck-taupe",
   "brand": "GOBI Cashmere",
   "name": "Taupe cashmere roll-neck",
   "price": 159.0,
   "was": null,
   "img": "img/look-turtleneck.webp",
   "live": true
  },
  "cucinelli-grey-trousers": {
   "url": "https://italist.com/products/brunello-cucinelli-trousers-gray-3444545675",
   "brand": "Brunello Cucinelli",
   "name": "Grey merino pleated trousers",
   "price": 1115.09,
   "was": 2424.1,
   "img": "img/look-trousers.webp",
   "live": true
  },
  "cj-suede-loafer": {
   "url": "https://italist.com/products/crockett-jones-loafer-brown-6293670027",
   "brand": "Crockett & Jones",
   "name": "Brown suede penny loafer",
   "price": 563.52,
   "was": 845.28,
   "img": "img/look-loafer.webp",
   "live": true
  },
  "slowear-woven-belt": {
   "url": "https://italist.com/products/slowear-belt-brown-5783522443",
   "brand": "Slowear",
   "name": "Woven brown leather belt",
   "price": 266.7,
   "was": 400.05,
   "img": "img/look-belt.webp",
   "live": true
  },
  "cucinelli-brown-scarf": {
   "url": "https://italist.com/products/brunello-cucinelli-scarf-brown-2709342347",
   "brand": "Brunello Cucinelli",
   "name": "Ribbed brown cashmere scarf",
   "price": 630.4,
   "was": 1189.43,
   "img": "img/look-scarf.webp",
   "live": true
  }
 },
 "looks": [
  {
   "id": "ohio-autumn",
   "name": "Navy, Taupe & Suede",
   "note": "A navy Tagliatore blazer over taupe cashmere, Cucinelli grey merino, brown suede and woven leather.",
   "pieces": [
    "tagliatore-navy-blazer",
    "gobi-taupe-rollneck",
    "cucinelli-grey-trousers",
    "cj-suede-loafer",
    "slowear-woven-belt",
    "cucinelli-brown-scarf"
   ]
  }
 ]
};
