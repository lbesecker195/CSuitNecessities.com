#!/usr/bin/env python3
"""Generate data/offers.yaml + product placeholder SVGs for C-Suit Necessities."""
import os, yaml, html, textwrap

SITE = "/Users/logan/Documents/businesses/C-Suit Reccuring Affiliate/site"
IMGDIR = os.path.join(SITE, "static/img/products")
os.makedirs(IMGDIR, exist_ok=True)

# category -> (title, accent hex, glyph path in 0..40 box)
# Display names deliberately avoid "&" so the taxonomy URLs stay clean.
CATS = {
 "leather-edc": ("Executive Leather", "#b45309"),
 "writing":     ("Writing Instruments", "#7c3aed"),
 "audio":       ("Acoustic Privacy", "#0ea5e9"),
 "furniture":   ("Ergonomic Furniture", "#059669"),
 "travel":      ("Travel Gear", "#dc2626"),
 "video":       ("Desk Technology", "#2563eb"),
 "beverage":    ("Desk Coffee", "#c2410c"),
 "wellness":    ("Wellness and Recovery", "#16a34a"),
 "decor":       ("Office Decor", "#a16207"),
 "security":    ("Hardware Security", "#475569"),
}

# ---------------------------------------------------------------------------
#  PRODUCT CATALOG
#  asin: "" -> the amzn.html partial falls back to a tagged Amazon SEARCH link,
#  which works immediately. Fill asin values in later to switch to direct links.
# ---------------------------------------------------------------------------
P = {}
def add(key, cat, name, brand, search, rating, tagline, deal, cta, bullets, compare, target=True):
    P[key] = dict(name=name, brand=brand, asin="", search=search, rating=rating,
                  tagline=tagline, deal=deal, cta=cta, bullets=bullets,
                  compare=compare, category=cat, target=target,
                  image=f"/img/products/{key}.svg",
                  domain="amazon.com")

# ---- 1. Leather & EDC -------------------------------------------------------
LROWS = ["Best for", "Leather / shell", "Weight", "Laptop fit", "Warranty", "Rating"]
add("saddleback-briefcase","leather-edc",
    "Saddleback Leather Thin Front Pocket Briefcase","Saddleback Leather Co.",
    "Saddleback Leather Thin Front Pocket Briefcase","4.8",
    "Full-grain boot leather, zero zippers to break","100-year leather — often ships with a free hobo bag",
    "Check Price on Amazon",
    ["Thick full-grain leather that only looks better scuffed",
     "No zippers, no fragile hardware — buckles and rivets only",
     "Fits most 15-inch laptops with room for a legal pad"],
    {"Best for":"Buy-it-once ruggedness","Leather / shell":'Full-grain "boot" leather',
     "Weight":"~4.5 lb empty","Laptop fit":"Up to 15 in","Warranty":"100 years","Rating":"4.8 / 5"})
add("bellroy-tokyo","leather-edc",
    "Bellroy Tokyo Work Bag (Premium)","Bellroy",
    "Bellroy Tokyo Work Bag Premium leather","4.6",
    "The minimalist's board-meeting-to-boarding-gate bag","",
    "Check Price on Amazon",
    ["Weather-resistant leather with a clean, low-profile silhouette",
     "Dedicated slots for two phones, cables and a charger",
     "Luggage pass-through sleeve for airport transit"],
    {"Best for":"Slim modern organization","Leather / shell":"Env. certified leather",
     "Weight":"~2.4 lb empty","Laptop fit":"Up to 16 in","Warranty":"3 years","Rating":"4.6 / 5"})
add("leatherology-padfolio","leather-edc",
    "Leatherology Zip-Around Executive Padfolio","Leatherology",
    "Leatherology Zip Around Executive Padfolio full grain","4.7",
    "Full-grain Italian leather for device-free rooms","Free monogramming on most orders",
    "Check Price on Amazon",
    ["Full-grain leather that ages into a personal patina",
     "Gusset expands for pitch decks; fits letter or A4 pads",
     "Smooth perimeter zip and a clear pen-loop"],
    {"Best for":"Paper-only executive sessions","Leather / shell":"Full-grain Italian",
     "Weight":"~1.6 lb","Laptop fit":"Tablet only","Warranty":"1 year","Rating":"4.7 / 5"})
add("shinola-valet-tray","leather-edc",
    "Shinola Detroit Large Leather Catchall Tray","Shinola",
    "Shinola Detroit Large Leather Catchall Valet Tray","4.7",
    "Structured veg-tan leather that ends desk clutter","",
    "Check Price on Amazon",
    ["Vegetable-tanned leather with firm, snap-stud corners",
     "Deep enough to hold a watch, rings, keys and AirPods",
     "Small footprint that fits beside a keyboard"],
    {"Best for":"Watch + EDC landing zone","Leather / shell":"Vegetable-tanned",
     "Weight":"~0.5 lb","Laptop fit":"n/a","Warranty":"Lifetime (defects)","Rating":"4.7 / 5"})
add("tumi-alpha3-brief","leather-edc",
    "Tumi Alpha 3 Compact Brief","Tumi",
    "Tumi Alpha 3 Compact Laptop Brief","4.7",
    "Ballistic-nylon brief with technical pockets everywhere","Tumi Tracer registration included",
    "Check Price on Amazon",
    ["FXT ballistic nylon shrugs off airport abuse",
     "Add-a-bag sleeve and dedicated tech organization",
     "Lighter than a leather brief of the same volume"],
    {"Best for":"Max organization, min weight","Leather / shell":"FXT ballistic nylon",
     "Weight":"~2.9 lb empty","Laptop fit":"Up to 15 in","Warranty":"5 years","Rating":"4.7 / 5"},
    target=False)

# ---- 2. Writing -----------------------------------------------------------
WROWS = ["Best for","Type","Nib / tip","Maintenance","Refill cost","Rating"]
add("montblanc-149","writing",
    "Montblanc Meisterstück 149 Fountain Pen","Montblanc",
    "Montblanc Meisterstuck 149 Fountain Pen","4.8",
    "The signature that closes the deal","",
    "Check Price on Amazon",
    ["Hand-ground 18K gold nib with a touch of spring",
     "Piston filler holds a huge ink reserve for signing marathons",
     "Substantial barrel that photographs like status"],
    {"Best for":"Public-facing prestige","Type":"Fountain","Nib / tip":"18K gold",
     "Maintenance":"Flush monthly","Refill cost":"Bottled ink, cheap","Rating":"4.8 / 5"})
add("waterman-carene","writing",
    "Waterman Carène Rollerball","Waterman",
    "Waterman Carene Rollerball Pen Black Sea","4.7",
    "Fountain-pen elegance, zero fuss","",
    "Check Price on Amazon",
    ["Lacquered, contoured body with a real brass core",
     "Instant ink laydown — grab it and sign",
     "Firm cap snap that survives a jacket pocket"],
    {"Best for":"Low-maintenance daily driver","Type":"Rollerball","Nib / tip":"Steel rollerball",
     "Maintenance":"None","Refill cost":"$8–12 each","Rating":"4.7 / 5"})
add("lamy-2000","writing",
    "Lamy 2000 Fountain Pen (Makrolon)","Lamy",
    "Lamy 2000 Fountain Pen Makrolon","4.8",
    "Bauhaus restraint for the discreet founder","",
    "Check Price on Amazon",
    ["Seamless Makrolon and brushed-steel body from 1966",
     "Hooded 14K gold nib, spring-loaded clip",
     "Disappears in the hand on long strategy memos"],
    {"Best for":"Understated design lovers","Type":"Fountain","Nib / tip":"14K hooded gold",
     "Maintenance":"Flush monthly","Refill cost":"Bottled ink, cheap","Rating":"4.8 / 5"})
add("leuchtturm-master","writing",
    "Leuchtturm1917 Master Slim A4+ Notebook","Leuchtturm1917",
    "Leuchtturm1917 Master Slim A4 Hardcover Notebook","4.7",
    "A full sheet of thinking room, archival paper","",
    "Check Price on Amazon",
    ["Oversized A4+ pages for real mind-mapping",
     "100 g/m² paper resists fountain-ink bleed and ghosting",
     "Numbered pages, index and lay-flat thread binding"],
    {"Best for":"Strategic planning at scale","Type":"Notebook","Nib / tip":"100 g/m² paper",
     "Maintenance":"n/a","Refill cost":"Whole notebook","Rating":"4.7 / 5"})
add("parker-duofold","writing",
    "Parker Duofold Prestige Centennial","Parker",
    "Parker Duofold Prestige Centennial Fountain Pen","4.6",
    "Heritage prestige at a saner price than Montblanc","",
    "Check Price on Amazon",
    ["Solid 18K/22K gold nib with a classic profile",
     "Cartridge/converter fill for travel convenience",
     "Grippy, secure clip"],
    {"Best for":"Prestige without the 149 tax","Type":"Fountain","Nib / tip":"18K gold",
     "Maintenance":"Flush monthly","Refill cost":"Cartridges or ink","Rating":"4.6 / 5"},
    target=False)

# ---- 3. Audio -----------------------------------------------------------
AROWS = ["Best for","Mic on calls","ANC","Battery","Multipoint","Rating"]
add("sony-xm5","audio",
    "Sony WH-1000XM5 Noise-Canceling Headphones","Sony",
    "Sony WH-1000XM5 Wireless Noise Canceling Headphones","4.7",
    "The desk sanctuary for investor calls","Frequent Amazon price drops — check today's",
    "Check Price on Amazon",
    ["Class-leading low-frequency (cabin / HVAC) cancellation",
     "8-mic beamforming keeps your voice clean on calls",
     "~30 hr battery and fast multipoint switching"],
    {"Best for":"Calls + focus at the desk","Mic on calls":"Excellent","ANC":"Class-leading",
     "Battery":"~30 hr","Multipoint":"Yes (2)","Rating":"4.7 / 5"})
add("bose-qc-ultra","audio",
    "Bose QuietComfort Ultra Headphones","Bose",
    "Bose QuietComfort Ultra Headphones over ear","4.6",
    "Red-eye comfort with the best clamp balance","",
    "Check Price on Amazon",
    ["Lightest long-haul clamp pressure of the flagships",
     "Immersive spatial audio for hybrid conference calls",
     "Compact fold-flat travel case"],
    {"Best for":"Long-haul travel comfort","Mic on calls":"Very good","ANC":"Excellent",
     "Battery":"~24 hr","Multipoint":"Yes (2)","Rating":"4.6 / 5"})
add("jabra-speak2-75","audio",
    "Jabra Speak2 75 Conference Speakerphone","Jabra",
    "Jabra Speak2 75 Speakerphone","4.6",
    "Turns any hotel room into a boardroom","",
    "Check Price on Amazon",
    ["Full-duplex — nobody gets clipped when two people talk",
     "Acoustic voice-leveling normalizes near/far speakers",
     "USB-C and Bluetooth with a carry pouch"],
    {"Best for":"Room calls off a laptop","Mic on calls":"360° room pickup","ANC":"Noise suppression",
     "Battery":"~32 hr","Multipoint":"USB + BT","Rating":"4.6 / 5"})
add("snooz","audio",
    "SNOOZ Real-Fan White Noise Machine","SNOOZ",
    "SNOOZ White Noise Sound Machine fan","4.6",
    "Sound-masking so hallway ears hear nothing","",
    "Check Price on Amazon",
    ["Real mechanical fan — no looping digital hiss",
     "Tunable tone and volume; app schedules",
     "Small enough to hide on a credenza"],
    {"Best for":"Office confidentiality masking","Mic on calls":"n/a","ANC":"Sound masking",
     "Battery":"AC powered","Multipoint":"n/a","Rating":"4.6 / 5"})
add("airpods-max","audio",
    "Apple AirPods Max","Apple",
    "Apple AirPods Max","4.7",
    "Seamless in an all-Apple executive stack","",
    "Check Price on Amazon",
    ["Instant switching across iPhone, iPad and Mac",
     "Excellent ANC and build; heavier on the head",
     "Best-in-class transparency mode"],
    {"Best for":"All-Apple households","Mic on calls":"Very good","ANC":"Excellent",
     "Battery":"~20 hr","Multipoint":"Apple devices","Rating":"4.7 / 5"},
    target=False)
add("sennheiser-momentum-4","audio",
    "Sennheiser Momentum 4 Wireless","Sennheiser",
    "Sennheiser Momentum 4 Wireless Headphones","4.5",
    "Marathon 60-hour battery and warm tuning","",
    "Check Price on Amazon",
    ["~60 hr battery outlasts any travel week",
     "Comfortable, low-profile fit",
     "Rich sound signature; ANC a step behind Sony/Bose"],
    {"Best for":"Battery life above all","Mic on calls":"Good","ANC":"Very good",
     "Battery":"~60 hr","Multipoint":"Yes (2)","Rating":"4.5 / 5"},
    target=False)

# ---- 4. Furniture -----------------------------------------------------------
FROWS = ["Best for","Support type","Cooling","Key adjustments","Warranty","Rating"]
add("herman-miller-aeron","furniture",
    "Herman Miller Aeron (PostureFit SL)","Herman Miller",
    "Herman Miller Aeron Chair PostureFit SL size B","4.7",
    "The corner-office standard for 12-hour days","Certified-refurb units on Amazon cost far less",
    "Check Price on Amazon",
    ["8Z Pellicle mesh — no sweat build-up over long sessions",
     "PostureFit SL stabilizes the sacrum and lumbar together",
     "Forward-tilt for heads-down review work"],
    {"Best for":"All-day desk marathons","Support type":"Suspended mesh","Cooling":"Excellent",
     "Key adjustments":"Tilt, PostureFit, arms","Warranty":"12 years","Rating":"4.7 / 5"})
add("steelcase-gesture","furniture",
    "Steelcase Gesture Office Chair","Steelcase",
    "Steelcase Gesture Office Chair with Headrest","4.7",
    "Arms that follow you to every device","",
    "Check Price on Amazon",
    ["360° arms support phone, tablet and keyboard postures",
     "Deep recline with weight-activated tracking",
     "Cushioned seat contours without going soft"],
    {"Best for":"Phone/tablet-heavy days","Support type":"Cushioned contour","Cooling":"Moderate",
     "Key adjustments":"4D arms, depth, recline","Warranty":"12 years","Rating":"4.7 / 5"})
add("ergotron-hx","furniture",
    "Ergotron HX Heavy-Duty Monitor Arm","Ergotron",
    "Ergotron HX Desk Monitor Arm","4.7",
    "Holds a 49-inch ultrawide with zero sag","",
    "Check Price on Amazon",
    ["Rated for large, heavy panels up to ~42 lb",
     "CF (Constant Force) lift repositions with a fingertip",
     "Clean internal cable routing"],
    {"Best for":"Big curved ultrawides","Support type":"Desk clamp arm","Cooling":"n/a",
     "Key adjustments":"Height, tilt, pan","Warranty":"10 years","Rating":"4.7 / 5"})
add("flexispot-e7-pro","furniture",
    "FlexiSpot E7 Pro Standing Desk","FlexiSpot",
    "FlexiSpot E7 Pro Commercial Standing Desk Frame","4.7",
    "Rock-solid at standing height while you type fast","",
    "Check Price on Amazon",
    ["Dual motors and heavy-gauge steel kill monitor wobble",
     "Quiet lift with accurate memory presets",
     "Anti-collision sensing and a wide height range"],
    {"Best for":"Shake-free sit/stand","Support type":"Dual-motor base","Cooling":"n/a",
     "Key adjustments":"Height presets","Warranty":"15 yr frame","Rating":"4.7 / 5"})
add("haworth-fern","furniture",
    "Haworth Fern Executive","Haworth",
    "Haworth Fern Office Chair","4.6",
    "Flexible 'digital knit' back that moves with the spine","",
    "Check Price on Amazon",
    ["Wave-suspension back flexes segment by segment",
     "Warm, residential look for a client-facing office",
     "Lighter recline feel than the Aeron"],
    {"Best for":"Spinal-flex comfort","Support type":"Flexible knit back","Cooling":"Good",
     "Key adjustments":"Tilt, lumbar, arms","Warranty":"12 years","Rating":"4.6 / 5"},
    target=False)

# ---- 5. Travel -----------------------------------------------------------
TROWS = ["Best for","Shell","Empty weight","Warranty","Wheels","Rating"]
add("tumi-alpha3-carryon","travel",
    "Tumi Alpha 3 Continental Dual Access Carry-On","Tumi",
    "Tumi Alpha 3 Continental Dual Access 4 Wheeled Carry On","4.7",
    "Ballistic-nylon tank with top + front access","Tumi Tracer registration included",
    "Check Price on Amazon",
    ["FXT ballistic nylon survives a decade of gate-checks",
     "Dual access — grab the laptop without unpacking",
     "Internal suiter brackets and add-a-bag sleeve"],
    {"Best for":"Frequent mixed-carrier flying","Shell":"FXT ballistic nylon",
     "Empty weight":"~9.9 lb","Warranty":"5 yr + 1 full","Wheels":"Dual spinner","Rating":"4.7 / 5"})
add("samsonite-cosmolite","travel",
    "Samsonite Black Label Cosmolite 3.0 Spinner","Samsonite",
    "Samsonite Cosmolite 3.0 Spinner","4.6",
    "Curv shell armor under 4.5 lb","",
    "Check Price on Amazon",
    ["Curv thermoplastic — huge impact resistance for the weight",
     "Shell flexes and springs back instead of cracking",
     "More packing allowance before you hit weight limits"],
    {"Best for":"Packing heavy without penalty","Shell":"Curv composite",
     "Empty weight":"~4.4 lb","Warranty":"10 years","Wheels":"Dual spinner","Rating":"4.6 / 5"})
add("anker-prime-240w","travel",
    "Anker Prime 240W GaN Desktop Charger","Anker",
    "Anker Prime 240W GaN Desktop Charger 4 port","4.7",
    "One plug for the laptop, tablet, phone and buds","",
    "Check Price on Amazon",
    ["240W across 4 ports — full-speed MacBook Pro plus 3 more",
     "Smart power reallocation as devices come and go",
     "Tiny footprint for the wattage; retains its cable"],
    {"Best for":"Killing the brick pile","Shell":"n/a",
     "Empty weight":"~1.3 lb","Warranty":"2 years","Wheels":"n/a","Rating":"4.7 / 5"})
add("peak-design-tech-pouch","travel",
    "Peak Design Tech Pouch","Peak Design",
    "Peak Design Tech Pouch","4.8",
    "Origami organizer that opens flat on the tray table","",
    "Check Price on Amazon",
    ["Folding pocket geometry keeps every dongle visible",
     "Weatherproof recycled shell and smooth zips",
     "Holds its shape stuffed to capacity"],
    {"Best for":"Cable + adapter control","Shell":"Weatherproof nylon",
     "Empty weight":"~0.5 lb","Warranty":"Lifetime","Wheels":"n/a","Rating":"4.8 / 5"})
add("rimowa-original-cabin","travel",
    "Rimowa Original Cabin (Aluminum)","Rimowa",
    "Rimowa Original Cabin aluminum suitcase","4.6",
    "Anodized aluminum status — dents and all","",
    "Check Price on Amazon",
    ["Grooved aluminum shell; a lifetime of character marks",
     "Heavier and pricier than composites",
     "5-year warranty, global service network"],
    {"Best for":"Status + repairability","Shell":"Anodized aluminum",
     "Empty weight":"~9.7 lb","Warranty":"5 years","Wheels":"Dual spinner","Rating":"4.6 / 5"},
    target=False)
add("briggs-riley-baseline","travel",
    "Briggs & Riley Baseline Essential Carry-On","Briggs & Riley",
    "Briggs Riley Baseline Essential Carry On Spinner","4.8",
    "The 'if it breaks we fix it, forever' bag","",
    "Check Price on Amazon",
    ["Unconditional lifetime repair — even airline damage",
     "Outsider handle frees up all interior space",
     "CX compression-expansion for overpackers"],
    {"Best for":"Zero-hassle warranty","Shell":"Ballistic nylon",
     "Empty weight":"~8.0 lb","Warranty":"Lifetime, unconditional","Wheels":"Dual spinner","Rating":"4.8 / 5"},
    target=False)

# ---- 6. Video -----------------------------------------------------------
VROWS = ["Best for","Sensor / optics","Tracking","Mic","Setup","Rating"]
add("insta360-link2","video",
    "Insta360 Link 2 4K AI Webcam","Insta360",
    "Insta360 Link 2 4K AI Webcam gimbal","4.6",
    "A camera operator that follows you to the whiteboard","",
    "Check Price on Amazon",
    ["1/2-inch sensor with real optical-look depth",
     "Physical 2-axis gimbal tracks you across the room",
     "Privacy: lens physically drops when you're muted"],
    {"Best for":"Presenting on camera","Sensor / optics":'1/2" + gimbal',"Tracking":"Mechanical PTZ",
     "Mic":"Dual noise-canceled","Setup":"Plug-and-play","Rating":"4.6 / 5"})
add("benq-screenbar-pro","video",
    "BenQ ScreenBar Pro Monitor Light","BenQ",
    "BenQ ScreenBar Pro Monitor Light Bar","4.7",
    "Desk light with zero screen glare","",
    "Check Price on Amazon",
    ["Asymmetric optics put light on the desk, not the panel",
     "Auto-dims to ambient; auto color temperature",
     "Clamps on thin and curved monitors, no screws"],
    {"Best for":"Evening reading light on camera","Sensor / optics":"Asymmetric LED","Tracking":"n/a",
     "Mic":"n/a","Setup":"Clip-on","Rating":"4.7 / 5"})
add("caldigit-ts4","video",
    "CalDigit TS4 Thunderbolt 4 Dock","CalDigit",
    "CalDigit TS4 Thunderbolt 4 Dock","4.6",
    "One cable: dual displays, 10GbE-class LAN, 98W","",
    "Check Price on Amazon",
    ["18 ports including 2.5GbE and front SD/USB",
     "98W charging drives a 16-inch laptop under load",
     "Stable sleep/wake on macOS and Windows"],
    {"Best for":"Single-cable command center","Sensor / optics":"n/a","Tracking":"n/a",
     "Mic":"Audio in/out","Setup":"1 cable","Rating":"4.6 / 5"})
add("remarkable-paper-pro","video",
    "reMarkable Paper Pro","reMarkable",
    "reMarkable Paper Pro tablet","4.4",
    "PDF markup and strategy drafts with no notifications","",
    "Check Price on Amazon",
    ["Color e-ink with a frontlight for any room",
     "Very low pen latency; paper-like drag",
     "Locked-down device — nothing to distract you"],
    {"Best for":"Distraction-free document review","Sensor / optics":"Color e-ink","Tracking":"n/a",
     "Mic":"n/a","Setup":"Account + sync","Rating":"4.4 / 5"})
add("obsbot-tiny-2","video",
    "OBSBOT Tiny 2 AI Webcam","OBSBOT",
    "OBSBOT Tiny 2 4K AI Webcam","4.4",
    "Gesture-controlled AI PTZ with a big sensor","",
    "Check Price on Amazon",
    ["1/1.5-inch sensor; strong low light",
     "Gesture control for zoom and tracking",
     "Voice-control add-ons via app"],
    {"Best for":"Solo presenters who move","Sensor / optics":'1/1.5" + gimbal',"Tracking":"AI PTZ",
     "Mic":"Dual","Setup":"App recommended","Rating":"4.4 / 5"},
    target=False)
add("logitech-brio-4k","video",
    "Logitech Brio 4K Webcam","Logitech",
    "Logitech Brio 4K Pro Webcam","4.4",
    "The safe fixed-lens 4K default","",
    "Check Price on Amazon",
    ["Reliable 4K with HDR in backlit offices",
     "No moving parts to fail",
     "Windows Hello face login"],
    {"Best for":"Set-and-forget reliability","Sensor / optics":"Fixed wide","Tracking":"Digital crop",
     "Mic":"Dual","Setup":"Plug-and-play","Rating":"4.4 / 5"},
    target=False)

# ---- 7. Beverage -----------------------------------------------------------
BROWS = ["Best for","How it heats","Portable","Cleaning","Battery","Rating"]
add("ember-mug-2","beverage",
    "Ember Temperature Control Smart Mug 2 (14 oz)","Ember",
    "Ember Mug 2 14 oz temperature control","4.5",
    "Coffee held at your exact temperature for 90 minutes","",
    "Check Price on Amazon",
    ["Set a precise temp; it holds there on the coaster",
     "~80 min battery off the coaster",
     "Preset temp works even without the app"],
    {"Best for":"Long meetings at the desk","How it heats":"Active electronic","Portable":"Short trips",
     "Cleaning":"Hand wash","Battery":"~80 min","Rating":"4.5 / 5"})
add("nespresso-creatista-pro","beverage",
    "Nespresso Creatista Pro by Breville","Breville",
    "Nespresso Creatista Pro espresso machine","4.6",
    "Barista-grade flat whites in under two minutes","",
    "Check Price on Amazon",
    ["ThermoJet heats in ~3 seconds",
     "Automatic steam wand textures real microfoam",
     "Touchscreen programs custom drinks"],
    {"Best for":"An office espresso bar","How it heats":"ThermoJet boiler","Portable":"No",
     "Cleaning":"Auto steam purge","Battery":"AC","Rating":"4.6 / 5"})
add("fellow-stagg-ekg-pro","beverage",
    "Fellow Stagg EKG Pro Electric Kettle","Fellow",
    "Fellow Stagg EKG Pro Electric Gooseneck Kettle","4.7",
    "Design-object kettle with to-the-degree control","",
    "Check Price on Amazon",
    ["Variable temperature with a 60-minute hold",
     "Restricted gooseneck spout for a controlled pour",
     "Genuinely handsome on a credenza"],
    {"Best for":"Specialty tea & pour-over","How it heats":"Element + hold","Portable":"No",
     "Cleaning":"Wipe / descale","Battery":"AC","Rating":"4.7 / 5"})
add("zojirushi-sm-khe48","beverage",
    "Zojirushi SM-KHE48 Vacuum Insulated Mug (16 oz)","Zojirushi",
    "Zojirushi SM-KHE48 stainless mug 16 oz","4.7",
    "Passive vacuum insulation that just refuses to quit","",
    "Check Price on Amazon",
    ["Holds heat for hours with no battery",
     "Flip-lock lid — genuinely leakproof in a bag",
     "Slick interior wipes clean"],
    {"Best for":"Commutes and flights","How it heats":"Passive vacuum","Portable":"Excellent",
     "Cleaning":"Easy","Battery":"None","Rating":"4.7 / 5"})
add("cauldryn-coffee","beverage",
    "Cauldryn Coffee Pro Heated Bottle","Cauldryn",
    "Cauldryn Coffee Pro heated travel mug","4.2",
    "Battery mug that can actually boil water","",
    "Check Price on Amazon",
    ["Heats and re-boils on the go with swappable batteries",
     "Bulky; more thermos than mug",
     "Best for field days away from outlets"],
    {"Best for":"Off-grid heating","How it heats":"Active battery","Portable":"Yes (bulky)",
     "Cleaning":"Hand wash","Battery":"Swappable","Rating":"4.2 / 5"},
    target=False)
add("fellow-carter-move","beverage",
    "Fellow Carter Move Mug","Fellow",
    "Fellow Carter Move Mug vacuum","4.6",
    "The nicest-drinking passive travel mug","",
    "Check Price on Amazon",
    ["Ceramic-coated interior — no metallic taste",
     "Splash-safe lid, tapered to fit cup holders",
     "Passive, so no charging ever"],
    {"Best for":"Taste + portability","How it heats":"Passive vacuum","Portable":"Excellent",
     "Cleaning":"Easy","Battery":"None","Rating":"4.6 / 5"},
    target=False)

# ---- 8. Wellness -----------------------------------------------------------
NROWS = ["Best for","What it does","Time per day","Noise","Data","Rating"]
add("theragun-pro-plus","wellness",
    "Theragun PRO Plus Multi-Therapy Device","Therabody",
    "Theragun PRO Plus percussive therapy device","4.5",
    "Melts neck and upper-back tension between meetings","",
    "Check Price on Amazon",
    ["16 mm stroke reaches deep muscle, not just surface",
     "Near-infrared and heat/vibration modes built in",
     "Quiet enough to use with someone in the room"],
    {"Best for":"Acute desk-tension relief","What it does":"Deep percussion","Time per day":"5–10 min",
     "Noise":"Whisper-quiet","Data":"Basic app","Rating":"4.5 / 5"})
add("kingsmith-walkingpad-x21","wellness",
    "KingSmith WalkingPad X21 Under-Desk Treadmill","KingSmith",
    "KingSmith WalkingPad X21 folding treadmill","4.4",
    "Folds flat behind a credenza; 10k steps on calls","",
    "Check Price on Amazon",
    ["Double-fold design stores in a slim gap",
     "Quiet motor — fine on a muted video call",
     "Remote / app speed control"],
    {"Best for":"Step count during calls","What it does":"Low-intensity cardio","Time per day":"30–60 min",
     "Noise":"Low hum","Data":"App steps","Rating":"4.4 / 5"})
add("gunnar-vertex","wellness",
    "Gunnar Optiks Vertex Computer Glasses","Gunnar",
    "Gunnar Optiks Vertex blue light glasses","4.5",
    "Cuts glare and dry-eye on 12-hour screen days","",
    "Check Price on Amazon",
    ["Blocks a high share of artificial blue light",
     "Distortion-free lens; subtle tint on camera",
     "Comfortable arms for all-day wear"],
    {"Best for":"Screen-fatigue reduction","What it does":"Blue-light + AR","Time per day":"All day",
     "Noise":"n/a","Data":"None","Rating":"4.5 / 5"})
add("coway-airmega-400s","wellness",
    "Coway Airmega 400S Smart Air Purifier","Coway",
    "Coway Airmega 400S air purifier","4.7",
    "Keeps a sealed office at near-zero PM2.5","",
    "Check Price on Amazon",
    ["Covers a large private office / suite",
     "Real-time sensor ramps up for cleaning-spray VOCs",
     "Quiet on sleep mode; app + scheduling"],
    {"Best for":"Cognitive stamina in sealed buildings","What it does":"HEPA + carbon","Time per day":"24/7",
     "Noise":"Very low on sleep","Data":"App AQI","Rating":"4.7 / 5"})
add("hyperice-hypervolt-2-pro","wellness",
    "Hyperice Hypervolt 2 Pro","Hyperice",
    "Hyperice Hypervolt 2 Pro massage gun","4.6",
    "Lighter percussion gun with more top-end power","",
    "Check Price on Amazon",
    ["5 speeds, strong stall force, lighter in hand",
     "Bluetooth guided routines",
     "Louder than the Theragun at max"],
    {"Best for":"Power + light weight","What it does":"Deep percussion","Time per day":"5–10 min",
     "Noise":"Moderate","Data":"App routines","Rating":"4.6 / 5"},
    target=False)
add("oura-ring-horizon","wellness",
    "Oura Ring Horizon (Gen 3)","Oura",
    "Oura Ring Horizon Gen 3 smart ring","4.2",
    "Invisible sleep and readiness tracking","Requires a membership",
    "Check Price on Amazon",
    ["Sleep, HRV and readiness with no wrist device",
     "Week-plus battery",
     "Subscription required for full insights"],
    {"Best for":"Discreet recovery data","What it does":"Passive tracking","Time per day":"0 (passive)",
     "Noise":"Silent","Data":"Deep, subscription","Rating":"4.2 / 5"},
    target=False)
add("whoop-4","wellness",
    "WHOOP 4.0","WHOOP",
    "WHOOP 4.0 fitness tracker","4.1",
    "Strain and recovery coaching, screenless","Membership-based",
    "Check Price on Amazon",
    ["Continuous strain / recovery / sleep coaching",
     "No screen; wear it anywhere",
     "Membership pricing model"],
    {"Best for":"Coached strain management","What it does":"Passive tracking","Time per day":"0 (passive)",
     "Noise":"Silent","Data":"Deep, subscription","Rating":"4.1 / 5"},
    target=False)

# ---- 9. Decor -----------------------------------------------------------
DROWS = ["Best for","Movement","Material","Noise","Statement level","Rating"]
add("howard-miller-burton","decor",
    "Howard Miller Burton Mantel Clock","Howard Miller",
    "Howard Miller Burton Mantel Clock","4.7",
    "Traditional gravitas for a credenza","",
    "Check Price on Amazon",
    ["Warm hardwood case with brass accents",
     "Dual chime with an automatic night shut-off",
     "The look of permanence behind a desk"],
    {"Best for":"Classic executive presence","Movement":"Quartz dual-chime","Material":"Hardwood + brass",
     "Noise":"Chime (defeatable)","Statement level":"High","Rating":"4.7 / 5"})
add("dalvey-grand-sedan","decor",
    "Dalvey Grand Sedan Desk Clock","Dalvey",
    "Dalvey Grand Sedan desk clock","4.6",
    "Scottish pocket-watch engineering, shrunk","",
    "Check Price on Amazon",
    ["Convex glass, spun metal dial, jewel-like scale",
     "Weighted base sits firm on a leather blotter",
     "Tarnish-resistant finish"],
    {"Best for":"Refined small-footprint piece","Movement":"Quartz","Material":"Stainless / brass",
     "Noise":"Silent","Statement level":"Medium","Rating":"4.6 / 5"})
add("authentic-models-sandtimer","decor",
    "Authentic Models 60-Minute Brass Sand Timer","Authentic Models",
    "Authentic Models 60 minute brass hourglass sand timer","4.6",
    "A silent, tactile deep-work timer","",
    "Check Price on Amazon",
    ["Flip it to start a distraction-free work block",
     "Heavy brass frame; no phone, no beep",
     "Runs within a minute of a true hour"],
    {"Best for":"Analog time-blocking","Movement":"Sand","Material":"Brass + glass",
     "Noise":"Silent","Statement level":"Medium","Rating":"4.6 / 5"})
add("carrara-bookends","decor",
    "Solid Carrara Marble Bookends","Craftsman",
    "solid Carrara white marble bookends heavy","4.7",
    "5+ lb of stone that never lets a binder lean","",
    "Check Price on Amazon",
    ["Each block is heavy enough for hardbound volumes",
     "Felt base protects the shelf and stops slipping",
     "Natural veining — no two pairs alike"],
    {"Best for":"Anchoring heavy books","Movement":"n/a","Material":"Carrara marble",
     "Noise":"Silent","Statement level":"Medium","Rating":"4.7 / 5"})
add("jaeger-atmos-homage","decor",
    "Luxury Glass Mechanical Mantel Clock","(various)",
    "luxury glass mechanical mantel clock skeleton","4.3",
    "Kinetic mechanical theater on the shelf","",
    "Check Price on Amazon",
    ["Visible mechanical movement as a talking piece",
     "Far cheaper than a real Atmos",
     "Needs occasional adjustment"],
    {"Best for":"Kinetic conversation piece","Movement":"Mechanical","Material":"Glass + metal",
     "Noise":"Soft tick","Statement level":"High","Rating":"4.3 / 5"},
    target=False)

# ---- 10. Security -----------------------------------------------------------
SROWS = ["Best for","Protects against","Standard","Daily friction","Travel","Rating"]
add("yubikey-5c-nfc","security",
    "Yubico YubiKey 5C NFC","Yubico",
    "Yubico YubiKey 5C NFC security key","4.8",
    "A phishing-proof lock for executive email","Buy two — one primary, one backup",
    "Check Price on Amazon",
    ["FIDO2 / WebAuthn stops credential phishing cold",
     "USB-C plus NFC tap for phones",
     "Also does TOTP, Smart Card, OpenPGP"],
    {"Best for":"Account takeover defense","Protects against":"Phishing / credential theft",
     "Standard":"FIDO2, FIPS opt.","Daily friction":"Low (a tap)","Travel":"Keychain","Rating":"4.8 / 5"})
add("3m-gold-privacy-filter","security",
    "3M Gold Privacy Filter","3M",
    "3M Gold Privacy Filter laptop","4.6",
    "Blacks out your screen for the seat next to you","",
    "Check Price on Amazon",
    ["Gold micro-louvers — sharper cutoff than matte film",
     "Screen stays bright and clear head-on",
     "Slide-mount tabs; reversible matte side"],
    {"Best for":"Lounge / plane visual privacy","Protects against":"Shoulder-surfing",
     "Standard":"—","Daily friction":"Very low","Travel":"Fits in the sleeve","Rating":"4.6 / 5"})
add("mission-darkness-faraday","security",
    "Mission Darkness Dry Shield Faraday Laptop Bag","Mission Darkness",
    "Mission Darkness Dry Shield Faraday Bag laptop","4.7",
    "True RF isolation for hostile-jurisdiction travel","",
    "Check Price on Amazon",
    ["Blocks cellular, Wi-Fi, Bluetooth and GPS",
     "Waterproof roll-top; rugged exterior",
     "Stops remote wipe and tracking in transit"],
    {"Best for":"High-risk travel","Protects against":"Remote tracking / wipe",
     "Standard":"MIL-STD-188-125 tested","Daily friction":"Medium","Travel":"Purpose-built","Rating":"4.7 / 5"})
add("fellowes-99ci","security",
    "Fellowes Powershred 99Ci Micro-Cut Shredder","Fellowes",
    "Fellowes Powershred 99Ci micro cut shredder","4.7",
    "Turns M&A printouts into confetti, jam-free","",
    "Check Price on Amazon",
    ["100% jam-proof feed for mixed stacks",
     "Micro-cut particles — effectively unreconstructable",
     "Long runtime before cool-down"],
    {"Best for":"Physical document destruction","Protects against":"Dumpster recovery",
     "Standard":"P-4 micro-cut","Daily friction":"Low","Travel":"No (desk-side)","Rating":"4.7 / 5"})
add("kingston-ironkey-vp80","security",
    "Kingston IronKey Vault Privacy 80 Encrypted SSD","Kingston",
    "Kingston IronKey Vault Privacy 80 external SSD","4.5",
    "FIPS-grade encrypted drive with an on-device PIN","",
    "Check Price on Amazon",
    ["Hardware AES-256, on-screen PIN pad — no host software",
     "Brute-force lockout and BadUSB defense",
     "Carries sensitive files air-gapped from the laptop"],
    {"Best for":"Encrypted data at rest","Protects against":"Drive theft / loss",
     "Standard":"FIPS 197 / 140-3 L3","Daily friction":"Medium","Travel":"Pocket SSD","Rating":"4.5 / 5"},
    target=False)

CAT_ROWS = {"leather-edc":LROWS,"writing":WROWS,"audio":AROWS,"furniture":FROWS,"travel":TROWS,
            "video":VROWS,"beverage":BROWS,"wellness":NROWS,"decor":DROWS,"security":SROWS}

# ---------------------------------------------------------------------------
#  write data/offers.yaml
# ---------------------------------------------------------------------------
banner = (
"# =============================================================================\n"
"#  PRODUCT CATALOG  —  every entry is an Amazon product.\n"
"#\n"
"#  AFFILIATE ID:  do NOT put your tag here. Set [params].amazonTag in hugo.toml\n"
"#  ONCE and it flows into every link, button and image site-wide.\n"
"#\n"
"#  asin: \"\"   ->  links resolve to a tagged Amazon SEARCH for `search:` (works now)\n"
"#  asin: \"B0...\" ->  links resolve to that exact product page (better conversion)\n"
"#  Fill in asin values as you confirm them; nothing else needs to change.\n"
"# =============================================================================\n"
)
out = {}
for k, v in P.items():
    d = {"name": v["name"], "brand": v["brand"], "domain": "amazon.com",
         "asin": "", "search": v["search"], "rating": v["rating"],
         "tagline": v["tagline"], "cta": v["cta"], "image": v["image"],
         "bullets": v["bullets"], "compare": v["compare"]}
    if v["deal"]:
        d["deal"] = v["deal"]
    if v["target"]:
        d["reviewRef"] = f"/reviews/{k}"
    out[k] = d
with open(os.path.join(SITE, "data/offers.yaml"), "w") as f:
    f.write(banner + "\n")
    yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True, width=100)
print("offers.yaml:", len(out), "products")

# ---------------------------------------------------------------------------
#  product placeholder SVGs
# ---------------------------------------------------------------------------
def esc(s): return html.escape(s, quote=True)
def wrapname(name, n=22):
    lines = textwrap.wrap(name, n)[:3]
    return lines

for k, v in P.items():
    title, accent = CATS[v["category"]]
    lines = wrapname(v["name"])
    tspans = ""
    y0 = 300 - (len(lines)-1)*34
    for i, ln in enumerate(lines):
        tspans += f'<tspan x="60" y="{y0 + i*46}">{esc(ln)}</tspan>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" font-family="Plus Jakarta Sans, system-ui, sans-serif">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0f1b33"/><stop offset="1" stop-color="#0b1120"/></linearGradient></defs>
  <rect width="800" height="500" fill="url(#g)"/>
  <rect x="0" y="0" width="10" height="500" fill="{accent}"/>
  <text x="60" y="90" fill="{accent}" font-size="18" font-weight="700" letter-spacing="2">{esc(v["brand"].upper())}</text>
  <text fill="#f7f9fc" font-size="40" font-weight="800" letter-spacing="-1">{tspans}</text>
  <text x="60" y="418" fill="#93a1bd" font-size="19" font-weight="500">{esc(v["tagline"])}</text>
  <g transform="translate(600,360)" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round">
    <rect x="0" y="0" width="120" height="86" rx="10"/><path d="M20 86 L20 30 M50 86 L50 12 M80 86 L80 44 M110 86 L110 22"/>
  </g>
  <text x="60" y="462" fill="#5b6a86" font-size="15">C-Suit Necessities · {esc(title)}</text>
</svg>
'''
    with open(os.path.join(IMGDIR, f"{k}.svg"), "w") as f:
        f.write(svg)
print("images:", len(P), "svgs ->", IMGDIR)

# expose catalog for the content generator
import json
with open("/private/tmp/claude-501/-Users-logan-Documents-businesses-C-Suit-Reccuring-Affiliate/ad900b6b-0d6d-40ab-a72c-343857693d26/scratchpad/catalog.json","w") as f:
    json.dump({"cats":{k:list(v) for k,v in CATS.items()}, "rows":CAT_ROWS,
               "products":{k:{"name":v["name"],"category":v["category"],"target":v["target"]} for k,v in P.items()}}, f, indent=1)
print("wrote catalog.json")
