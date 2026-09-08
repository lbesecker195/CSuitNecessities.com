#!/usr/bin/env python3
"""
Fetch editorial photography from Unsplash for every product in data/offers.yaml
and write the image URL + required attribution back into the catalog.

Usage:
    export UNSPLASH_ACCESS_KEY=xxxxxxxx
    python3 tools/fetch_unsplash.py            # all products
    python3 tools/fetch_unsplash.py sony-xm5   # just one

Follows the Unsplash API Guidelines:
  * hotlinks images.unsplash.com (their preferred method, keeps view counts working)
  * records photographer + profile link for on-page attribution
  * appends the required utm_source / utm_medium referral params
  * pings the /download_location endpoint on selection
"""
import json, os, sys, time, urllib.parse, urllib.request
import yaml

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "").strip()
APP = "C-Suit%20Necessities"           # utm_source, per Unsplash guidelines
UA = "CSuitNecessities/1.0"

if not KEY:
    sys.exit("Set UNSPLASH_ACCESS_KEY first (https://unsplash.com/developers -> New Application)")

# ---------------------------------------------------------------------------
# Hand-written search terms. The literal product name returns nothing useful on
# a stock library, so each product maps to the scene/subject that reads as "this
# category" to an executive audience. Orientation is forced to landscape.
# ---------------------------------------------------------------------------
QUERY = {
 # Executive Leather
 "saddleback-briefcase":      "brown leather briefcase",
 "bellroy-tokyo":             "canvas messenger bag commuter",
 "leatherology-padfolio":     "leather folio meeting notes",
 "shinola-valet-tray":        "leather valet tray watch keys",
 "tumi-alpha3-brief":         "business laptop bag",
 # Writing Instruments
 "montblanc-149":             "fountain pen signing document",
 "waterman-carene":           "luxury pen on desk",
 "lamy-2000":                 "minimalist fountain pen",
 "leuchtturm-master":         "open notebook fountain pen desk",
 "parker-duofold":            "vintage fountain pen closeup",
 # Acoustic Privacy
 "sony-xm5":                  "over ear headphones desk",
 "bose-qc-ultra":             "headphones airplane travel",
 "jabra-speak2-75":           "hotel room desk laptop call",
 "snooz":                     "closed office door hallway",
 "airpods-max":               "white over ear headphones",
 "sennheiser-momentum-4":     "headphones on wooden desk",
 # Ergonomic Furniture
 "herman-miller-aeron":       "mesh task chair office",
 "steelcase-gesture":         "black executive office chair",
 "ergotron-hx":               "curved monitor office workspace",
 "flexispot-e7-pro":          "standing desk office",
 "haworth-fern":              "designer office chair",
 # Travel Gear
 "tumi-alpha3-carryon":       "carry on luggage airport",
 "samsonite-cosmolite":       "hard shell suitcase travel",
 "anker-prime-240w":          "usb c charger cables desk",
 "peak-design-tech-pouch":    "travel tech organizer pouch cables",
 "rimowa-original-cabin":     "aluminium suitcase travel",
 "briggs-riley-baseline":     "black suitcase business travel",
 # Desk Technology
 "insta360-link2":            "webcam video call desk",
 "benq-screenbar-pro":        "desk lamp monitor light",
 "caldigit-ts4":              "laptop docking station desk",
 "remarkable-paper-pro":      "e ink tablet stylus notes",
 "obsbot-tiny-2":             "webcam on monitor",
 "logitech-brio-4k":          "video conference home office",
 # Desk Coffee
 "ember-mug-2":               "coffee mug on desk laptop",
 "nespresso-creatista-pro":   "espresso machine office kitchen",
 "fellow-stagg-ekg-pro":      "gooseneck kettle pour over",
 "zojirushi-sm-khe48":        "stainless steel travel mug",
 "cauldryn-coffee":           "insulated travel flask",
 "fellow-carter-move":        "ceramic travel coffee mug",
 # Wellness and Recovery
 "theragun-pro-plus":         "massage gun recovery",
 "kingsmith-walkingpad-x21":  "walking treadmill home office",
 "gunnar-vertex":             "glasses computer screen desk",
 "coway-airmega-400s":        "air purifier modern room",
 "hyperice-hypervolt-2-pro":  "percussion massage device",
 "oura-ring-horizon":         "smart ring wearable",
 "whoop-4":                   "fitness tracker wrist band",
 # Office Decor
 "howard-miller-burton":      "wooden mantel clock",
 "dalvey-grand-sedan":        "brass desk clock",
 "authentic-models-sandtimer":"hourglass sand timer desk",
 "carrara-bookends":          "marble bookends books shelf",
 "jaeger-atmos-homage":       "glass skeleton clock",
 # Hardware Security
 "yubikey-5c-nfc":            "security key usb authentication",
 "3m-gold-privacy-filter":    "laptop screen airport lounge",
 "mission-darkness-faraday":  "black tactical laptop bag",
 "fellowes-99ci":             "paper shredder office documents",
 "kingston-ironkey-vp80":     "encrypted external ssd drive",
}


def api(path, **params):
    url = f"https://api.unsplash.com{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Client-ID {KEY}",
        "Accept-Version": "v1",
        "User-Agent": UA,
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r), r.headers.get("X-Ratelimit-Remaining")


def ping_download(photo):
    """Unsplash API Guidelines: notify on download/selection."""
    loc = (photo.get("links") or {}).get("download_location")
    if not loc:
        return
    try:
        req = urllib.request.Request(loc, headers={
            "Authorization": f"Client-ID {KEY}", "User-Agent": UA})
        urllib.request.urlopen(req, timeout=15).read()
    except Exception:
        pass


def pick(key, query, used=frozenset()):
    data, remaining = api("/search/photos", query=query, per_page=10,
                          orientation="landscape", content_filter="high")
    results = data.get("results") or []
    # Never let two products share a photo — it reads as lazy and kills trust.
    p = next((r for r in results if r["id"] not in used), None)
    if not p:
        return None, remaining
    ping_download(p)
    raw = p["urls"]["raw"]
    # Unsplash dynamic resizing — one URL, right size, modern format.
    img = raw + "&w=1200&h=750&fit=crop&crop=entropy&q=80&fm=jpg"
    user = p["user"]
    return {
        "image": img,
        "imageAlt": (p.get("alt_description") or query).strip().capitalize(),
        "photoCredit": user["name"],
        "photoCreditUrl": f'{user["links"]["html"]}?utm_source={APP}&utm_medium=referral',
        "photoId": p["id"],
    }, remaining


def main():
    path = os.path.join(SITE, "data/offers.yaml")
    header = []
    with open(path) as f:
        raw = f.read()
    for line in raw.splitlines():
        if line.startswith("#") or not line.strip():
            header.append(line)
        else:
            break
    offers = yaml.safe_load(raw)

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    force = "--force" in sys.argv
    only = args or None
    hits = misses = skipped = 0
    used = {v["photoId"] for v in offers.values() if v.get("photoId")}
    for key, o in offers.items():
        if only and key not in only:
            continue
        # Resumable: leave products that already have a photo alone unless --force.
        if o.get("photoId") and not force:
            skipped += 1
            continue
        q = QUERY.get(key)
        if not q:
            print(f"SKIP {key}: no query defined")
            continue
        try:
            found, remaining = pick(key, q, used)
        except Exception as e:
            print(f"FAIL {key}: {e}")
            break
        if not found:
            print(f"MISS {key}  (query: {q})")
            misses += 1
            continue
        o.update(found)
        used.add(found["photoId"])
        hits += 1
        print(f"OK   {key:30s} {found['photoCredit'][:22]:22s} rate-limit left: {remaining}")
        sys.stdout.flush()
        time.sleep(0.4)

    with open(path, "w") as f:
        f.write("\n".join(header).rstrip() + "\n\n")
        yaml.safe_dump(offers, f, sort_keys=False, allow_unicode=True, width=100)
    print(f"\n{hits} set, {misses} missed, {skipped} already had photos -> data/offers.yaml")
    remaining = [k for k, v in offers.items() if not v.get("photoId")]
    if remaining:
        print(f"{len(remaining)} still without a photo: {' '.join(remaining)}")


if __name__ == "__main__":
    main()
