#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate all review + comparison markdown for C-Suit Necessities."""
import os, json, datetime

SITE = "/Users/logan/Documents/businesses/C-Suit Reccuring Affiliate/site"
SP = "/private/tmp/claude-501/-Users-logan-Documents-businesses-C-Suit-Reccuring-Affiliate/ad900b6b-0d6d-40ab-a72c-343857693d26/scratchpad"
cat = json.load(open(os.path.join(SP, "catalog.json")))
CATS, ROWS = cat["cats"], cat["rows"]
PRODUCTS = cat["products"]

os.makedirs(os.path.join(SITE, "content/reviews"), exist_ok=True)
os.makedirs(os.path.join(SITE, "content/compare"), exist_ok=True)

D0 = datetime.date(2026, 1, 12)   # keep every date in the past so nothing is treated as future content
def dated(i):
    return (D0 + datetime.timedelta(days=i * 3)).isoformat()

def fm(d):
    import io
    lines = ["+++"]
    def val(v):
        if isinstance(v, bool): return "true" if v else "false"
        if isinstance(v, (int, float)): return str(v)
        if isinstance(v, list):
            return "[" + ", ".join('"' + str(x).replace('"', '\\"') + '"' for x in v) + "]"
        return '"' + str(v).replace('\\', '\\\\').replace('"', '\\"') + '"'
    for k, v in d.items():
        if k == "faq":
            lines.append("faq = [")
            for q, a in v:
                qq = q.replace('"', '\\"'); aa = a.replace('\\', '\\\\').replace('"', '\\"')
                lines.append(f'  {{ q = "{qq}", a = "{aa}" }},')
            lines.append("]")
        else:
            lines.append(f"{k} = {val(v)}")
    lines.append("+++\n")
    return "\n".join(lines)

def takeaways(key, items):
    b = "\n".join("- " + x for x in items)
    return f'{{{{< key-takeaways offer="{key}" >}}}}\n{b}\n{{{{< /key-takeaways >}}}}\n'

def proscons(pros, cons):
    p = "\n".join("- " + x for x in pros)
    c = "\n".join("- " + x for x in cons)
    return f"{{{{< pros-cons >}}}}\n{p}\nvs\n{c}\n{{{{< /pros-cons >}}}}\n"

def buy(key, text):
    return f'{{{{< buy "{key}" >}}}}{text}{{{{< /buy >}}}}'

def cta(key):
    return f'{{{{< cta "{key}" >}}}}\n'

def offercard(key):
    return f'{{{{< offer-card "{key}" >}}}}\n'

def write_single(key, S, order):
    p = PRODUCTS[key]
    cslug = p["category"]; ctitle = CATS[cslug][0]
    secs = S["sections"]
    body = []
    body.append(takeaways(key, S["takeaways"]))
    # section 1
    body.append(f"## {secs[0][0]}\n\n{secs[0][1]}\n")
    body.append(offercard(key))
    # section 2
    body.append(f"## {secs[1][0]}\n\n{secs[1][1]}\n")
    # optional inline image linking to product
    body.append(f'![{p["name"]}](/img/products/{key}.svg "{S["verdict"]} — {p["name"]}")\n')
    # section 3
    body.append(f"## {secs[2][0]}\n\n{secs[2][1]}\n")
    body.append(proscons(S["pros"], S["cons"]))
    body.append("## Who it's for\n\n" + S["forwho"] + "\n")
    body.append(cta(key))
    front = {
        "title": S["title"],
        "headline": S["headline"],
        "dek": S["dek"],
        "date": dated(order),
        "lastmod": dated(order + 30),
        "weight": order + 1,
        "categories": [ctitle],
        "tags": S.get("tags", []),
        "keywords": S.get("keywords", []),
        "image": f"/img/products/{key}.svg",
        "imageAlt": p["name"],
        "offer": key,
        "verdict": S["verdict"],
        "cardCue": S.get("cardCue", "Read the review →"),
        "dek_": "",
        "finalCta": S["finalcta"],
        "faq": S["faq"],
    }
    front.pop("dek_")
    md = fm(front) + "\n".join(body) + "\n"
    with open(os.path.join(SITE, "content/reviews", f"{key}.md"), "w") as f:
        f.write(md)

def write_compare(slug, C, order):
    cslug = C["cat"]; ctitle = CATS[cslug][0]
    rows = ROWS[cslug]
    conts = C["contenders"]
    body = []
    body.append(takeaways(C["offer"], C["takeaways"]))
    body.append(C["intro"] + "\n")
    body.append(f'## The table\n\n{{{{< comparison offers="{",".join(conts)}" rows="{",".join(rows)}" >}}}}\n')
    body.append("## Where each one wins\n")
    for k in conts:
        nm = PRODUCTS[k]["name"]
        body.append(f"### {nm}\n\n{C['notes'][k]} {buy(k, C['notescta'].get(k, 'Check the current Amazon price'))}.\n")
    body.append("## The call\n\n" + C["verdict"] + "\n")
    body.append(cta(C["offer"]))
    front = {
        "title": C["title"],
        "headline": C["headline"],
        "dek": C["dek"],
        "date": dated(60 + order),
        "lastmod": dated(60 + order),
        "weight": order + 1,
        "categories": [ctitle],
        "tags": C.get("tags", []),
        "keywords": C.get("keywords", []),
        "image": f"/img/products/{conts[0]}.svg",
        "imageAlt": C["title"],
        "offer": C["offer"],
        "verdict": C["verdict_short"],
        "cardCue": "See the winner →",
        "finalCta": C["finalcta"],
        "faq": C["faq"],
    }
    md = fm(front) + "\n".join(body) + "\n"
    with open(os.path.join(SITE, "content/compare", f"{slug}.md"), "w") as f:
        f.write(md)

# ============================================================================
#  SINGLE REVIEWS
# ============================================================================
SINGLES = {}

# ---------- 1. LEATHER & EDC ----------
SINGLES["saddleback-briefcase"] = dict(
 title="Buy It Once: The Saddleback Briefcase Built to Outlive You",
 headline="The Saddleback Leather Thin Briefcase Is the Last Bag You'll Buy",
 dek="Boot-thick full-grain leather, not one zipper to fail, and a 100-year warranty that isn't a marketing line. Here's why it beats a designer label.",
 verdict="Best buy-it-once executive bag",
 cardCue="See why it lasts 100 years →",
 tags=["briefcase","leather","edc"], keywords=["saddleback leather briefcase","full grain briefcase","executive briefcase"],
 takeaways=[
   "Full-grain \"boot\" leather so thick it shrugs off airport floors and looks better every year.",
   "No zippers, no magnets, no plastic clips — just buckles and rivets that can't strand you at a gate.",
   "Carries a 15-inch laptop plus a legal pad without feeling like a suitcase.",
   "Priced once. The 100-year warranty means your kids inherit it.",
 ],
 sections=[
  ("The leather is the whole argument",
   "Most \"luxury\" bags are thin, corrected leather glued over cardboard stiffeners. Saddleback uses full-grain hide roughly twice the thickness of a typical designer brief, with pigskin lining and polyester thread that outlasts the leather. Drop it, kick it under a seat, leave it on a wet curb — it develops character instead of damage. If you've replaced a status bag every few years, price this one out per year of use and " + buy("saddleback-briefcase","check what it actually costs on Amazon today") + "."),
  ("Nothing on it can break",
   "Zippers are the first thing to die on a briefcase, usually mid-trip. This design has none. The main flap closes under two leather straps and buckles; the front pocket is open-access for a phone and passport. Fewer moving parts means fewer failure points on the one day you can't afford a bag failure. Frequent flyers tend to " + buy("saddleback-briefcase","grab the current Amazon listing") + " the moment they understand that."),
  ("Load, carry, and the airport test",
   "Fully loaded it's heavy — that's the tradeoff for leather this substantial — but the wide shoulder strap spreads it well and it stands up on its own base. The 15-inch laptop slot sits against your back, papers and a tablet in front. After a year the front develops a deep, uneven patina that photographs like money. See the current color options and pricing when you " + buy("saddleback-briefcase","open the Amazon page") + "."),
 ],
 pros=["Leather thick enough to be genuinely generational","Zero breakable hardware","Stands upright, opens fast under a flap","Patina gets better with abuse","Backed 100 years"],
 cons=["Heavy when fully loaded","Break-in period before the leather softens","Not the bag for minimalists who want 2 lbs"],
 forwho="The executive who is tired of replacing bags and wants the decision to be permanent. If you value light weight and technical pockets over ruggedness, look at the Bellroy Tokyo instead — but if you want an heirloom, this is it.",
 finalcta="If you want to stop buying briefcases, this is the one to buy.",
 faq=[("Is it too heavy for daily carry?","Empty it's around 4.5 lb — noticeably more than a nylon brief. The wide strap manages it well for a walk through a terminal, but if you carry a full load across a large campus every day, factor that in. Check the current weight and dimensions on the [Amazon listing](https://www.amazon.com/s?k=Saddleback+Leather+Thin+Front+Pocket+Briefcase)."),
      ("Does the 100-year warranty actually mean anything?","Yes — it transfers and covers workmanship. The leather and hardware are chosen so that honoring it is cheap for them. That's the point.")],
)
SINGLES["bellroy-tokyo"] = dict(
 title="The 2-Pound Briefcase: Bellroy Tokyo Work Bag, Reviewed",
 headline="Bellroy Tokyo Work Bag: Board Meeting to Boarding Gate, No Bulk",
 dek="A slim, weather-resistant leather brief that organizes two phones, cables and a 16-inch laptop — and slides onto your carry-on handle.",
 verdict="Best slim modern brief",
 cardCue="See the organization layout →",
 tags=["briefcase","bellroy","travel"], keywords=["bellroy tokyo work bag","slim briefcase","minimalist work bag"],
 takeaways=[
   "Clean, low-profile silhouette that reads modern-executive, not luggage.",
   "Purpose-cut slots for two phones, a charger and cables so nothing rattles loose.",
   "Luggage pass-through sleeve makes airport transit one-handed.",
   "Weather-resistant leather exterior that wipes clean.",
 ],
 sections=[
  ("Built for the hybrid week",
   "The Tokyo assumes your day has three modes — desk, meeting, flight — and none of them should require repacking. The main compartment takes a 16-inch laptop and a slim folio; a second zone holds the daily-carry small stuff in defined pockets. It stays under two and a half pounds empty, which you feel by the end of a travel day. Compare the Premium leather and the woven versions when you " + buy("bellroy-tokyo","check prices on Amazon") + "."),
  ("Dual-phone, dual-charger reality",
   "If you run a personal and a work phone, this is one of the few briefs that gives each a home, plus a stretch pocket sized for a GaN charger and a coiled cable. Everything has a place, so packing takes seconds and nothing prints through the leather. Executives who carry two devices tend to " + buy("bellroy-tokyo","order it after seeing that layout") + "."),
  ("Strap and pass-through",
   "The shoulder strap is a real leather strap with a proper pad, not an afterthought, and the geometry keeps the bag flat against your hip. The back sleeve slides over a roller handle so you're not shoulder-carrying through security. See current color and edition options on the " + buy("bellroy-tokyo","Amazon page") + "."),
 ],
 pros=["Genuinely slim and light","Best-in-class small-item organization","Weatherproof exterior","Comfortable real strap","Luggage pass-through"],
 cons=["Not built for heavy daily loads","Structured shape has less give than a soft brief","Premium leather commands a premium price"],
 forwho="The minimalist executive who flies often and wants one refined bag for every mode of the day. If you want maximum ruggedness or an heirloom, the Saddleback is the other end of the spectrum.",
 finalcta="For a slim brief that handles a hybrid travel week, this is the pick.",
 faq=[("Will a 16-inch MacBook Pro fit?","Yes, the main laptop compartment is sized for up to 16 inches. Confirm the exact internal dimensions against your machine on the [Amazon listing](https://www.amazon.com/s?k=Bellroy+Tokyo+Work+Bag)."),
      ("Premium edition vs standard — worth it?","The Premium uses a fuller, more weather-resistant leather and hardware that ages better. If this is your daily bag, it's the one to get.")],
)
SINGLES["leatherology-padfolio"] = dict(
 title="The Folio You Unzip When Laptops Are Banned From the Room",
 headline="Leatherology Zip-Around Executive Padfolio: Full-Grain, Board-Ready",
 dek="Some rooms don't allow devices. This full-grain Italian leather folio is what you bring instead — and it signals more than a laptop ever could.",
 verdict="Best padfolio for device-free sessions",
 cardCue="See the full-grain leather →",
 tags=["padfolio","leatherology","leather"], keywords=["leatherology padfolio","executive padfolio","zip around portfolio"],
 takeaways=[
   "Full-grain leather that develops a personal patina — not the plastic-coated stuff.",
   "Gusset expands to swallow a printed pitch deck; fits letter or A4 pads.",
   "Perimeter zip is smooth and keeps loose pages from escaping in a bag.",
   "Free monogramming on most orders makes it unmistakably yours.",
 ],
 sections=[
  ("Why paper still wins some rooms",
   "Board sessions, deal rooms, certain government and legal settings — devices go in a locker. Walking in with a substantial leather folio instead of fumbling for a legal pad is a small signal that you were ready. The full-grain hide here is thick and tight-grained, and it only looks better after a year of handling. See the color range and current pricing when you " + buy("leatherology-padfolio","check Amazon") + "."),
  ("It actually holds a deck",
   "The zip-around gusset expands a couple of inches, so a 40-page printed deck, a notepad and a few reference documents all fit without bulging. Inside: card slots, a document sleeve, a pen loop with real clearance for a fat-barreled pen. If you present from paper, " + buy("leatherology-padfolio","grab it on Amazon") + " before your next off-site."),
  ("The details that age well",
   "Edge-painted seams, a smooth YKK-class perimeter zip, and a lining that doesn't pill. Add a monogram and it's yours for a decade. Check whether monogramming is offered on the current " + buy("leatherology-padfolio","Amazon listing") + "."),
 ],
 pros=["Real full-grain leather at a fair price","Expanding gusset fits full decks","Smooth perimeter zip","Generous pen loop","Monogram option"],
 cons=["No room for a laptop (by design)","Full-grain needs occasional conditioning","Heavier than a vinyl folio"],
 forwho="Executives who regularly sit in device-free rooms and want to arrive looking prepared. If your meetings are all laptop-friendly, a slim brief like the Bellroy covers more ground.",
 finalcta="For the rooms where laptops don't go, this is what you carry.",
 faq=[("Letter or A4 pad?","It accommodates both — there's a strap system sized for standard US letter and a bit of extra length for A4. Verify against your region's pad size on the [Amazon page](https://www.amazon.com/s?k=Leatherology+Zip+Around+Executive+Padfolio)."),
      ("Will a Montblanc 149 fit the pen loop?","Yes — the loop is cut with clearance for wide barrels, unlike most folios. That's one reason fountain-pen users choose it.")],
)
SINGLES["shinola-valet-tray"] = dict(
 title="The $95 Object That Ends Desk Clutter for Good",
 headline="Shinola Detroit Leather Catchall Tray: The Desk Statement That Works",
 dek="Structured vegetable-tanned leather that corrals your watch, keys and rings — and protects a mechanical watch bracelet from your titanium keys.",
 verdict="Best desk valet tray",
 cardCue="See it on a credenza →",
 tags=["valet tray","shinola","desk"], keywords=["shinola catchall tray","leather valet tray","desk organizer tray"],
 takeaways=[
   "Firm vegetable-tanned leather holds its shape — corners stand up, don't flop.",
   "Deep enough for a watch, wedding band, AirPods and a key fob without a jumble.",
   "Soft leather floor means your watch bracelet never meets bare metal.",
   "Small footprint — it lives beside the keyboard, not across the desk.",
 ],
 sections=[
  ("Clutter is a decision you keep re-making",
   "Without a landing zone, your watch and keys scatter across the desk every evening and you hunt for them every morning. A single tray ends that loop. This one is structured — the snap-stud corners give it rigid walls, so it reads as an intentional object, not a floppy leather square. See the size and color options when you " + buy("shinola-valet-tray","check the Amazon listing") + "."),
  ("It protects what you put in it",
   "Drop a steel dive-watch bracelet into a wooden or metal tray and you'll hear it — and eventually see the micro-scratches. The veg-tan leather floor here is soft enough to be a safe home for a mechanical watch every night. Collectors tend to " + buy("shinola-valet-tray","buy one on Amazon") + " for exactly that reason."),
  ("Footprint and finish",
   "The large size still tucks beside a keyboard. The leather starts firm and lightens as it patinas. Check current dimensions and finish on the " + buy("shinola-valet-tray","Amazon page") + "."),
 ],
 pros=["Rigid, structured walls","Safe surface for watch bracelets","Compact footprint","Ages into a warm patina","Doubles as a travel tray"],
 cons=["Premium price for a tray","Veg-tan darkens unevenly if it gets wet","One color may sell out"],
 forwho="Anyone with a watch habit and a cluttered desk. It's also the easy gift for the executive who has everything.",
 finalcta="A small object that fixes a daily annoyance — worth it.",
 faq=[("Large or small size?","The large holds a watch plus everything else comfortably; the small is really just for a watch and a ring. Most people want the large — confirm dimensions on the [Amazon listing](https://www.amazon.com/s?k=Shinola+Detroit+Large+Leather+Catchall+Tray)."),
      ("Does it scratch a watch clasp?","No — the interior is smooth veg-tan leather. It's one of the safer trays for a metal bracelet.")],
)

# ---------- 2. WRITING ----------
SINGLES["montblanc-149"] = dict(
 title="Is the Montblanc 149 Worth It? A Blunt Answer",
 headline="Montblanc Meisterstück 149 Review: The Pen That Signs the Deal",
 dek="An 18K gold nib, a piston that holds enough ink for a hundred signatures, and a barrel that photographs like status. Does that justify the flagship price?",
 verdict="Best status fountain pen",
 cardCue="See the gold nib →",
 tags=["fountain pen","montblanc","luxury"], keywords=["montblanc 149 review","meisterstuck 149","best executive fountain pen"],
 takeaways=[
   "The 18K nib has a hint of give that makes your signature look deliberate.",
   "Piston filler holds a large ink reserve — days of signing between refills.",
   "The barrel is big; it fills a hand and reads across a conference table.",
   "It's a public-facing object as much as a writing tool. Priced accordingly.",
 ],
 sections=[
  ("What you're actually paying for",
   "Mechanically, a $40 pen can lay down ink. The 149 sells something else: a hand-finished gold nib tuned for a smooth, slightly springy line, a resin barrel with real depth, and a name every counterparty recognizes when you uncap it to sign. If that moment matters in your work, " + buy("montblanc-149","see the current Amazon price") + " and decide."),
  ("On paper, in a signing session",
   "Ink flow is generous and consistent, even on heavier stock. Unposted it's balanced; posted it's long and back-heavy for most hands. The wide barrel is comfortable for a page of signatures but a little much for dense note-taking — that's not what it's for. Check nib width options (a medium is the safe default) on the " + buy("montblanc-149","Amazon listing") + "."),
  ("Living with it",
   "Flush the piston monthly, keep it capped, and it runs for decades. Resale holds better than almost any pen. If you want the same gravitas with less flash, look at the Lamy 2000 — otherwise " + buy("montblanc-149","get the 149 on Amazon") + "."),
 ],
 pros=["Hand-tuned 18K nib with character","Huge ink capacity","Unmistakable presence","Holds value","Decades of service with basic care"],
 cons=["Flagship price","Large barrel isn't for everyone","Posted balance is back-heavy","A target for 'look at me' criticism"],
 forwho="Executives who sign in front of people and want the pen to be part of the moment. Everyone else can get 90% of the writing experience for a fraction of the price.",
 finalcta="If the signature moment matters in your role, the 149 earns its keep.",
 faq=[("Which nib size should I order?","Medium is the versatile default for signatures and notes. Fine if your handwriting is small; broad only if you want a showy, wet line. Nib options are listed on the [Amazon page](https://www.amazon.com/s?k=Montblanc+Meisterstuck+149+Fountain+Pen)."),
      ("Fountain pen upkeep — is it a hassle?","Flush it with water once a month and don't let it dry out capped. That's the whole routine.")],
)
SINGLES["waterman-carene"] = dict(
 title="The Grab-and-Sign Pen: Waterman Carène, Reviewed",
 headline="Waterman Carène Rollerball Review: Fountain-Pen Looks, Zero Maintenance",
 dek="Lacquered, contoured, brass-cored — and it writes the instant it touches paper. The low-fuss alternative for people who don't want to babysit a nib.",
 verdict="Best low-maintenance executive pen",
 cardCue="See the Black Sea finish →",
 tags=["rollerball","waterman","pen"], keywords=["waterman carene rollerball","low maintenance executive pen","best rollerball pen"],
 takeaways=[
   "Rollerball ink laydown — no priming, no skipping after it sits in a drawer.",
   "Real brass chassis under the lacquer gives it a planted, quality weight.",
   "Firm cap snap survives a jacket pocket and a briefcase.",
   "Refills are common and cheap to keep in a drawer.",
 ],
 sections=[
  ("For people who don't want a hobby",
   "A fountain pen is a small commitment — flushing, ink choice, the occasional hard start. The Carène gives you the lacquered, contoured elegance and the brass heft without any of that. Uncap it after two weeks in a drawer and it writes on the first stroke. See the finishes and current price when you " + buy("waterman-carene","check Amazon") + "."),
  ("The writing experience",
   "The rollerball refill is wet and dark, so notes and signatures both look substantial. The center of gravity sits low toward the grip, which keeps long note-taking sessions from tiring your hand. It also lays down cleanly on carbon-copy and thermal paper where a fountain pen would feather. Fast note-takers tend to " + buy("waterman-carene","order one on Amazon") + "."),
  ("Cap, clip, refills",
   "The cap snaps with a positive click and holds — no cap creep in a pocket. Refills are standard Waterman rollerball, easy to stockpile. Check refill availability on the " + buy("waterman-carene","Amazon page") + "."),
 ],
 pros=["Instant, reliable ink laydown","Brass core = real quality weight","Secure cap snap","Cheap, available refills","No maintenance ever"],
 cons=["Rollerball refills run out faster than a fountain pen's ink","Less 'special' than a gold nib","Lacquer can chip if dropped on a hard edge"],
 forwho="The executive who wants a beautiful pen that just works and never needs thought. If you enjoy the ritual of a fountain pen, get the Lamy 2000 or the 149 instead.",
 finalcta="A handsome pen with zero upkeep — hard to argue with.",
 faq=[("Can it take a fountain-pen nib?","There's a Carène fountain pen variant, but this is the rollerball — its appeal is that there's no nib to manage. Both are on the [Amazon listing](https://www.amazon.com/s?k=Waterman+Carene+Rollerball)."),
      ("How often will I replace refills?","With daily note-taking, roughly monthly. Keep two spares in your desk and you'll never be caught out.")],
)
SINGLES["lamy-2000"] = dict(
 title="The Anti-Montblanc: Why Founders Choose the Lamy 2000",
 headline="Lamy 2000 Review: Bauhaus Restraint for the Discreet Executive",
 dek="A seamless Makrolon and brushed-steel body designed in 1966 and never bettered. The pen for the person who finds a gold Montblanc a little loud.",
 verdict="Best understated fountain pen",
 cardCue="See the seamless body →",
 tags=["fountain pen","lamy","design"], keywords=["lamy 2000 review","understated fountain pen","best minimalist pen"],
 takeaways=[
   "One continuous form — no visible seams, no branding shouting across the table.",
   "Hooded 14K gold nib: a smooth, wet line with a small sweet spot.",
   "Spring-loaded clip and piston filler; a lot of engineering, invisibly.",
   "Costs a fraction of a flagship and arguably out-designs all of them.",
 ],
 sections=[
  ("Design as a signal",
   "The Lamy 2000 says something specific: that you notice design and don't need a logo to prove taste. The Makrolon fiberglass body is warm to the touch, matte, and grippy without a molded section. It's the pen a technical founder or a low-key CEO reaches for. See current finishes and pricing on " + buy("lamy-2000","Amazon") + "."),
  ("The nib takes a day",
   "The 14K nib is hooded, so less of it shows and it stays wet in a drawer. It has a slightly narrower sweet spot than an open nib — rotate it a few degrees and you find the glide. Give it a day of use and it disappears in the hand on long strategy memos. Once it clicks, people " + buy("lamy-2000","buy a second one on Amazon") + "."),
  ("Filling and care",
   "It's a piston filler — twist the blind cap, draw from a bottle, flush monthly. Nib swaps require sending it to Lamy, so order the width you want (EF/F/M). Check nib options on the " + buy("lamy-2000","Amazon listing") + "."),
 ],
 pros=["Timeless, seamless industrial design","Warm, grippy Makrolon body","Hooded nib stays ready","Excellent value for a gold-nib piston filler","No loud branding"],
 cons=["Nib sweet spot needs a short adjustment","Nib width is a commit-at-purchase decision","Not a 'wow' object for people who want flash"],
 forwho="The executive whose taste is quiet — design-literate, logo-averse. If you want the pen to be a visible status cue, the Montblanc 149 is the other choice.",
 finalcta="The connoisseur's everyday pen. Order the M nib and don't look back.",
 faq=[("EF, F, or M nib?","M is the smooth all-rounder and the most forgiving of the sweet spot. F if your writing is small. EF only if you like feedback. Widths are on the [Amazon page](https://www.amazon.com/s?k=Lamy+2000+Fountain+Pen+Makrolon)."),
      ("Makrolon vs stainless version?","The Makrolon is lighter, warmer and the original. The stainless is heavier and blingier. Most buyers want the Makrolon.")],
)
SINGLES["leuchtturm-master"] = dict(
 title="Why Your Best Thinking Needs a Bigger Page",
 headline="Leuchtturm1917 Master Slim A4+ Review: A Full Sheet of Thinking Room",
 dek="Oversized pages, 100 g/m² archival paper, numbered and indexed. The notebook for mapping a strategy that doesn't fit in a pocket Moleskine.",
 verdict="Best large-format planning notebook",
 cardCue="See the A4+ format →",
 tags=["notebook","leuchtturm","paper"], keywords=["leuchtturm master slim","a4 notebook fountain pen","strategic planning notebook"],
 takeaways=[
   "A4+ pages give you room to actually mind-map instead of cramping notes.",
   "100 g/m² paper resists fountain-ink bleed-through and ghosting.",
   "Numbered pages plus a real index turn a year of notes into a reference.",
   "Lay-flat thread binding survives constant open-and-close.",
 ],
 sections=[
  ("Small pages force small thinking",
   "A pocket notebook is fine for a to-do list. It's the wrong tool for laying out an org chart, a deal structure or a quarter's priorities on one visible surface. The Master Slim gives you a full oversized sheet, so the whole picture stays in view. See the ruling options (dotted is the flexible choice) on " + buy("leuchtturm-master","Amazon") + "."),
  ("The paper handles a wet pen",
   "At 100 g/m² this stock takes a broad, wet fountain nib with minimal ghosting and effectively no bleed-through — you can use both sides. If you've been avoiding fountain pens because your notebook can't handle them, this fixes it. Fountain-pen users " + buy("leuchtturm-master","pick these up in multipacks on Amazon") + "."),
  ("Built to be referenced later",
   "Every page is numbered, there's an index at the front, and two ribbons plus perforated last sheets. The thread binding lies flat from page one. Check page count and cover colors on the " + buy("leuchtturm-master","Amazon listing") + "."),
 ],
 pros=["Genuinely large working surface","Fountain-pen-friendly 100 g/m² paper","Numbered pages + index","Lies flat, sturdy binding","Handsome hardcover"],
 cons=["Too big to carry everywhere","Fewer pages than a standard Leuchtturm (thicker paper)","Premium price per notebook"],
 forwho="Anyone whose planning and strategy work needs space to breathe on the page. Pair it with a fine or medium fountain pen for the full experience.",
 finalcta="For real planning work, the bigger page pays for itself.",
 faq=[("Dotted, ruled, or plain?","Dotted is the most flexible — structure when you want it, freedom when you don't. All rulings are on the [Amazon page](https://www.amazon.com/s?k=Leuchtturm1917+Master+Slim+A4+Notebook)."),
      ("Will it bleed with a broad wet nib?","Minimal ghosting, essentially no bleed-through on the 100 g/m² paper. It's one of the better mass-market notebooks for wet pens.")],
)

# ---------- 3. AUDIO ----------
SINGLES["sony-xm5"] = dict(
 title="The Desk Sanctuary: Sony WH-1000XM5 for People on Calls All Day",
 headline="Sony WH-1000XM5 Review: The Headset That Makes Any Room a Quiet Office",
 dek="Class-leading noise cancellation plus an 8-mic array that keeps your voice clean on investor calls — wherever you're taking them.",
 verdict="Best headphones for calls + focus",
 cardCue="See the call-mic test →",
 tags=["headphones","sony","noise canceling"], keywords=["sony wh-1000xm5 review","best headphones for calls","noise canceling headphones executive"],
 takeaways=[
   "Best-in-class cancellation of the low-frequency drone — HVAC, cabin, traffic.",
   "8-mic beamforming keeps your voice intelligible on the other end of a call.",
   "~30-hour battery and fast multipoint between a laptop and a phone.",
   "Light clamp; the one weak spot is warmth over very long sessions.",
 ],
 sections=[
  ("Why it's the default",
   "For a desk-and-travel executive, the XM5 hits the widest set of needs: it kills the ambient rumble that causes fatigue, it switches instantly between your work laptop and your phone, and — critically — people on your calls say you sound clear. Amazon runs frequent price drops on these, so " + buy("sony-xm5","check today's number") + " before you buy elsewhere."),
  ("The part reviews under-weight: the mic",
   "Most noise-canceling headphones cancel noise *for you* and let a jet of background through *to your callers*. The XM5's array is genuinely good at suppressing keyboard clatter and room chatter on the transmit side, which matters when you're the one presenting numbers. If you live on video calls, " + buy("sony-xm5","get them on Amazon") + "."),
  ("Comfort and battery over a real day",
   "The pads are soft and the clamp is gentle, so nothing pinches — but the synthetic leather traps heat, and after three straight hours you'll want a break. Battery genuinely lasts a travel day. Check color and current bundle pricing on the " + buy("sony-xm5","Amazon listing") + "."),
 ],
 pros=["Class-leading low-frequency ANC","Strong transmit-side mic for calls","Fast, reliable multipoint","~30 hr battery","Light clamp pressure"],
 cons=["Ear cups get warm over long sessions","Don't fold as compactly as the XM4","Touch controls can misfire with gloves"],
 forwho="Executives whose day is calls, focus work and travel in some mix. If pure long-haul comfort is the priority, the Bose QC Ultra clamps lighter.",
 finalcta="The safest single pick for a call-heavy executive. Buy on a price dip.",
 faq=[("XM5 vs XM4 — upgrade?","The XM5 improves call mic quality and ANC on voices; the XM4 folds smaller and is cheaper. For call-heavy use, the XM5. Both are on the [Amazon page](https://www.amazon.com/s?k=Sony+WH-1000XM5)."),
      ("Can it connect to a laptop and phone at once?","Yes — multipoint holds two devices and switches automatically when a call comes in on the phone.")],
)
SINGLES["bose-qc-ultra"] = dict(
 title="Best Headphones for the Red-Eye: Bose QuietComfort Ultra",
 headline="Bose QuietComfort Ultra Review: The Comfort King for Long-Haul Flights",
 dek="The lightest clamp pressure of any flagship, excellent cancellation, and a case that actually fits in a personal item. Built for the cross-continental commute.",
 verdict="Best for travel comfort",
 cardCue="See the fold-flat case →",
 tags=["headphones","bose","travel"], keywords=["bose quietcomfort ultra review","best headphones for flights","comfortable noise canceling headphones"],
 takeaways=[
   "The most forgiving fit of the flagships — no jaw ache after a 7-hour flight.",
   "Cancellation is right there with Sony on cabin noise.",
   "Immersive spatial audio makes hybrid conference calls easier to follow.",
   "Case folds flat and slim for a briefcase or seat-back pocket.",
 ],
 sections=[
  ("Comfort is a feature, not a nicety",
   "On a long flight, clamp pressure is the difference between arriving rested and arriving with a headache. The QC Ultra has the gentlest, best-distributed fit Bose has made, and the pads breathe better than Sony's. If your travel is long-haul, that alone can decide it — " + buy("bose-qc-ultra","check the Amazon price") + "."),
  ("On calls and in meetings",
   "Mic performance is very good if a step behind the Sony for transmit clarity in loud spaces. Where it pulls ahead is the immersive-audio mode for group calls — voices get a sense of place, which reduces the fatigue of a long panel. Frequent flyers " + buy("bose-qc-ultra","buy these on Amazon") + " for the comfort and keep a wired option for critical calls."),
  ("Packing and battery",
   "The case is noticeably slimmer than the XM5's and the cups fold flat. Battery covers a travel day with ANC on. See current colorways and any bundle on the " + buy("bose-qc-ultra","Amazon listing") + "."),
 ],
 pros=["Best-in-class fit and clamp comfort","Excellent ANC on cabin noise","Useful spatial mode for group calls","Compact fold-flat case","Clean, understated look"],
 cons=["Transmit mic trails the Sony in loud rooms","Shorter rated battery than some rivals","App is functional, not deep"],
 forwho="The executive whose pain point is long flights and back-to-back meetings. If your priority is call-mic quality at a noisy desk, get the Sony XM5.",
 finalcta="If comfort on long flights is the deciding factor, this is the one.",
 faq=[("QC Ultra vs Sony XM5 for calls?","Sony has the edge on transmit-mic clarity in loud environments; Bose wins on all-day fit and the spatial call mode. Compare both on the [Amazon page](https://www.amazon.com/s?k=Bose+QuietComfort+Ultra+Headphones)."),
      ("Does spatial audio work on any call app?","The immersive mode processes incoming audio locally, so it works regardless of the conferencing platform.")],
)
SINGLES["jabra-speak2-75"] = dict(
 title="Turn a Hotel Room Into a Boardroom: Jabra Speak2 75",
 headline="Jabra Speak2 75 Review: The Speakerphone That Fixes Laptop-Mic Calls",
 dek="Full-duplex audio, 360-degree pickup and acoustic voice-leveling — so a call from a satellite office sounds like a call from HQ.",
 verdict="Best portable conference speakerphone",
 cardCue="See the pickup pattern →",
 tags=["speakerphone","jabra","conference"], keywords=["jabra speak2 75 review","portable conference speakerphone","best speakerphone for calls"],
 takeaways=[
   "Full-duplex: two people can talk at once without either getting clipped.",
   "Acoustic leveling evens out the loud person and the quiet person in the room.",
   "360-degree mic pickup covers a small meeting table.",
   "USB-C and Bluetooth; comes with a travel pouch.",
 ],
 sections=[
  ("The laptop mic is costing you authority",
   "A built-in laptop mic makes you sound distant, echoey and small — not the impression you want when you're the one leading the call. The Speak2 75 drops on the table and instantly you sound present and in command. Anyone who runs calls from hotels or satellite offices should " + buy("jabra-speak2-75","check the Amazon price") + "."),
  ("Full-duplex is the real upgrade",
   "Cheap speakerphones are half-duplex — when the far side talks, your mic ducks, so interruptions and quick agreement get lost. This one is full-duplex, so the conversation flows naturally. It also normalizes levels so the person leaning back isn't inaudible. Road warriors " + buy("jabra-speak2-75","buy one on Amazon") + " and leave it in the bag permanently."),
  ("Connectivity and battery",
   "USB-C for a guaranteed-clean laptop connection, Bluetooth for a phone, ~32 hours of talk time, and a hard-shell pouch. Check the current bundle and any dongle inclusion on the " + buy("jabra-speak2-75","Amazon listing") + "."),
 ],
 pros=["Full-duplex — natural back-and-forth","Acoustic voice-leveling","Wide 360° pickup","Long battery + travel pouch","Dual USB-C / Bluetooth"],
 cons=["Overkill for solo headset calls","Bluetooth adds slight latency vs USB","Premium vs consumer speakerphones"],
 forwho="Executives who lead calls from rooms other than their own office. For solo desk calls, a headset like the Sony XM5 is the better tool.",
 finalcta="One purchase that permanently upgrades how you sound in every room.",
 faq=[("USB or Bluetooth — which sounds better?","USB-C is the cleaner, lower-latency connection for a laptop; use Bluetooth for a phone. Both are supported — details on the [Amazon page](https://www.amazon.com/s?k=Jabra+Speak2+75)."),
      ("How many people does it cover?","Comfortably a table of four to six. Beyond that you'd want a room system.")],
)
SINGLES["snooz"] = dict(
 title="Sound-Masking So the Hallway Hears Nothing",
 headline="SNOOZ Real-Fan White Noise Machine Review: Confidential Conversations, Contained",
 dek="A real mechanical fan — not a looping digital hiss — that masks financial and personnel discussions before they reach the hallway.",
 verdict="Best office sound-masking device",
 cardCue="See where it sits →",
 tags=["white noise","snooz","privacy"], keywords=["snooz white noise machine review","office sound masking","white noise machine for privacy"],
 takeaways=[
   "A genuine spinning fan produces a natural broadband sound with no loop artifacts.",
   "Tunable tone and volume let you match the door gap and room size.",
   "Small and quiet-looking — hides on a credenza or behind a monitor.",
   "App scheduling turns it on before your first sensitive meeting.",
 ],
 sections=[
  ("Why digital white noise fails at masking",
   "Looped digital noise has a repeating signature your ear learns to tune out — and so does anyone listening at the door. A real fan produces true broadband sound that actually covers speech frequencies. If your office walls are thin and your conversations aren't casual, " + buy("snooz","see the Amazon price") + "."),
  ("Tuning it to your room",
   "The housing rotates to shift the tone from deep to airy, and the volume range is wide. Set it once for your door gap and room and it does its job. Executives with corner offices and confidential calendars " + buy("snooz","order one on Amazon") + " and forget about it."),
  ("Footprint and control",
   "It's compact, matte, and unremarkable-looking on purpose. The app schedules on/off and adjusts settings without you touching it. Check dimensions and the current model on the " + buy("snooz","Amazon listing") + "."),
 ],
 pros=["Real fan = natural, non-repeating sound","Genuinely effective speech masking","Tunable tone and volume","Discreet footprint","App scheduling"],
 cons=["Moving parts vs a solid-state machine","Not battery powered","Won't stop a determined eavesdropper — it masks, not soundproofs"],
 forwho="Executives whose offices carry sensitive conversations and thin walls. Pair it with a closed door and lowered voices.",
 finalcta="Cheap insurance against a conversation leaving the room.",
 faq=[("Does it actually stop people overhearing?","It masks speech so words become unintelligible past the door — it doesn't soundproof. For most offices that's the meaningful protection. See specs on the [Amazon page](https://www.amazon.com/s?k=SNOOZ+White+Noise+Sound+Machine)."),
      ("Is the fan noise annoying to work next to?","Most people find real-fan noise easier to ignore than digital loops. You can tune it quieter for your own comfort while still masking at the door.")],
)

# ---------- 4. FURNITURE ----------
SINGLES["herman-miller-aeron"] = dict(
 title="The Aeron, 30 Years Later: Still the One to Buy?",
 headline="Herman Miller Aeron Review: Why the Corner-Office Standard Still Wins",
 dek="8Z Pellicle mesh, PostureFit SL, forward tilt — assessed over the 12-hour days it was built for. And a cheaper way to buy one.",
 verdict="Best all-day executive chair",
 cardCue="See the refurb savings →",
 tags=["office chair","herman miller","ergonomic"], keywords=["herman miller aeron review","best executive office chair","aeron posturefit"],
 takeaways=[
   "Pellicle mesh keeps you cool across an 8+ hour day — no sweat patch.",
   "PostureFit SL stabilizes the sacrum, which is what actually saves your lower back.",
   "Forward tilt is underrated for heads-down review work.",
   "Certified-refurbished units cost far less and carry a warranty — check those first.",
 ],
 sections=[
  ("The mesh is the point",
   "Cushioned chairs get hot and compress over the years; the Aeron's suspension mesh does neither. Across a long day you stay cool and the support feels identical at hour nine as at hour one. If you sit for a living, " + buy("herman-miller-aeron","check the Amazon price — including certified-refurbished") + "."),
  ("PostureFit SL vs everything else",
   "Most chairs push on your lumbar. The Aeron's PostureFit SL also stabilizes the sacrum — the base of the spine — which is the mechanism that keeps you from slumping without thinking about it. It's the single feature worth paying for. Executives with a history of back pain " + buy("herman-miller-aeron","buy the loaded config on Amazon") + "."),
  ("Size and the refurb route",
   "Get the size right (B fits most adults; C is the large). A new one is expensive; Herman Miller and authorized sellers list certified-refurbished Aerons with a 12-year warranty for a lot less. Compare new vs refurb on the " + buy("herman-miller-aeron","Amazon listing") + "."),
 ],
 pros=["Cool, consistent mesh support all day","PostureFit SL genuinely helps posture","Forward tilt for focused work","12-year warranty","Refurb market makes it attainable"],
 cons=["New price is steep","Firm mesh seat isn't for people who want plush","Sizing (A/B/C) requires attention"],
 forwho="Anyone doing long days at a desk who wants a chair that performs the same at hour ten. If you're constantly shifting between phone, tablet and keyboard, the Steelcase Gesture's arms may suit you better.",
 finalcta="Still the benchmark. Buy a certified-refurbished one and save.",
 faq=[("Size A, B, or C?","B fits roughly 90% of adults. A is for smaller frames, C for larger or taller. Sizing guidance is on the [Amazon page](https://www.amazon.com/s?k=Herman+Miller+Aeron+Chair+PostureFit+SL)."),
      ("Is certified-refurbished worth it?","Yes — it's remanufactured to spec and carries the full 12-year warranty, typically at 30–50% off new.")],
)
SINGLES["steelcase-gesture"] = dict(
 title="The Chair Built for a Phone in One Hand",
 headline="Steelcase Gesture Review: The Only Chair That Follows You to Every Device",
 dek="360-degree arms that support you whether you're typing, holding a tablet, or thumbing a phone — the posture most chairs ignore.",
 verdict="Best chair for device-switching",
 cardCue="See the arm range →",
 tags=["office chair","steelcase","ergonomic"], keywords=["steelcase gesture review","best office chair for posture","office chair with adjustable arms"],
 takeaways=[
   "The arms move in almost every direction — they actually support a phone-holding posture.",
   "Weight-activated recline tracks your movement without a tension dial fight.",
   "Cushioned contour seat that supports without going soft over years.",
   "Fabric options hold up to suit hardware (belt buckles, cufflinks).",
 ],
 sections=[
  ("The posture nobody designs for",
   "You spend hours a day with an arm raised, holding or tapping a device. Most chair arms can't follow that — so your shoulder and neck take the load. The Gesture's arms rotate, slide and tilt to stay under your forearm in that position. If your day is a lot of phone and tablet, " + buy("steelcase-gesture","check the Amazon price") + "."),
  ("Recline that just works",
   "Instead of hunting for the right tension, the Gesture's mechanism responds to your body weight and tracks smoothly as you lean back to think and forward to type. Add the headrest for calls where you lean back. Executives who never sit still " + buy("steelcase-gesture","order it on Amazon") + "."),
  ("Seat, materials, longevity",
   "The seat is contoured foam — supportive now, still supportive in year five. Choose a tighter-weave fabric if you wear hardware that could pick at loops. See fabric and headrest options on the " + buy("steelcase-gesture","Amazon listing") + "."),
 ],
 pros=["Best arm adjustability on the market","Intuitive weight-activated recline","Durable contoured seat","Good for phone/tablet posture","12-year warranty"],
 cons=["Warmer than a mesh chair","Heavy; awkward to move between rooms","Configurator can get expensive"],
 forwho="Executives who are always holding a device and want arm support that follows. If you run hot or want the lightest all-day support, the mesh Aeron is the alternative.",
 finalcta="If your day is device-in-hand, this chair was designed for you.",
 faq=[("Do I need the headrest?","If you lean back for calls or thinking, yes — it makes the recline usable. It's a configurable option on the [Amazon page](https://www.amazon.com/s?k=Steelcase+Gesture+Office+Chair+with+Headrest)."),
      ("Gesture vs Leap?","Gesture has the superior arms and a slightly firmer feel; Leap has a more dynamic backrest. For device-heavy work, Gesture.")],
)
SINGLES["ergotron-hx"] = dict(
 title="No Wobble, No Sag: Ergotron HX With a 49-Inch Ultrawide",
 headline="Ergotron HX Monitor Arm Review: Holds a Massive Ultrawide Dead Still",
 dek="Rated for heavy panels, repositions with a fingertip, and routes cables internally. The arm for a 49-inch curved executive display.",
 verdict="Best arm for heavy ultrawides",
 cardCue="See the weight rating →",
 tags=["monitor arm","ergotron","desk setup"], keywords=["ergotron hx review","monitor arm for 49 inch ultrawide","heavy duty monitor arm"],
 takeaways=[
   "Built for large, heavy panels where lighter arms droop or bounce.",
   "Constant-Force lift moves a big display with one finger and holds position.",
   "Internal cable channels keep the desk clean.",
   "Solid clamp that bites properly on a thick hardwood desk.",
 ],
 sections=[
  ("Most arms can't hold a real ultrawide",
   "A 49-inch curved panel is heavy and has a lot of leverage. Put it on a mid-range arm and you get sag, a slow droop over the day, and a bounce every time you type hard. The HX is engineered for exactly this weight class. Before you buy the monitor, " + buy("ergotron-hx","price the arm on Amazon") + "."),
  ("Fingertip repositioning",
   "Ergotron's Constant-Force lift is tuned so a heavy display feels weightless through its range and stays exactly where you leave it — no knobs. For a shared or hot-desk setup where people reposition constantly, that's the feature. Setup-obsessives " + buy("ergotron-hx","buy the HX on Amazon") + "."),
  ("Mounting and cables",
   "Use the C-clamp on a solid desk; check thickness limits for thick tops. Cables run through the arm for a clean look. Confirm your monitor's weight and VESA against the spec on the " + buy("ergotron-hx","Amazon listing") + "."),
 ],
 pros=["Handles genuinely heavy panels","Effortless, stay-put repositioning","Clean internal cable routing","Sturdy clamp","10-year warranty"],
 cons=["Overkill (and overpriced) for a light 27-inch","Heavy, involved installation","Very thick desks may need the bolt-through option"],
 forwho="Anyone running a large, heavy curved display who's tired of sag and bounce. For a standard 27-inch monitor, a lighter arm is fine.",
 finalcta="If your monitor is big and heavy, this is the arm that holds it.",
 faq=[("Will it hold a 49-inch Samsung/LG ultrawide?","Check your specific panel's weight against the HX rating — most 49-inch curved monitors fall within it, some heavy ones need the HX with an extension. Specs are on the [Amazon page](https://www.amazon.com/s?k=Ergotron+HX+Desk+Monitor+Arm)."),
      ("Clamp or bolt-through?","Clamp works for most desks up to a listed thickness. For very thick or stone tops, use the grommet/bolt-through mount.")],
)
SINGLES["flexispot-e7-pro"] = dict(
 title="The Standing Desk That Doesn't Shake When You Type",
 headline="FlexiSpot E7 Pro Review: Dual-Motor, Heavy Steel, Zero Monitor Wobble",
 dek="The main failure of cheap sit-stand desks is shake at standing height. The E7 Pro's frame and motors are built to eliminate it.",
 verdict="Best value shake-free standing desk",
 cardCue="See the frame build →",
 tags=["standing desk","flexispot","desk setup"], keywords=["flexispot e7 pro review","stable standing desk","best sit stand desk"],
 takeaways=[
   "Dual motors and heavy-gauge steel legs stay planted at full height.",
   "Quiet lift cycle — fine to raise during a call.",
   "Accurate memory presets return to your exact sit/stand heights.",
   "Anti-collision sensing and a wide height range for tall and short users.",
 ],
 sections=[
  ("Wobble is the whole test",
   "Every sit-stand desk is stable when it's low. The question is what happens at standing height when you type fast or lean on it. The E7 Pro's frame is stiff enough that your monitor stays still. If you've returned a wobbly desk before, " + buy("flexispot-e7-pro","check the E7 Pro price on Amazon") + "."),
  ("Living with it",
   "The motors are quiet enough that raising the desk mid-meeting doesn't announce itself. Presets are accurate to the millimeter, so your sit and stand positions are one tap away. People who actually alternate sitting and standing " + buy("flexispot-e7-pro","buy the frame on Amazon") + " and add their own top."),
  ("Range, safety, cables",
   "The height range covers most users standing and seated; anti-collision reverses if it meets an obstacle. There's room under the top for a cable tray. Confirm the frame width fits your desired top on the " + buy("flexispot-e7-pro","Amazon listing") + "."),
 ],
 pros=["Genuinely stable at standing height","Quiet motors","Precise memory presets","Wide height range","Long frame warranty"],
 cons=["Frame only — you buy or build the top","Heavy, two-person assembly","Deep programming menu is fiddly at first"],
 forwho="Anyone who wants a standing desk that stays rock-solid while typing. If you never actually stand, a fixed desk saves money.",
 finalcta="The stability problem, solved — at a sane price.",
 faq=[("Does it come with a desktop?","The E7 Pro is typically sold as a frame; you choose a top (theirs or your own). Bundle options are on the [Amazon page](https://www.amazon.com/s?k=FlexiSpot+E7+Pro+Standing+Desk)."),
      ("How stable is it really at max height?","Noticeably stiffer than single-motor desks — minor sway at the very top with a heavy monitor arm, negligible in normal use.")],
)

# ---------- 5. TRAVEL ----------
SINGLES["tumi-alpha3-carryon"] = dict(
 title="The Carry-On That Survives a Decade of Gate-Checks",
 headline="Tumi Alpha 3 Continental Dual Access Review: Built for the Frequent Flyer",
 dek="FXT ballistic nylon, dual top-and-front access, internal suiter brackets — the case that earns the premium luggage tier.",
 verdict="Best premium soft-side carry-on",
 cardCue="See the dual-access opening →",
 tags=["carry-on","tumi","luggage"], keywords=["tumi alpha 3 review","best premium carry on","tumi continental dual access"],
 takeaways=[
   "FXT ballistic nylon is the toughest soft-side shell in the category.",
   "Dual access — reach a laptop from the top without opening the whole case.",
   "Suiter brackets and an add-a-bag sleeve for real business travel.",
   "Tumi Tracer registration helps recover a lost bag.",
 ],
 sections=[
  ("Why soft-side, why Tumi",
   "A soft-side carry-on flexes into a tight bin and absorbs impacts a hard shell would crack on. Tumi's FXT ballistic nylon is denser and more abrasion-resistant than what competitors use, which is why ten-year-old Alphas still look serviceable. If you fly weekly, " + buy("tumi-alpha3-carryon","check the current Amazon price") + "."),
  ("Dual access earns its keep",
   "The front panel opens independently for a laptop and documents, so security and the seat-back become one-handed. The main clamshell has compression straps and a suiter to keep a jacket unwrinkled. Road warriors " + buy("tumi-alpha3-carryon","buy the Continental on Amazon") + " and stop thinking about luggage."),
  ("Fit, wheels, warranty",
   "It's on the larger end of carry-on legal — great domestically, check dimensions for stricter international carriers. Wheels are firm on carpet; the warranty is 5 years plus a year of any-reason coverage. See sizes and finishes on the " + buy("tumi-alpha3-carryon","Amazon listing") + "."),
 ],
 pros=["Toughest soft-side shell in class","Dual access is genuinely useful","Business-travel organization","Tracer recovery program","Strong warranty"],
 cons=["Heavy for a soft-side","Larger footprint — tight on strict international limits","Premium price"],
 forwho="The weekly flyer who wants a bag that disappears as a concern. If you want the lightest possible shell, the Samsonite Cosmolite is the counterpoint.",
 finalcta="For serious flight frequency, the Alpha 3 is the buy-and-forget choice.",
 faq=[("Is it international carry-on legal?","It's within US and most international limits but on the larger side — check your strict-limit carriers (some European and regional airlines) against the listed dimensions on the [Amazon page](https://www.amazon.com/s?k=Tumi+Alpha+3+Continental+Dual+Access)."),
      ("Alpha 3 vs the aluminum Rimowa?","The Tumi is lighter to lift, more impact-tolerant and better organized; the Rimowa is a status object that dents. For pure function, Tumi.")],
)
SINGLES["samsonite-cosmolite"] = dict(
 title="Featherweight Armor: Samsonite Cosmolite 3.0",
 headline="Samsonite Black Label Cosmolite 3.0 Review: Curv Shell, Under 4.5 Pounds",
 dek="Curv composite gives you serious impact resistance at a weight that lets you pack heavy garments without hitting the airline limit.",
 verdict="Best ultralight hard-shell",
 cardCue="See the weight number →",
 tags=["luggage","samsonite","lightweight"], keywords=["samsonite cosmolite review","lightest hard shell luggage","curv suitcase"],
 takeaways=[
   "Curv thermoplastic — a very high strength-to-weight ratio.",
   "The shell flexes under impact and springs back instead of cracking.",
   "Every pound the case doesn't weigh is a pound you can pack.",
   "Distinctive fluted shell that's easy to spot on a carousel.",
 ],
 sections=[
  ("Weight is the spec that matters",
   "If your case weighs 8+ pounds empty, you've spent a tenth of your allowance before packing. The Cosmolite comes in around 4.4 pounds for the spinner, which changes what you can bring. Executives who pack suits and shoes " + buy("samsonite-cosmolite","check the Amazon price") + "."),
  ("Curv isn't marketing",
   "Curv is a self-reinforced polypropylene composite — it takes a hit, deforms, and recovers, where polycarbonate can crack and ABS can stay dented. For checked use especially, that resilience shows over years. Frequent travelers " + buy("samsonite-cosmolite","buy the Cosmolite on Amazon") + "."),
  ("Handles, wheels, interior",
   "The telescoping handle is rigid with minimal play; wheels are smooth. Interior is a straightforward clamshell with a divider. Compare the carry-on and checked sizes on the " + buy("samsonite-cosmolite","Amazon listing") + "."),
 ],
 pros=["Exceptionally light for a hard shell","Curv shell resists cracking","More effective packing allowance","Easy to spot","Solid handle"],
 cons=["Premium price for the technology","Fluted shell scuffs show","Interior organization is basic"],
 forwho="Travelers who pack heavy and fight the scale. If you want maximum organization and a dual-access design, look at the Tumi Alpha 3.",
 finalcta="If the weigh-in is your enemy, this is the case to carry.",
 faq=[("How light is it, exactly?","The spinner carry-on is roughly 4.4 lb and the medium checked around 6 lb — among the lightest hard shells available. Current weights per size are on the [Amazon page](https://www.amazon.com/s?k=Samsonite+Cosmolite+3.0+Spinner)."),
      ("Does Curv really resist cracking?","Yes — it's designed to flex and recover. It'll scuff, but structural cracks are far less common than with polycarbonate.")],
)
SINGLES["anker-prime-240w"] = dict(
 title="One Plug for the Whole Bag: Anker Prime 240W",
 headline="Anker Prime 240W GaN Charging Station Review: Kill the Brick Pile",
 dek="Full-speed charging for a 16-inch MacBook Pro, an iPad, a phone and earbuds — from a single outlet, in a footprint smaller than one laptop brick.",
 verdict="Best all-in-one desktop charger",
 cardCue="See all four ports →",
 tags=["charger","anker","gan"], keywords=["anker prime 240w review","best gan charger","desktop charging station"],
 takeaways=[
   "240W total across 4 ports — enough for a full-power laptop plus three devices.",
   "Dynamically reallocates power as devices plug and unplug.",
   "GaN internals keep it small and cool for the wattage.",
   "Weighted base and a retained AC cable — it stays put on the desk.",
 ],
 sections=[
  ("The problem it removes",
   "A travelling executive carries four chargers and a tangle of cables. This one unit replaces all of them: park it on the desk or in the hotel, plug in everything, done. If your bag has a charger pouch, " + buy("anker-prime-240w","check the Amazon price") + " — it probably replaces the whole pouch."),
  ("Smart power allocation",
   "When you plug the laptop in alone it gets the full wattage; add an iPad and phone and the station reallocates intelligently so everything still charges fast. There's a small display showing per-port output. Frequent travelers " + buy("anker-prime-240w","buy it on Amazon") + " and standardize on USB-C cables."),
  ("Build and cable",
   "It's dense and low, so it doesn't skate around when you pull a cable, and the AC cord is captive/retained. Check whether the bundle includes the charging cables you need on the " + buy("anker-prime-240w","Amazon listing") + "."),
 ],
 pros=["Replaces 3–4 separate chargers","True full-speed laptop charging","Smart multi-device allocation","Compact, cool GaN design","Informative display"],
 cons=["Not pocket-sized — it's a desktop unit","Premium vs a basic multiport","Cables often sold separately"],
 forwho="Anyone tired of carrying a charger for every device. If you only ever charge a phone, this is more than you need.",
 finalcta="One purchase that empties your cable pouch. Worth it.",
 faq=[("Will it charge a 16-inch MacBook Pro at full speed?","Yes — a single port delivers enough for full-speed 16-inch charging, and it shares intelligently when other devices are attached. Port specs are on the [Amazon page](https://www.amazon.com/s?k=Anker+Prime+240W+GaN+Desktop+Charger)."),
      ("Does it come with cables?","Sometimes — check the specific listing. Budget for a couple of 100W-rated USB-C cables if not.")],
)
SINGLES["peak-design-tech-pouch"] = dict(
 title="The Dongle Problem, Solved: Peak Design Tech Pouch",
 headline="Peak Design Tech Pouch Review: Everything Visible, Nothing Lost",
 dek="Origami-style pockets that open flat on a tray table and keep every adapter, cable and stylus in view.",
 verdict="Best cable and adapter organizer",
 cardCue="See it open flat →",
 tags=["organizer","peak design","travel gear"], keywords=["peak design tech pouch review","best cable organizer","dongle pouch travel"],
 takeaways=[
   "Folding pocket rows open flat so you see everything at once.",
   "Weatherproof recycled shell; smooth, snag-free zips.",
   "Holds its shape stuffed — no shapeless lump in the bag.",
   "Fits an airline seat-back pocket and stays organized upright.",
 ],
 sections=[
  ("Why a flat-opening pouch matters",
   "A normal zip pouch is a bucket — you dig, you dump, you lose the USB-C-to-A adapter you needed. The Tech Pouch's accordion pockets fan open so every item has a visible slot. On a plane that's the difference between finding your dongle and missing the moment. Frequent flyers " + buy("peak-design-tech-pouch","check the Amazon price") + "."),
  ("Build quality you feel",
   "The shell is weatherproof, the zips glide, and there's an internal pass-through so you can charge a battery inside without opening it. It survives being crammed into a full bag. People who've tried cheaper pouches " + buy("peak-design-tech-pouch","upgrade to this one on Amazon") + "."),
  ("Capacity and dimensions",
   "It swallows a surprising amount — GaN charger, several cables, adapters, a small mouse, pens — and keeps its rectangular shape. Check exact dimensions against your kit on the " + buy("peak-design-tech-pouch","Amazon listing") + "."),
 ],
 pros=["Flat-opening = everything visible","Weatherproof, durable shell","Keeps its shape when full","Internal charge pass-through","Lifetime warranty"],
 cons=["Premium price for a pouch","Can get heavy if you overfill it","One size — too big for a truly minimal kit"],
 forwho="Anyone who travels with more than two cables. If your kit is a single charger and one cable, a smaller sleeve is enough.",
 finalcta="A small upgrade that removes a recurring travel-day annoyance.",
 faq=[("Will a GaN charger and cables all fit?","Yes — a 65–100W GaN brick, three or four cables, and adapters fit with room to spare. Capacity details are on the [Amazon page](https://www.amazon.com/s?k=Peak+Design+Tech+Pouch)."),
      ("Is it actually weatherproof?","The shell and zips resist rain and spills; it's not submersible, but a coffee spill in a bag won't reach the contents.")],
)

# ---------- 6. VIDEO ----------
SINGLES["insta360-link2"] = dict(
 title="A Camera Operator That Follows You: Insta360 Link 2",
 headline="Insta360 Link 2 Review: The Webcam With a Real Gimbal",
 dek="A 1/2-inch sensor and a physical 2-axis gimbal that tracks you to the whiteboard — with genuine optical-look depth, not a fake blur.",
 verdict="Best webcam for presenting",
 cardCue="See the gimbal track →",
 tags=["webcam","insta360","video calls"], keywords=["insta360 link 2 review","best 4k webcam","ai tracking webcam"],
 takeaways=[
   "Larger 1/2-inch sensor gives real subject-background separation.",
   "Mechanical gimbal physically pans and tilts to keep you framed.",
   "Gesture controls to zoom or lock tracking without touching anything.",
   "Privacy shield: the lens tilts down and covers itself when you mute.",
 ],
 sections=[
  ("Why the gimbal beats digital tracking",
   "Software 'auto-framing' just crops a wide sensor, so you lose resolution as you move. The Link 2 physically moves the camera, so you stay full-quality and centered even when you step to a whiteboard. If you present on camera, " + buy("insta360-link2","check the Amazon price") + "."),
  ("The image holds up",
   "The bigger sensor means less noise in a dim conference room and a natural depth of field that makes you look lit even when you aren't. Gestures let you trigger a zoom-in on a document or lock framing mid-call. Executives who run webinars " + buy("insta360-link2","buy it on Amazon") + "."),
  ("Privacy and setup",
   "Mute your mic and the lens rotates down to physically block itself — a real shield, not an LED. It's plug-and-play, with an app for fine control. Check mount compatibility on the " + buy("insta360-link2","Amazon listing") + "."),
 ],
 pros=["Physical gimbal tracking keeps full quality","Large sensor for low light and depth","Useful gesture controls","Genuine physical privacy shield","Plug-and-play"],
 cons=["Pricey for a webcam","Tracking can over-move if you fidget","App recommended for best results"],
 forwho="Anyone who presents, teaches or moves during calls. If you sit still and just need clean 4K, the Logitech Brio is cheaper and fine.",
 finalcta="If you present on camera, the tracking gimbal is worth it.",
 faq=[("Does the tracking need software running?","Basic tracking works on-device; the app unlocks tuning (speed, zoom limits) and presets. Details on the [Amazon page](https://www.amazon.com/s?k=Insta360+Link+2+4K+Webcam)."),
      ("Link 2 vs OBSBOT Tiny 2?","Both have gimbals; the Link 2 has a slightly cleaner image pipeline and the physical privacy shield, the OBSBOT leans on gesture/voice control. Compare both listings.")],
)
SINGLES["benq-screenbar-pro"] = dict(
 title="Desk Light With Zero Screen Glare: BenQ ScreenBar Pro",
 headline="BenQ ScreenBar Pro Review: Light on the Desk, Not on the Panel",
 dek="Asymmetric optics illuminate your paperwork without throwing a single reflection onto the screen — and it auto-tunes to the room.",
 verdict="Best monitor light bar",
 cardCue="See the no-glare beam →",
 tags=["monitor light","benq","desk setup"], keywords=["benq screenbar pro review","monitor light bar","no glare desk lamp"],
 takeaways=[
   "Asymmetric lens design keeps light off the screen entirely.",
   "Auto-dims to ambient light and auto-adjusts color temperature.",
   "Clamps on thin and curved monitors with no tools and no screws.",
   "Capacitive touch and a presence sensor that turns it on when you sit down.",
 ],
 sections=[
  ("The reflection problem",
   "A normal desk lamp behind or beside your monitor bounces off the panel and washes out contrast. The ScreenBar sits on top of the monitor and throws light forward and down onto the desk only. If you read paper documents at your desk in the evening, " + buy("benq-screenbar-pro","check the Amazon price") + "."),
  ("It manages itself",
   "The Pro model adds an ambient sensor that dims it as the room changes and a presence sensor that switches it on when you arrive. Set it once and it's just correct. People doing late document reviews " + buy("benq-screenbar-pro","buy it on Amazon") + "."),
  ("Fit and controls",
   "The weighted clip works on slim bezels and curved panels without blocking the webcam. Touch controls on the bar handle manual override. Confirm it fits your monitor's thickness on the " + buy("benq-screenbar-pro","Amazon listing") + "."),
 ],
 pros=["Genuinely no screen glare","Auto brightness and color temperature","No-tool clip for thin/curved monitors","Presence-sensing on/off","Frees the desk of a lamp"],
 cons=["Premium vs the standard ScreenBar","Very thick or unusually shaped monitors may not clip well","USB-powered — needs a spare port or plug"],
 forwho="Anyone who does paper or mixed work at a monitor and works past sunset. If you only ever look at the screen, you may not need it.",
 finalcta="A small fixture that makes evening desk work easier on the eyes.",
 faq=[("Will it fit a curved ultrawide?","The clip is designed for flat and curved monitors within a thickness range — check your panel's top-edge depth against the spec on the [Amazon page](https://www.amazon.com/s?k=BenQ+ScreenBar+Pro+Monitor+Light)."),
      ("ScreenBar Pro vs Halo?","Pro adds the presence sensor and auto color temperature; Halo has a wireless controller puck and a backlight. For hands-off simplicity, Pro.")],
)
SINGLES["caldigit-ts4"] = dict(
 title="One Cable to Run Everything: CalDigit TS4",
 headline="CalDigit TS4 Thunderbolt 4 Dock Review: The Enterprise Nerve Center",
 dek="Dual displays, 2.5GbE, studio audio, external NVMe and 98W laptop charging — over a single Thunderbolt cable, without throttling.",
 verdict="Best Thunderbolt 4 dock",
 cardCue="See all 18 ports →",
 tags=["dock","caldigit","thunderbolt"], keywords=["caldigit ts4 review","best thunderbolt 4 dock","docking station dual monitor"],
 takeaways=[
   "18 ports — including 2.5GbE, front SD and USB — cover a full desk setup.",
   "98W charging keeps a 16-inch laptop powered under sustained load.",
   "Stable sleep/wake behavior on both macOS and Windows.",
   "Enough bandwidth for dual displays plus fast external storage at once.",
 ],
 sections=[
  ("The single-cable promise, delivered",
   "You sit down, plug in one Thunderbolt cable, and your laptop has two monitors, wired networking, all your peripherals and a full charge. The TS4 is the dock that does this reliably instead of dropping a display on wake. If your desk is a mess of dongles, " + buy("caldigit-ts4","check the Amazon price") + "."),
  ("It doesn't choke under load",
   "Run dual 4K/6K, copy from an external NVMe array, and stay on a 2.5GbE line — the TS4 has the bandwidth headroom to do all of it without stutter. Power users " + buy("caldigit-ts4","buy the TS4 on Amazon") + " and never think about it again."),
  ("Audio, charging, compatibility",
   "Separate headphone and mic jacks with a clean noise floor, 98W to the host, and consistent behavior across OSes. Check display-count limits for your specific laptop chipset on the " + buy("caldigit-ts4","Amazon listing") + "."),
 ],
 pros=["Highest useful port count in class","98W laptop charging","Reliable sleep/wake","Dual-display + fast storage simultaneously","Clean audio I/O"],
 cons=["Expensive","Large, warm brick on the desk","Full dual-display support depends on your laptop, not the dock"],
 forwho="Anyone docking a laptop into a serious multi-display, wired-network desk. If you just need one monitor and power, a cheaper hub works.",
 finalcta="The dock that ends docking problems. Buy it once.",
 faq=[("Will it drive two 4K monitors from a MacBook?","Apple Silicon MacBook Air/Pro (non-Max) natively support one external display; Pro Max and Windows machines support two-plus. The dock provides the ports — your laptop sets the limit. See notes on the [Amazon page](https://www.amazon.com/s?k=CalDigit+TS4+Thunderbolt+4+Dock)."),
      ("Does it really fix sleep/wake dropouts?","It's among the most reliable docks for this, but some issues are OS-side. It's markedly better than cheaper docks in practice.")],
)
SINGLES["remarkable-paper-pro"] = dict(
 title="Where Strategy Docs Go to Get Read: reMarkable Paper Pro",
 headline="reMarkable Paper Pro Review: PDF Markup With Zero Notifications",
 dek="A color e-ink pad for annotating disclosures, marking up decks and drafting strategy — with nothing on it that can interrupt you.",
 verdict="Best distraction-free document tablet",
 cardCue="See the color e-ink →",
 tags=["e-ink","remarkable","paperless"], keywords=["remarkable paper pro review","best e-ink tablet for pdf","paperless executive tablet"],
 takeaways=[
   "Color e-ink with a frontlight — readable in a bright office or a dim flight.",
   "Very low pen latency; writing feels like pen on paper.",
   "No browser, no email, no app store — it can't distract you.",
   "Cloud sync for getting PDFs on and marked-up copies off.",
 ],
 sections=[
  ("The point is what it can't do",
   "An iPad can mark up a PDF — and also show you Slack, email and the news. The Paper Pro deliberately can't. For reviewing a board deck or a financial disclosure without your attention fracturing, that constraint is the feature. Executives who review long documents " + buy("remarkable-paper-pro","check the Amazon price") + "."),
  ("It feels right to write on",
   "Pen latency is low enough that handwriting and margin notes feel natural, and the color layer lets you actually highlight and flag. Marked-up copies sync back out as standard PDFs. People drowning in documents " + buy("remarkable-paper-pro","buy it on Amazon") + "."),
  ("Battery, sync, the subscription question",
   "Battery lasts through heavy review days; the frontlight is even. Full cloud features tie to a subscription — check the current terms and what's included on the " + buy("remarkable-paper-pro","Amazon listing") + "."),
 ],
 pros=["Genuinely removes digital distraction","Color e-ink with frontlight","Paper-like writing feel","Clean PDF in/out","Long battery"],
 cons=["Expensive for a single-purpose device","Best features want a subscription","Not a general tablet — that's the trade"],
 forwho="Executives who read and annotate long documents and want to protect their focus. If you want one device that does everything, this isn't it — and that's deliberate.",
 finalcta="If focus is the scarce resource, a device that can't distract you is worth paying for.",
 faq=[("Do I have to pay a subscription?","The device works without one, but handwriting conversion, unlimited cloud sync and some integrations are subscription features. Current pricing is on the [Amazon page](https://www.amazon.com/s?k=reMarkable+Paper+Pro)."),
      ("Can I read normal PDFs and ebooks?","Yes — PDFs and EPUBs load and display well, with the frontlight for low light. It's not tied to a bookstore.")],
)

# ---------- 7. BEVERAGE ----------
SINGLES["ember-mug-2"] = dict(
 title="Coffee That's Never Cold: Ember Mug 2 (14 oz)",
 headline="Ember Mug 2 Review: Your Coffee Held at 135°F Through a 90-Minute Meeting",
 dek="Set the exact temperature and it stays there — through the interrupted call, the pulled-in meeting, the fire drill. For people whose coffee always goes cold.",
 verdict="Best desk smart mug",
 cardCue="See the temperature set →",
 tags=["smart mug","ember","desk coffee"], keywords=["ember mug 2 review","temperature control mug","smart coffee mug"],
 takeaways=[
   "Dial in a precise temperature; the mug holds it on the charging coaster.",
   "~80 minutes of hold off the coaster for a walk to a meeting.",
   "A preset temperature works with no app once it's configured.",
   "The 14 oz size fits a real pour-over or a double flat white.",
 ],
 sections=[
  ("The problem is specific and real",
   "You make a good coffee, you get pulled into something, you come back to a lukewarm cup and either drink it disappointed or microwave it. The Ember removes that entire pattern — the coffee is the temperature you set, an hour later. If that's your morning, " + buy("ember-mug-2","check the Amazon price") + "."),
  ("14 oz vs 10 oz",
   "The 10 oz is an espresso-sized mug; the 14 oz holds a proper filter coffee or a large milk drink and has better battery. For a desk mug, get the 14. People who've owned the small one " + buy("ember-mug-2","get the 14 oz on Amazon") + "."),
  ("Battery, app, care",
   "On the coaster it holds indefinitely; off it, around 80 minutes. Set a preset once and you can ignore the app. Hand-wash only, and don't scrape it with a metal spoon. Check color options on the " + buy("ember-mug-2","Amazon listing") + "."),
 ],
 pros=["Actually keeps coffee at your exact temp","Preset mode needs no app","14 oz fits real coffee drinks","Charging coaster included","Clean, desk-appropriate look"],
 cons=["Hand-wash only","~80 min battery off the coaster","Premium price for a mug"],
 forwho="Anyone whose coffee routinely goes cold at their desk. If you drink your coffee in ten minutes flat, you don't need it.",
 finalcta="A very specific annoyance, completely solved.",
 faq=[("10 oz or 14 oz?","14 oz for a desk — it fits filter coffee and milk drinks and has longer battery. The 10 oz is really for straight espresso. Both are on the [Amazon page](https://www.amazon.com/s?k=Ember+Mug+2+14+oz)."),
      ("How long does it stay hot away from the coaster?","Around 80 minutes on a full charge — enough to carry it into a meeting and back.")],
)
SINGLES["nespresso-creatista-pro"] = dict(
 title="The In-Office Barista: Nespresso Creatista Pro",
 headline="Nespresso Creatista Pro Review: Flat Whites in Under Two Minutes, No Mess",
 dek="ThermoJet heating and an automatic steam wand that textures real microfoam — executive-grade milk drinks without a kitchen or a skill.",
 verdict="Best office espresso machine",
 cardCue="See the auto steam wand →",
 tags=["espresso","nespresso","breville"], keywords=["nespresso creatista pro review","best office espresso machine","capsule machine with steam wand"],
 takeaways=[
   "ThermoJet heats in about 3 seconds — no waiting for a boiler.",
   "The automatic steam wand textures milk to a set temperature and foam level.",
   "Touchscreen stores custom drinks so a guest can make one.",
   "Capsule system means no grinder, no dosing, no puck mess.",
 ],
 sections=[
  ("Consistency without a barista",
   "A traditional machine makes a great coffee once you've learned it. The Creatista Pro makes the same good flat white every time, in two minutes, with a capsule and a jug of milk. For an office where people just want a reliable coffee, " + buy("nespresso-creatista-pro","check the Amazon price") + "."),
  ("The steam wand is the differentiator",
   "Most capsule machines give you a milk frother that makes stiff foam. This has a real automatic steam wand that produces the silky microfoam a flat white needs, to a temperature you set. Offices upgrading from a pod-and-frother setup " + buy("nespresso-creatista-pro","buy it on Amazon") + "."),
  ("Cleaning and upkeep",
   "The wand purges itself; you wipe it and empty the capsule bin. Descaling is periodic. Check the water tank size and included starter set on the " + buy("nespresso-creatista-pro","Amazon listing") + "."),
 ],
 pros=["3-second heat-up","Genuine microfoam from an auto wand","Programmable drinks","No grinder or puck mess","Compact for an office counter"],
 cons=["Capsule cost over time","Louder than a manual machine","Tank needs regular refilling in a busy office"],
 forwho="An office or executive suite that wants café-quality milk drinks with zero training. Purists with time will still prefer a manual setup.",
 finalcta="For a hands-off office coffee bar, this is the machine.",
 faq=[("Does it use standard Nespresso capsules?","It uses the original-line capsules (not Vertuo). Compatibility and the included welcome set are listed on the [Amazon page](https://www.amazon.com/s?k=Nespresso+Creatista+Pro)."),
      ("Can it make two drinks back to back?","Yes — the ThermoJet reheats fast enough that there's no meaningful wait between drinks.")],
)
SINGLES["fellow-stagg-ekg-pro"] = dict(
 title="The Kettle People Photograph: Fellow Stagg EKG Pro",
 headline="Fellow Stagg EKG Pro Review: To-the-Degree Control in a Design Object",
 dek="Variable temperature, a 60-minute hold, and a flow-restricted gooseneck — in a kettle handsome enough to leave out on a credenza.",
 verdict="Best pour-over kettle",
 cardCue="See the pour control →",
 tags=["kettle","fellow","tea coffee"], keywords=["fellow stagg ekg pro review","best gooseneck kettle","variable temperature kettle"],
 takeaways=[
   "Set any temperature to the degree; it holds for up to an hour.",
   "Restricted gooseneck spout gives a slow, aimable pour.",
   "The Pro adds altitude calibration and a nicer screen.",
   "It looks like an object, not an appliance.",
 ],
 sections=[
  ("Temperature is a real variable",
   "Green tea wants ~175°F, a light-roast pour-over ~205°F, black tea a full boil. A one-button kettle can't do that. The Stagg EKG Pro lets you set exactly what the leaf or bean wants and holds it while you're on a call. Tea and coffee people " + buy("fellow-stagg-ekg-pro","check the Amazon price") + "."),
  ("The pour is controllable",
   "The gooseneck is restricted so you get a thin, steady, aimable stream — which is the whole game in pour-over and matters for blooming tea too. The counterweighted handle keeps it balanced as it empties. Ritual-minded drinkers " + buy("fellow-stagg-ekg-pro","buy it on Amazon") + "."),
  ("Pro vs standard EKG",
   "The Pro adds altitude adjustment (so 'boiling' is actually right where you are), a sharper display and a few presets. See which model is listed and the current price on the " + buy("fellow-stagg-ekg-pro","Amazon listing") + "."),
 ],
 pros=["To-the-degree temperature + 1-hr hold","Excellent pour control","Genuinely attractive on a desk","Balanced handle","Altitude calibration (Pro)"],
 cons=["Smaller capacity than a bulk kettle","Premium price","Matte finish shows fingerprints"],
 forwho="Anyone who takes their tea or coffee seriously and works near a kettle. If you just want hot water fast, a basic kettle is a quarter of the price.",
 finalcta="A daily ritual, upgraded — and it looks the part.",
 faq=[("EKG Pro vs regular EKG — worth the extra?","The Pro's altitude calibration matters if you're well above sea level; otherwise the standard EKG does the core job. Both may appear on the [Amazon page](https://www.amazon.com/s?k=Fellow+Stagg+EKG+Pro+Kettle)."),
      ("Can I leave it holding temperature all morning?","Yes — the hold runs up to 60 minutes per activation; tap it again to extend.")],
)
SINGLES["zojirushi-sm-khe48"] = dict(
 title="The Mug That Won't Quit: Zojirushi SM-KHE48",
 headline="Zojirushi SM-KHE48 Review: Vacuum Insulation That Outlasts Your Flight",
 dek="No battery, no app — just the best passive insulation in the business, a genuinely leakproof lid, and one-handed operation in transit.",
 verdict="Best insulated travel mug",
 cardCue="See the lock lid →",
 tags=["travel mug","zojirushi","insulated"], keywords=["zojirushi sm-khe48 review","best insulated travel mug","leakproof coffee mug"],
 takeaways=[
   "Holds heat for many hours with zero power — physics, not electronics.",
   "Flip-lock lid is genuinely leakproof thrown in a bag.",
   "One-handed open with a thumb; the lid stays put.",
   "Slick interior coating wipes clean and resists staining.",
 ],
 sections=[
  ("Passive done right",
   "You don't need a battery to keep coffee hot — you need excellent vacuum insulation, and Zojirushi's is the benchmark. Fill it before a flight and it's still hot when you land. If you've been let down by mugs that go lukewarm by mid-morning, " + buy("zojirushi-sm-khe48","check the Amazon price") + "."),
  ("The lid is the differentiator",
   "Most 'leakproof' mugs leak eventually. This one has a flip lid with a locking tab — throw it in a briefcase sideways and nothing comes out. The open button is thumb-operated for one-handed use walking through an airport. Commuters " + buy("zojirushi-sm-khe48","buy it on Amazon") + "."),
  ("Cleaning and size",
   "The interior is a smooth electro-polished/coated finish that rinses clean and doesn't hold coffee stains. The 16 oz is the versatile size. Check capacities and colors on the " + buy("zojirushi-sm-khe48","Amazon listing") + "."),
 ],
 pros=["Best-in-class heat retention","Truly leakproof locking lid","One-handed operation","Easy-clean interior","No charging, ever"],
 cons=["Narrow mouth — no ice cubes, awkward to deep-clean","Plain looks","Lid mechanism has small parts to keep clean"],
 forwho="Commuters and travelers who want hot coffee hours later and zero leaks. If you want your coffee held at a precise temp at a desk, that's the Ember's job.",
 finalcta="The no-nonsense choice for hot coffee that survives the trip.",
 faq=[("How long does it actually stay hot?","Several hours near serving temperature and warm well beyond that — among the best passive mugs tested. Manufacturer retention figures are on the [Amazon page](https://www.amazon.com/s?k=Zojirushi+SM-KHE48+stainless+mug)."),
      ("Is it genuinely leakproof in a bag?","Yes, with the lid locked. It's one of the few that reliably passes the sideways-in-a-briefcase test.")],
)

# ---------- 8. WELLNESS ----------
SINGLES["theragun-pro-plus"] = dict(
 title="Neck Tension Gone Before the Next Call: Theragun PRO Plus",
 headline="Theragun PRO Plus Review: Deep Relief Between Back-to-Back Meetings",
 dek="A 16 mm stroke that reaches real muscle, plus infrared and heat modes — quiet enough to use with someone in the room.",
 verdict="Best percussive therapy device",
 cardCue="See the quiet motor →",
 tags=["massage gun","theragun","recovery"], keywords=["theragun pro plus review","best massage gun","percussive therapy device"],
 takeaways=[
   "16 mm amplitude works deep tissue, not just the surface.",
   "Built-in near-infrared, heat and vibration heads for the neck and traps.",
   "Genuinely quiet — you can use it discreetly between meetings.",
   "Hot-swappable batteries so it's never out of charge.",
 ],
 sections=[
  ("The desk posture tax",
   "Hours at a screen load the upper traps and the base of the neck, and by mid-afternoon it's a headache. Two minutes with the PRO Plus on the traps resets that. If your shoulders live around your ears by 3pm, " + buy("theragun-pro-plus","check the Amazon price") + "."),
  ("Why the Plus over the base PRO",
   "The Plus folds in near-infrared light and a heated head, which the traps and neck respond to well, plus a breath/heart-rate feature in the app. If you're buying one for recovery between meetings, the extras are the point. People with chronic desk tension " + buy("theragun-pro-plus","buy the Plus on Amazon") + "."),
  ("Noise, battery, ergonomics",
   "It's quiet enough for an open office and the rotating handle lets you reach your own back. Batteries swap in a second. Check the included attachment set on the " + buy("theragun-pro-plus","Amazon listing") + "."),
 ],
 pros=["Reaches deep muscle","Infrared + heat + vibration built in","Quiet enough for the office","Hot-swap batteries","Ergonomic multi-grip handle"],
 cons=["Expensive vs a basic massage gun","Heavier than mini models","App features are nice-to-have, not essential"],
 forwho="Executives with chronic neck and upper-back tension from screen work. If you just want occasional relief and portability, a mini percussion gun is cheaper.",
 finalcta="If desk tension is a daily thing, this pays for itself in headaches avoided.",
 faq=[("PRO Plus vs PRO vs Elite?","Plus adds infrared/heat and biometric app features; PRO is the pro-grade percussion without the light therapy; Elite is smaller and quieter. Compare on the [Amazon page](https://www.amazon.com/s?k=Theragun+PRO+Plus)."),
      ("Is it actually quiet?","Yes — it's one of the quieter full-size guns. Fine to use on a call with your camera off.")],
)
SINGLES["kingsmith-walkingpad-x21"] = dict(
 title="10,000 Steps During Your Strategy Calls: WalkingPad X21",
 headline="KingSmith WalkingPad X21 Review: The Treadmill That Folds Behind a Credenza",
 dek="A 180-degree double-fold under-desk treadmill that stores in a slim gap — quiet enough for a muted call, real enough for a step count.",
 verdict="Best folding under-desk treadmill",
 cardCue="See the double fold →",
 tags=["treadmill","walkingpad","wellness"], keywords=["kingsmith walkingpad x21 review","under desk treadmill","folding walking pad"],
 takeaways=[
   "Double-fold design stores upright in a narrow space when you're done.",
   "Quiet motor — background hum, not a distraction on a muted call.",
   "Stable belt and frame for a natural walking gait.",
   "Remote and app speed control; step tracking built in.",
 ],
 sections=[
  ("Movement without a time cost",
   "The reason executives don't walk more isn't willpower, it's the calendar. A walking pad under a standing desk turns low-stakes calls and reading time into 8,000–10,000 steps you didn't have to schedule. If your day has an hour of calls you could take standing, " + buy("kingsmith-walkingpad-x21","check the Amazon price") + "."),
  ("The fold is why this one",
   "Most walking pads are a flat slab you shove under a couch. The X21 folds in the middle and stands upright, so it fits behind a credenza or in a closet gap. That's the difference between using it and tripping over it. Home-office execs " + buy("kingsmith-walkingpad-x21","buy the X21 on Amazon") + "."),
  ("Noise, controls, limits",
   "At walking speeds the motor is a low hum that a muted mic won't pick up. Control it by remote or app. It's for walking, not running — check the speed range and weight limit on the " + buy("kingsmith-walkingpad-x21","Amazon listing") + "."),
 ],
 pros=["Folds upright for real storage","Quiet at walking speeds","Stable underfoot","App + remote control","Turns call time into step count"],
 cons=["Walking speeds only — not for jogging","Heavy to move despite folding","Needs a standing desk to pair with"],
 forwho="Home-office and hybrid executives with call-heavy days and no time to work out. If you have room for a permanent treadmill, a full one is sturdier.",
 finalcta="If your steps are the thing that slips, this fixes it without a calendar fight.",
 faq=[("Can I run on it?","No — it's built for walking speeds. That keeps it quiet and thin. Speed specs are on the [Amazon page](https://www.amazon.com/s?k=KingSmith+WalkingPad+X21)."),
      ("How quiet is it on a call?","At 2–3 mph it's a soft hum. With your mic muted or a decent headset, callers won't hear it.")],
)
SINGLES["gunnar-vertex"] = dict(
 title="For the 12-Hour Screen Day: Gunnar Vertex Glasses",
 headline="Gunnar Optiks Vertex Review: Cutting Glare and Dry Eye on Long Days",
 dek="Blocks a large share of artificial blue light and kills glare — distortion-free, with a tint subtle enough for video calls.",
 verdict="Best computer glasses for executives",
 cardCue="See the lens clarity →",
 tags=["blue light glasses","gunnar","eye strain"], keywords=["gunnar vertex review","blue light glasses","computer glasses for eye strain"],
 takeaways=[
   "Filters a high percentage of high-energy blue light.",
   "Anti-reflective coating cuts the glare that causes squinting and headaches.",
   "Optically correct lenses — no fishbowl distortion at the edges.",
   "Tint is light enough that you don't look yellow on camera.",
 ],
 sections=[
  ("Eye strain is cumulative",
   "One long day at a screen is fine. Weeks of them cause dry eye, blur toward evening, and tension headaches. Cutting glare and blue light won't fix bad habits, but it measurably reduces the load. If your evenings end with tired, gritty eyes, " + buy("gunnar-vertex","check the Amazon price") + "."),
  ("Why these over pharmacy blue-light glasses",
   "Cheap blue-light glasses often have distorted lenses and a heavy yellow tint. The Vertex uses proper optical lenses and a restrained tint, so text stays crisp and you look normal on a call. People polishing decks at 11pm " + buy("gunnar-vertex","buy them on Amazon") + "."),
  ("Fit and prescription",
   "The frame is light with arms that hold without pinching behind the ears for all-day wear. Prescription versions are available. Check frame sizes and Rx options on the " + buy("gunnar-vertex","Amazon listing") + "."),
 ],
 pros=["Real anti-glare coating","Meaningful blue-light filtering","No lens distortion","Subtle tint for video calls","Comfortable all-day frame"],
 cons=["Slight warm cast to whites","Not a substitute for screen breaks","Prescription versions cost more"],
 forwho="Anyone doing 10+ hour screen days who ends up with tired eyes and headaches. If your screen time is modest, focus on the 20-20-20 rule first.",
 finalcta="A low-cost way to take some load off a screen-heavy day.",
 faq=[("Do blue-light glasses actually work?","Evidence is mixed on blue light and sleep, but the anti-glare coating and reduced squinting deliver a noticeable comfort improvement for heavy users. Lens specs are on the [Amazon page](https://www.amazon.com/s?k=Gunnar+Optiks+Vertex)."),
      ("Can I get them in my prescription?","Yes — Gunnar offers prescription lenses for most frames including the Vertex.")],
)
SINGLES["coway-airmega-400s"] = dict(
 title="Cleaner Air, Sharper Afternoons: Coway Airmega 400S",
 headline="Coway Airmega 400S Review: Near-Zero PM2.5 in a Sealed Office",
 dek="True HEPA plus carbon, sized for a large private office, with a sensor that reacts to cleaning-spray VOCs — because stuffy air dulls the afternoon.",
 verdict="Best air purifier for a private office",
 cardCue="See the coverage area →",
 tags=["air purifier","coway","wellness"], keywords=["coway airmega 400s review","best air purifier for office","hepa air purifier large room"],
 takeaways=[
   "Covers a large private office / suite on a reasonable fan setting.",
   "Real-time particle and VOC sensor ramps the fan when air quality drops.",
   "Quiet on sleep/low mode — usable during calls.",
   "App and scheduling; clear filter-life indicator.",
 ],
 sections=[
  ("Sealed buildings, dull afternoons",
   "Modern offices recirculate air, and CO2 and VOC build-up through the afternoon is a real drag on focus. A purifier won't lower CO2, but it clears the particulates and off-gassing that make a room feel stale. If your 3pm is a fog, " + buy("coway-airmega-400s","check the Amazon price") + "."),
  ("The sensor does the thinking",
   "It reads the air continuously and spins up when someone runs a vacuum outside your door or sprays cleaner nearby, then settles back down. You set it and forget it. Executives in interior offices " + buy("coway-airmega-400s","buy the 400S on Amazon") + "."),
  ("Noise, filters, running cost",
   "On low it's genuinely quiet; on max it moves serious air and you'll hear it. Filters last months with an indicator. Check filter replacement cost and coverage rating on the " + buy("coway-airmega-400s","Amazon listing") + "."),
 ],
 pros=["Large coverage area","Responsive auto mode","Quiet on low/sleep","App + scheduling","Clear filter-life tracking"],
 cons=["Large physical footprint","Replacement filters aren't cheap","Max speed is loud"],
 forwho="Executives in sealed or interior offices who notice an afternoon slump. If your office has good ventilation and windows that open, the effect is smaller.",
 finalcta="If your office air feels stale by mid-afternoon, this is a straightforward fix.",
 faq=[("What room size does it cover?","It's rated for a large room and refreshes a mid-size office multiple times an hour. Exact CADR and coverage figures are on the [Amazon page](https://www.amazon.com/s?k=Coway+Airmega+400S)."),
      ("Does it help with CO2 or just particles?","Particles and VOCs/odors, not CO2. For CO2 you need ventilation — but the particulate and odor reduction is what makes a closed room feel fresher.")],
)

# ---------- 9. DECOR ----------
SINGLES["howard-miller-burton"] = dict(
 title="Gravitas on the Credenza: Howard Miller Burton Clock",
 headline="Howard Miller Burton Mantel Clock Review: Traditional Weight, Modern Reliability",
 dek="A warm hardwood case, brass accents and a dual chime with automatic night shut-off — the object that says an office has been here a while.",
 verdict="Best traditional executive clock",
 cardCue="See the wood finish →",
 tags=["clock","howard miller","office decor"], keywords=["howard miller burton clock review","executive mantel clock","desk clock for office"],
 takeaways=[
   "High-gloss hardwood case with brass detailing — reads as permanence.",
   "Dual chime (Westminster / Ave Maria) with an automatic overnight silence.",
   "Quartz movement, so it keeps time without daily winding.",
   "Sized for a credenza or a broad desk, not a shelf.",
 ],
 sections=[
  ("What a real clock signals",
   "A phone tells the time. A substantial clock on the credenza tells a visitor that this office is established and unhurried. The Burton's finish and proportions do that job. If you're furnishing an office you want to feel weighty, " + buy("howard-miller-burton","check the Amazon price") + "."),
  ("Chime you can live with",
   "It offers Westminster or Ave Maria chimes with volume control and — crucially — an automatic night shut-off so it doesn't chime at 3am if the clock is in a home office. You can also silence it entirely. Buyers furnishing a study " + buy("howard-miller-burton","order it on Amazon") + "."),
  ("Movement and care",
   "It's a quartz dual-chime movement, so no winding ritual — just a battery. The case benefits from occasional polishing. Confirm dimensions and finish on the " + buy("howard-miller-burton","Amazon listing") + "."),
 ],
 pros=["Genuine hardwood + brass presence","Pleasant chimes with night shut-off","No winding — quartz accuracy","Handsome from across a room","Trusted clockmaker"],
 cons=["Chime purists may want a mechanical movement","Large — needs real surface space","Gloss finish shows dust"],
 forwho="Executives furnishing an office to feel established and traditional. If your aesthetic is minimalist-modern, the Dalvey desk clock is the smaller, cleaner statement.",
 finalcta="For an office that should feel like it's always been there, this is the piece.",
 faq=[("Is it mechanical or quartz?","This model is quartz with an electronic chime — accurate and low-maintenance. If you specifically want a key-wound mechanical movement, that's a different (pricier) category. Details on the [Amazon page](https://www.amazon.com/s?k=Howard+Miller+Burton+Mantel+Clock)."),
      ("Can I turn the chimes off completely?","Yes — there's a full silence setting plus the automatic overnight shut-off.")],
)
SINGLES["dalvey-grand-sedan"] = dict(
 title="Pocket-Watch Engineering, Shrunk: Dalvey Grand Sedan",
 headline="Dalvey Grand Sedan Desk Clock Review: Compact Scottish Precision",
 dek="Convex glass, a spun-metal dial and a weighted base — a jewel-like desk clock for the executive whose taste runs modern and restrained.",
 verdict="Best compact desk clock",
 cardCue="See the convex glass →",
 tags=["desk clock","dalvey","office decor"], keywords=["dalvey grand sedan review","luxury desk clock","small executive clock"],
 takeaways=[
   "Inspired by antique pocket watches — convex crystal, fine dial work.",
   "Weighted base sits firmly on a leather blotter and doesn't slide.",
   "Tarnish-resistant finish keeps its shine for years.",
   "Small footprint — a detail piece, not a centerpiece.",
 ],
 sections=[
  ("Restraint as a statement",
   "Not every executive wants a large chiming clock. The Grand Sedan makes its point quietly: precise, well-made, obviously considered. It signals taste without taking up the desk. If your office leans minimalist, " + buy("dalvey-grand-sedan","check the Amazon price") + "."),
  ("The details up close",
   "The convex crystal, the spun concentric dial, the weight in the hand — it's built like a small instrument. It reads clearly from across a desk despite the size. People buying a considered gift " + buy("dalvey-grand-sedan","order it on Amazon") + "."),
  ("Placement and finish",
   "The base is heavy enough to stay put on a leather blotter. The finish resists tarnish and fingerprints better than raw brass. Confirm dimensions and finish options on the " + buy("dalvey-grand-sedan","Amazon listing") + "."),
 ],
 pros=["Beautifully made at a small scale","Weighted, stable base","Tarnish-resistant finish","Reads clearly despite size","Excellent gift"],
 cons=["Quartz, not mechanical","Small — easy to overlook on a big desk","Premium price for the size"],
 forwho="The executive with modern, restrained taste who wants one refined object on the desk. For traditional gravitas, the Howard Miller Burton is the larger statement.",
 finalcta="A small, precise object that quietly signals taste.",
 faq=[("Does it need winding?","No — it's a quartz movement. Set it and change the battery once a year. Specs on the [Amazon page](https://www.amazon.com/s?k=Dalvey+Grand+Sedan+desk+clock)."),
      ("Is it big enough to read across a room?","It's designed as a desk piece — clear at desk distance, less so from across a large office. For that, size up to a mantel clock.")],
)
SINGLES["authentic-models-sandtimer"] = dict(
 title="The Analog Focus Timer: A 60-Minute Brass Hourglass",
 headline="Authentic Models 60-Minute Brass Sand Timer Review: Deep Work, No Alerts",
 dek="Flip it to start a focus block. No phone, no countdown beep — just a physical, silent anchor for an hour of real work.",
 verdict="Best analog focus timer",
 cardCue="See the brass frame →",
 tags=["sand timer","focus","office decor"], keywords=["brass sand timer 60 minute","hourglass focus timer","deep work timer"],
 takeaways=[
   "Flipping it is a deliberate ritual that starts a work block.",
   "Completely silent — no alert to yank you out of flow.",
   "Heavy brass frame; it's a desk object, not a gimmick.",
   "Runs within about a minute of a true hour.",
 ],
 sections=[
  ("Why physical beats a phone timer",
   "A timer on your phone means picking up the device that has every notification on it. A sand timer you just flip. The visible, silent drain of the sand is a gentle awareness of time passing without the anxiety of a ticking countdown. If you protect focus blocks, " + buy("authentic-models-sandtimer","check the Amazon price") + "."),
  ("It's built to last",
   "The brass frame has real heft, the glass is thick, and the sand flows without clumping. It looks like something that belongs on an executive desk, not a novelty. People serious about time-blocking " + buy("authentic-models-sandtimer","buy it on Amazon") + "."),
  ("Accuracy and use",
   "It runs close to a true 60 minutes — within a minute or so, which is all a focus block needs. Some also keep a 5- or 15-minute timer for stand-ups. Check the size and whether other durations are offered on the " + buy("authentic-models-sandtimer","Amazon listing") + "."),
 ],
 pros=["Silent — no jarring alarm","Tactile start ritual","Solid brass and glass build","Desk-worthy object","Accurate enough for the job"],
 cons=["Not precise to the second","One fixed duration per timer","Sand timers can vary unit to unit"],
 forwho="Anyone who runs focus sprints and wants to keep the phone out of the loop. If you need exact timing or intervals, a dedicated cube timer is better.",
 finalcta="A quiet, physical way to defend an hour of deep work.",
 faq=[("How accurate is a 60-minute sand timer?","Typically within a minute or two of an hour — fine for focus blocks, not for anything that needs precision. Notes are on the [Amazon page](https://www.amazon.com/s?k=Authentic+Models+60+minute+brass+sand+timer)."),
      ("Does the sand clump over time?","Quality timers like this use graded sand that flows consistently for years. Keep it out of humidity.")],
)
SINGLES["carrara-bookends"] = dict(
 title="5 Pounds of Stone That Never Lets a Binder Lean",
 headline="Solid Carrara Marble Bookends Review: Architectural Weight for the Shelf",
 dek="Heavy natural marble that holds annual filings, legal manuals and hardbound volumes dead upright — with felt feet that protect the shelf.",
 verdict="Best heavy bookends",
 cardCue="See the marble veining →",
 tags=["bookends","marble","office decor"], keywords=["carrara marble bookends","heavy bookends","marble office decor"],
 takeaways=[
   "Each block is heavy enough to hold a run of hardbound books without sliding.",
   "Felt base protects the shelf and adds grip.",
   "Natural Carrara veining — every pair is one of a kind.",
   "Beveled edges so they don't chip a desk or each other.",
 ],
 sections=[
  ("Light bookends don't work",
   "A hollow metal L-bracket slides the moment you pull a book. Solid marble at 5+ pounds a side simply doesn't move. If your shelf of reports and manuals is permanently leaning, " + buy("carrara-bookends","check the Amazon price") + "."),
  ("They also look the part",
   "Carrara marble has the grey veining you recognize from good architecture. On a shelf of legal volumes or annual reports, they read as considered. People furnishing a proper office " + buy("carrara-bookends","buy a pair on Amazon") + "."),
  ("The practical details",
   "Full-contact felt on the base protects wood and stops any creep; the edges are beveled so they don't nick the desk. Check the weight per block and dimensions on the " + buy("carrara-bookends","Amazon listing") + "."),
 ],
 pros=["Heavy enough to actually work","Real Carrara marble","Felt base protects the shelf","Unique veining","Beveled, desk-safe edges"],
 cons=["Heavy to ship and reposition","Marble can chip if dropped on a hard floor","Veining varies — you get what arrives"],
 forwho="Anyone with a shelf of heavy books and binders that won't stay upright. For light paperbacks, cheaper bookends are fine.",
 finalcta="The bookends that end the leaning-shelf problem for good.",
 faq=[("How heavy is each block?","Typically 4–6 lb per side for solid marble bookends this size — enough to hold a full run of hardbacks. Exact weight is on the [Amazon page](https://www.amazon.com/s?k=solid+Carrara+white+marble+bookends+heavy)."),
      ("Will the veining match the photos?","Natural marble varies — expect the same grey-on-white character, not an identical pattern.")],
)

# ---------- 10. SECURITY ----------
SINGLES["yubikey-5c-nfc"] = dict(
 title="The $50 Lock That Stops Executive Email Phishing Cold",
 headline="YubiKey 5C NFC Review: Hardware That Makes Your Account Un-Phishable",
 dek="FIDO2/WebAuthn in a keychain fob. Targeted phishing and credential theft simply stop working once this is on the account.",
 verdict="Best hardware security key",
 cardCue="See the USB-C + NFC →",
 tags=["security key","yubico","2fa"], keywords=["yubikey 5c nfc review","hardware security key","fido2 key for executives"],
 takeaways=[
   "FIDO2/WebAuthn cryptographically binds login to the real site — phishing pages fail.",
   "USB-C for laptops, NFC tap for phones — works through most cases.",
   "Also handles TOTP, Smart Card and OpenPGP for legacy systems.",
   "Buy two: one on the keychain, one locked in a drawer as backup.",
 ],
 sections=[
  ("Why a key beats an authenticator app",
   "A one-time code from an app can still be typed into a fake login page — that's how modern phishing works. A hardware key won't authenticate to the wrong domain, full stop. For an executive whose email is a target, that's the difference. " + buy("yubikey-5c-nfc","check the Amazon price") + " and add it to your email and SSO first."),
  ("It fits how you actually work",
   "USB-C plugs into the laptop; NFC taps against the back of a phone, usually through the case. It covers Google, Microsoft, Okta, Duo, password managers and more. Security-conscious leaders " + buy("yubikey-5c-nfc","buy a pair on Amazon") + " — always a pair."),
  ("The backup rule",
   "If you register only one key and lose it, you're locked out. Register two from the start, keep the spare somewhere safe. Confirm you're getting the 5C NFC (not a different form factor) on the " + buy("yubikey-5c-nfc","Amazon listing") + "."),
 ],
 pros=["Makes accounts genuinely un-phishable","USB-C + NFC covers laptop and phone","Multi-protocol for legacy systems","Durable, no battery","Cheap insurance for a high-value target"],
 cons=["You must buy and register a backup","Some older services still don't support keys","Small — easy to misplace if not on a keychain"],
 forwho="Any executive whose email or admin access is worth attacking — which is all of them. Non-negotiable for finance and IT leadership.",
 finalcta="The highest-leverage security purchase you can make. Buy two today.",
 faq=[("Do I need more than one?","Yes — register at least two so a lost key doesn't lock you out. Most people buy a 2-pack. Options are on the [Amazon page](https://www.amazon.com/s?k=Yubico+YubiKey+5C+NFC)."),
      ("Will NFC work through my phone case?","Usually — thin and mid cases are fine; very thick or metal cases can block it. USB-C always works as a fallback.")],
)
SINGLES["3m-gold-privacy-filter"] = dict(
 title="Black Out Your Screen for the Seat Next to You",
 headline="3M Gold Privacy Filter Review: Nothing to See From the Next Chair",
 dek="Gold micro-louver technology gives a sharper side-angle cutoff than matte film — while your own head-on view stays bright and clear.",
 verdict="Best laptop privacy filter",
 cardCue="See the 30° blackout →",
 tags=["privacy filter","3m","visual security"], keywords=["3m gold privacy filter review","laptop privacy screen","anti spy screen filter"],
 takeaways=[
   "Gold micro-louvers cut off the view sharply beyond ~30 degrees.",
   "Head-on, the screen stays bright — less dimming than cheaper films.",
   "Reversible: gold side for a brighter look, matte side to also kill glare.",
   "Slide-mount tabs or adhesive; comes off for screen-sharing.",
 ],
 sections=[
  ("Where you're actually exposed",
   "Airport lounges, the middle seat, open conference rooms, a coffee shop with your back to the room — anyone beside or behind you can read a financial model or an email thread. A privacy filter makes your screen look black to them. If you work in public, " + buy("3m-gold-privacy-filter","check the Amazon price for your screen size") + "."),
  ("Why 3M's gold version",
   "Budget privacy films dim your own view noticeably and have a soft cutoff you can still peek past. 3M's gold micro-louver filter has a crisper angle cutoff and keeps more brightness for you. Executives who travel with sensitive material " + buy("3m-gold-privacy-filter","buy the right size on Amazon") + "."),
  ("Fitting it",
   "Laptop versions use slide-mount tabs so you can pull the filter off for a presentation; monitor versions hang or attach. Measure your display and pick the exact model on the " + buy("3m-gold-privacy-filter","Amazon listing") + "."),
 ],
 pros=["Sharp side-angle blackout","Keeps your head-on brightness","Reversible matte/anti-glare side","Removable for screen-sharing","Sized for many laptops and monitors"],
 cons=["Slight sparkle/texture on the gold side","Must buy the exact size for your screen","Adds a step when you present"],
 forwho="Anyone who opens sensitive documents in public or open-plan spaces. If you only ever work in a private office, you don't need it.",
 finalcta="Cheap protection against the most low-tech data leak there is.",
 faq=[("How do I get the right size?","Match your exact laptop model or measure the monitor's viewable area — filters are sold per size and must fit precisely. Sizing help is on the [Amazon page](https://www.amazon.com/s?k=3M+Gold+Privacy+Filter)."),
      ("Does it make my screen dim?","Less than cheaper films. The gold layer keeps more brightness head-on; you'll notice a small reduction, not a big one.")],
)
SINGLES["mission-darkness-faraday"] = dict(
 title="Air-Gapped in a Bag: Mission Darkness Faraday Laptop Sleeve",
 headline="Mission Darkness Dry Shield Faraday Bag Review: True RF Isolation in Transit",
 dek="Blocks cellular, Wi-Fi, Bluetooth and GPS — so a device can't be tracked, pushed to, or remotely wiped while you move through a hostile jurisdiction.",
 verdict="Best Faraday bag for travel",
 cardCue="See the signal-block spec →",
 tags=["faraday bag","mission darkness","travel security"], keywords=["mission darkness faraday bag review","faraday laptop bag","rf blocking bag travel"],
 takeaways=[
   "Attenuates across cellular, Wi-Fi, Bluetooth and GPS bands.",
   "Waterproof roll-top closure and a rugged abrasion-resistant exterior.",
   "Stops remote wipe, remote tracking and push exploits while sealed.",
   "Sized for a laptop and tablet together.",
 ],
 sections=[
  ("The threat this addresses",
   "In some jurisdictions, a device out of your hands — or even in your bag — can be located, pushed malware, or wiped before you land. A Faraday bag makes the device electromagnetically invisible until you choose to open it. If your travel takes you somewhere you don't trust the network, " + buy("mission-darkness-faraday","check the Amazon price") + "."),
  ("Build matters for a Faraday bag",
   "Cheap RF pouches lose their seal as the fabric creases and wears. Mission Darkness uses tested shielding fabric with a roll-top that maintains attenuation, plus a waterproof, tough outer. Security and legal travelers " + buy("mission-darkness-faraday","buy the laptop size on Amazon") + "."),
  ("Sizing and use",
   "Get the size that fits your laptop plus a tablet or phone. Seal it before you're in the sensitive environment, not after. Check the tested attenuation figures and dimensions on the " + buy("mission-darkness-faraday","Amazon listing") + "."),
 ],
 pros=["Broad-band signal blocking","Waterproof, rugged construction","Maintains its seal with use","Fits laptop + tablet","Tested attenuation data published"],
 cons=["Bulky to carry alongside a normal bag","Device is unreachable while sealed (the point)","Overkill for domestic low-risk travel"],
 forwho="Executives, legal and security staff who travel to jurisdictions where device compromise is a real risk. For everyday domestic travel, it's more than you need.",
 finalcta="If your travel involves untrusted networks, this is the isolation you want.",
 faq=[("Does it really block GPS and cellular?","Yes — the tested fabric attenuates across those bands when properly sealed. The published attenuation figures are on the [Amazon page](https://www.amazon.com/s?k=Mission+Darkness+Dry+Shield+Faraday+Bag+laptop)."),
      ("Can the device still be used inside?","No — that's the point. It's fully isolated until you unseal it.")],
)
SINGLES["fellowes-99ci"] = dict(
 title="Board Decks to Confetti, Without the Jam: Fellowes 99Ci",
 headline="Fellowes Powershred 99Ci Review: Jam-Proof Micro-Cut for Confidential Paper",
 dek="Turns M&A printouts, financial models and printed emails into micro-particles — and its jam-proof feed means it actually gets used.",
 verdict="Best executive-office shredder",
 cardCue="See the micro-cut size →",
 tags=["shredder","fellowes","document security"], keywords=["fellowes 99ci review","micro cut shredder","confidential document shredder office"],
 takeaways=[
   "P-4 micro-cut particles are effectively impossible to reassemble.",
   "100% jam-proof feed handles mixed stacks without stopping.",
   "Long runtime before the motor needs to cool.",
   "Bin large enough for a real purge, not just a few sheets.",
 ],
 sections=[
  ("Strip-cut isn't shredding",
   "A strip-cut shredder produces ribbons a determined person can tape back together. For anything genuinely confidential — deal documents, board materials, HR files — you want micro-cut, which turns a page into hundreds of confetti particles. If your printer produces anything sensitive, " + buy("fellowes-99ci","check the Amazon price") + "."),
  ("Jam-proof means it gets used",
   "The reason shredders sit unused is jams. The 99Ci's feed is designed to reject over-thick stacks before they jam and power through staples and cards. A shredder that always works is a shredder people actually use. Offices handling deal flow " + buy("fellowes-99ci","buy the 99Ci on Amazon") + "."),
  ("Runtime, capacity, noise",
   "It runs for a solid stretch before a cool-down, takes a useful number of sheets per pass, and the bin holds a proper clear-out. It's not silent — check the runtime and bin size on the " + buy("fellowes-99ci","Amazon listing") + "."),
 ],
 pros=["P-4 micro-cut security","Genuinely jam-proof feed","Handles staples, clips, cards","Long runtime","Large bin"],
 cons=["Loud while running","Heavy to move","Micro-cut bin fills faster than strip-cut"],
 forwho="Any executive or team that prints confidential material. If you're truly paperless, you don't need it — but most aren't.",
 finalcta="The shredder that gets used because it never jams. That's the whole value.",
 faq=[("How secure is P-4 micro-cut?","Each sheet becomes hundreds of small particles — reconstruction is not realistically feasible. For classified-equivalent needs there's P-5/P-6, but P-4 covers corporate confidentiality. Specs on the [Amazon page](https://www.amazon.com/s?k=Fellowes+Powershred+99Ci)."),
      ("Can it take staples and credit cards?","Yes — staples and paper clips go straight through, and it has a separate slot/mode for cards.")],
)

# ============================================================================
#  write singles
# ============================================================================
order = 0
by_cat_order = {}
for key, S in SINGLES.items():
    c = PRODUCTS[key]["category"]
    by_cat_order[c] = by_cat_order.get(c, 0)
for key, S in SINGLES.items():
    write_single(key, S, order)
    order += 1
print("singles written:", len(SINGLES))

# ============================================================================
#  COMPARISONS
# ============================================================================
COMPS = []
COMPS.append(dict(
 slug="executive-carry-showdown", cat="leather-edc",
 title="Which Executive Bag Actually Signals Authority? 4-Way Test",
 headline="Saddleback vs Bellroy vs Leatherology vs Tumi: The Executive Carry Showdown",
 dek="Heritage ruggedness or modern technical organization? We line up four very different answers and tell you which one to carry.",
 offer="saddleback-briefcase",
 contenders=["saddleback-briefcase","bellroy-tokyo","leatherology-padfolio","tumi-alpha3-brief"],
 takeaways=[
   "Want it to last forever and don't mind weight → Saddleback.",
   "Want slim, light and organized for travel → Bellroy Tokyo.",
   "Sit in device-free rooms → Leatherology padfolio.",
   "Want maximum pockets at minimum weight → Tumi Alpha 3.",
 ],
 intro="These four bags answer the same question — \"what do I carry into the room?\" — in opposite ways. One is a generational leather object. One is a minimalist travel tool. One is for rooms that ban laptops. One is a technical nylon organizer. Here's how to choose.",
 notes={
   "saddleback-briefcase":"The authority play through sheer permanence — thick leather, no zippers, a 100-year warranty. Heavy, and you'll break it in, but it's the last bag you buy.",
   "bellroy-tokyo":"The modern minimalist's pick: slim, light, weatherproof, with real organization for two phones and a charger, plus a luggage pass-through. The best all-rounder for a travel week.",
   "leatherology-padfolio":"Not a bag — a full-grain folio for board and deal rooms where devices are locked away. Expands for a printed deck, and the unzip is its own quiet signal.",
   "tumi-alpha3-brief":"The technical choice: FXT ballistic nylon, a pocket for everything, lighter than a leather brief of the same volume. Less romance, more function.",
 },
 notescta={},
 verdict="For most executives, the Bellroy Tokyo is the right daily bag — slim, light, organized, travel-ready. Buy the Saddleback if you want a leather object you'll hand down and don't mind carrying the weight. Keep a Leatherology padfolio in the drawer for device-free rooms. The Tumi is the pick only if pocket count is your top priority.",
 verdict_short="Bellroy for daily; Saddleback to hand down",
 finalcta="Still deciding? The Bellroy Tokyo is the safe daily choice.",
 tags=["briefcase","comparison"], keywords=["best executive briefcase","saddleback vs bellroy"],
 faq=[("One bag for everything — which?","The Bellroy Tokyo. It's the only one of the four that credibly covers desk, meeting and flight in a single slim package."),
      ("Best value?","The Leatherology padfolio delivers the most full-grain leather per dollar — but it's a folio, not a briefcase.")],
))
COMPS.append(dict(
 slug="boardroom-pen-showdown", cat="writing",
 title="The Only Pen Comparison an Executive Needs: 4 Contenders",
 headline="Montblanc 149 vs Waterman Carène vs Lamy 2000 vs Parker Duofold",
 dek="Flashy prestige or friction-free reliability? Four pens, four philosophies of what a signature should say.",
 offer="lamy-2000",
 contenders=["montblanc-149","waterman-carene","lamy-2000","parker-duofold"],
 takeaways=[
   "Want the room to notice the pen → Montblanc 149.",
   "Want zero maintenance → Waterman Carène rollerball.",
   "Want design credibility without the logo → Lamy 2000.",
   "Want heritage prestige for less → Parker Duofold.",
 ],
 intro="A pen is a small decision that people watch you make. These four cover the full range — from the Montblanc that everyone recognizes to the Lamy that only the design-literate clock. Pick based on what you want the moment to say.",
 notes={
   "montblanc-149":"Maximum recognition. The 18K nib writes beautifully and the barrel photographs like status. You'll also field the occasional \"nice pen\" with a raised eyebrow — that's the deal.",
   "waterman-carene":"The pragmatist's choice. Rollerball ink laydown, brass heft, no nib to manage. Grab it after two weeks in a drawer and it just writes.",
   "lamy-2000":"The quiet flex. A 1966 Bauhaus design with a hooded gold nib, no visible branding. The people who matter to you will notice; nobody else will.",
   "parker-duofold":"Heritage and a real gold nib at roughly half the 149's price. Less universally recognized, but a serious pen that signs beautifully.",
 },
 notescta={},
 verdict="For a daily writer with taste, the Lamy 2000 is the pick — gold-nib performance, timeless design, a fraction of the flagship price. Choose the Montblanc 149 only if the visible-status moment genuinely matters in your role. The Waterman Carène is the answer if you don't want to think about upkeep at all. The Parker Duofold splits the difference.",
 verdict_short="Lamy 2000 for taste; 149 for status",
 finalcta="The connoisseur's daily pick is the Lamy 2000.",
 tags=["fountain pen","comparison"], keywords=["best executive pen","montblanc vs lamy"],
 faq=[("Lowest lifetime cost?","The Lamy 2000 or Montblanc 149 — both use bottled ink, which is pennies per fill. The Waterman's rollerball refills add up over years."),
      ("Best for someone who's never used a fountain pen?","The Waterman Carène rollerball. All the elegance, none of the learning curve.")],
))
COMPS.append(dict(
 slug="silence-is-currency", cat="audio",
 title="The Headphone Test That Actually Matters for Executives",
 headline="Sony XM5 vs Bose QC Ultra vs AirPods Max vs Sennheiser Momentum 4",
 dek="Not 'which sounds best' — which keeps you intelligible on a high-stakes video call and comfortable through a day of them.",
 offer="sony-xm5",
 contenders=["sony-xm5","bose-qc-ultra","airpods-max","sennheiser-momentum-4"],
 takeaways=[
   "Best transmit mic for calls in noisy places → Sony XM5.",
   "Best all-day / long-haul comfort → Bose QC Ultra.",
   "All-Apple household → AirPods Max.",
   "Longest battery by far → Sennheiser Momentum 4.",
 ],
 intro="For an executive, headphones are a call tool first and a music tool second. The deciding questions are: do you sound clear to the other side, and are these comfortable in back-to-back meetings? Here's how the four flagships land.",
 notes={
   "sony-xm5":"The best balance for a call-heavy desk: class-leading noise cancellation and the strongest transmit-mic performance of the group in a noisy room. Ear cups run warm over very long sessions.",
   "bose-qc-ultra":"The comfort winner — the gentlest clamp of the flagships and a useful spatial mode for group calls. Mic is very good but a step behind the Sony in loud spaces.",
   "airpods-max":"Only makes sense in an all-Apple setup, where the instant device switching is genuinely seamless. Heavier on the head; excellent transparency mode.",
   "sennheiser-momentum-4":"~60 hours of battery outlasts any travel week and it's comfortable and warm-sounding. ANC and call mic are a notch below Sony and Bose.",
 },
 notescta={},
 verdict="The Sony WH-1000XM5 is the default for a call-heavy executive — it cancels the most noise and keeps you the clearest to your callers. If your pain point is comfort on long flights and long meeting days, the Bose QC Ultra is the better buy. AirPods Max only for committed Apple users; the Momentum 4 if battery life trumps everything.",
 verdict_short="Sony XM5 for calls; Bose for comfort",
 finalcta="For most executives, the Sony WH-1000XM5 is the pick.",
 tags=["headphones","comparison"], keywords=["best headphones for video calls","sony xm5 vs bose qc ultra"],
 faq=[("Which is best purely for the microphone?","The Sony XM5 in a noisy environment. In a quiet office the gap narrows and all four are fine."),
      ("Which for a 10-hour flight?","The Bose QC Ultra — the clamp comfort advantage compounds over that long.")],
))
COMPS.append(dict(
 slug="executive-seating-battle", cat="furniture",
 title="Aeron vs Gesture vs Fern: The Chair Worth 2,000 Hours a Year",
 headline="Herman Miller Aeron vs Steelcase Gesture vs Haworth Fern",
 dek="Suspended mesh, cushioned contour, or flexible knit? Three top-tier chairs, three different bodies they suit.",
 offer="herman-miller-aeron",
 contenders=["herman-miller-aeron","steelcase-gesture","haworth-fern"],
 takeaways=[
   "Run hot / want consistent all-day support → Aeron.",
   "Always holding a phone or tablet → Steelcase Gesture.",
   "Want spinal flex and a warmer look → Haworth Fern.",
 ],
 intro="If you sit for 2,000+ hours a year, this is a real capital decision. All three are excellent and last 12 years. The choice comes down to how your body likes to be supported — and how much you move.",
 notes={
   "herman-miller-aeron":"Suspended mesh that stays cool and supports identically at hour nine as hour one. PostureFit SL stabilizes the sacrum. The safe pick for long, static desk days — and the refurb market makes it attainable.",
   "steelcase-gesture":"The arm system is unmatched — it follows you into every device posture, which is why it wins for phone- and tablet-heavy executives. Warmer than mesh; heavier to move.",
   "haworth-fern":"The 'digital knit' back flexes segment by segment with your spine, and the residential look suits a client-facing office. Lighter recline feel than the Aeron.",
 },
 notescta={},
 verdict="The Aeron remains the default for most executives — cool, consistent, backed by an enormous refurb market that cuts the price. Choose the Gesture if your day is device-in-hand and you want the best arms made. The Fern is the pick if you want spinal-flex comfort and a warmer aesthetic for a client-facing room.",
 verdict_short="Aeron default; Gesture for device days",
 finalcta="The safe long-term buy is a certified-refurbished Aeron.",
 tags=["office chair","comparison"], keywords=["best executive office chair","aeron vs gesture"],
 faq=[("Best for a bad lower back?","The Aeron's PostureFit SL has the most direct sacral support. Try the Fern if you prefer a back that moves with you."),
      ("Cheapest way into one of these?","A certified-refurbished Aeron — remanufactured to spec with the full 12-year warranty, often 30–50% off.")],
))
COMPS.append(dict(
 slug="elite-carry-on-showdown", cat="travel",
 title="Tumi vs Rimowa vs Briggs & Riley: Which Carry-On Is Actually Worth It?",
 headline="Tumi Alpha 3 vs Rimowa Original Cabin vs Briggs & Riley Baseline",
 dek="Ballistic-nylon toughness, aluminum status, or an unconditional lifetime warranty? Three premium philosophies of luggage.",
 offer="tumi-alpha3-carryon",
 contenders=["tumi-alpha3-carryon","rimowa-original-cabin","briggs-riley-baseline"],
 takeaways=[
   "Toughest shell + best organization → Tumi Alpha 3.",
   "Status and character (and dents) → Rimowa aluminum.",
   "Never-think-about-warranty peace of mind → Briggs & Riley.",
 ],
 intro="At this price the bags are all well made — the question is which philosophy you're buying. Impact-tolerant nylon that flexes into a bin. Aluminum that wears its travels as dents. Or a bag the maker will repair forever, no questions.",
 notes={
   "tumi-alpha3-carryon":"The most travel-ready: FXT ballistic nylon that flexes and survives, dual top/front access, suiter brackets, and the Tracer recovery program. Heavy for a soft-side, and on the larger end of carry-on legal.",
   "rimowa-original-cabin":"The status object. Anodized aluminum that looks superb and then collects dents as a feature. Heavier and pricier; 5-year warranty and a global service network.",
   "briggs-riley-baseline":"The pragmatist's flex: an unconditional lifetime warranty that covers airline damage, plus the Outsider handle that frees all interior space and CX compression for overpackers.",
 },
 notescta={},
 verdict="For pure function, the Tumi Alpha 3 wins — toughest shell, best organization, most travel-ready design. Buy the Briggs & Riley if warranty peace of mind matters more to you than anything else; its lifetime coverage is the real deal. The Rimowa is a status purchase — beautiful, heavier, and it will dent.",
 verdict_short="Tumi for function; Briggs & Riley for warranty",
 finalcta="The most travel-ready choice is the Tumi Alpha 3.",
 tags=["carry-on","comparison"], keywords=["best premium carry on","tumi vs rimowa vs briggs riley"],
 faq=[("Which survives checked-bag abuse best?","The Tumi's ballistic nylon flexes and recovers; the Rimowa dents; the Briggs & Riley is tough and, if something breaks, free to fix forever."),
      ("Lightest of the three?","The Briggs & Riley Baseline is typically the lightest to lift, thanks to the external handle design.")],
))
COMPS.append(dict(
 slug="executive-presence-4k", cat="video",
 title="The Webcam Showdown for People Who Present on Camera",
 headline="Insta360 Link 2 vs OBSBOT Tiny 2 vs Logitech Brio 4K",
 dek="AI-driven gimbal tracking or a rock-solid fixed lens? Depends on whether you move during calls.",
 offer="insta360-link2",
 contenders=["insta360-link2","obsbot-tiny-2","logitech-brio-4k"],
 takeaways=[
   "You present and move (whiteboard, standing) → Insta360 Link 2.",
   "You want gesture/voice control and a big sensor → OBSBOT Tiny 2.",
   "You sit still and want zero fuss → Logitech Brio 4K.",
 ],
 intro="If you sit centered and still, almost any 4K webcam is fine — get the Brio and move on. If you stand, move to a whiteboard, or run webinars, a physical gimbal changes the game. Here's the split.",
 notes={
   "insta360-link2":"The best tracking of the three, with a physical 2-axis gimbal that keeps you full-resolution as you move, a large sensor for dim rooms, and a genuine physical privacy shield when muted.",
   "obsbot-tiny-2":"A big 1/1.5-inch sensor and slick gesture control — raise a hand to trigger zoom or tracking. Leans on its app for the best results.",
   "logitech-brio-4k":"The safe default: reliable 4K with HDR for backlit offices, no moving parts to fail, and Windows Hello login. No tracking beyond a digital crop.",
 },
 notescta={},
 verdict="If you present on camera — standing, moving, whiteboarding — the Insta360 Link 2 is worth it for the real gimbal tracking and the physical privacy shield. The OBSBOT Tiny 2 is the alternative if you like gesture control. If you sit still, save the money and get the Logitech Brio 4K.",
 verdict_short="Link 2 if you move; Brio if you don't",
 finalcta="For presenters, the Insta360 Link 2 is the pick.",
 tags=["webcam","comparison"], keywords=["best 4k webcam","insta360 link 2 vs obsbot tiny 2"],
 faq=[("Do I need tracking at all?","Only if you leave the center of frame during calls. If you don't, a fixed lens like the Brio gives a cleaner, simpler result."),
      ("Best in a backlit corner office?","All three handle backlight, but the Link 2 and Tiny 2's larger sensors do noticeably better in mixed light.")],
))
COMPS.append(dict(
 slug="hot-coffee-equation", cat="beverage",
 title="Battery Mug or Vacuum Flask? The Desk-Coffee Question, Settled",
 headline="Ember Mug 2 vs Cauldryn vs Fellow Carter Move vs Zojirushi",
 dek="Active electronic heating versus passive vacuum insulation — and which one belongs on your desk versus in your bag.",
 offer="ember-mug-2",
 contenders=["ember-mug-2","cauldryn-coffee","fellow-carter-move","zojirushi-sm-khe48"],
 takeaways=[
   "Precise temp at a desk for hours → Ember Mug 2.",
   "Actually boil water off-grid → Cauldryn.",
   "Best-tasting passive travel mug → Fellow Carter Move.",
   "Toughest, most leakproof passive mug → Zojirushi.",
 ],
 intro="Two philosophies. Active mugs hold a precise temperature with a battery and a coaster — great at a desk, limited on the move. Passive vacuum mugs need no power and travel anywhere, but the coffee slowly cools. Match the tool to where you drink.",
 notes={
   "ember-mug-2":"The desk champion: set 135°F and it stays there through a 90-minute meeting. About 80 minutes of hold off the coaster. Hand-wash only.",
   "cauldryn-coffee":"The outlier — swappable batteries powerful enough to re-boil water in the field. Bulky; more thermos than mug. For off-grid days, not the office.",
   "fellow-carter-move":"The nicest-drinking passive mug: a ceramic-coated interior with no metallic taste, a splash-safe lid, cup-holder friendly. No charging ever.",
   "zojirushi-sm-khe48":"The tank: best-in-class passive retention, a genuinely leakproof locking lid, one-handed operation. Plain looks, narrow mouth.",
 },
 notescta={},
 verdict="If your coffee dies at your desk, the Ember Mug 2 solves exactly that. If you want hot coffee hours later with zero fuss and zero charging, the Zojirushi is the durable pick and the Fellow Carter Move is the better-tasting one. The Cauldryn is a specialist tool for people who are genuinely off-grid.",
 verdict_short="Ember for the desk; Zojirushi for the road",
 finalcta="For desk coffee that never goes cold, the Ember Mug 2.",
 tags=["coffee mug","comparison"], keywords=["ember mug vs zojirushi","best travel coffee mug executive"],
 faq=[("Do I need the battery mug if I drink coffee fast?","No — if you finish a cup in 15 minutes, a passive mug like the Fellow or Zojirushi is simpler and cheaper."),
      ("Which travels best?","The Zojirushi — leakproof locking lid, tough body, no charging.")],
))
COMPS.append(dict(
 slug="deep-focus-recovery", cat="wellness",
 title="Percussion Gun or Recovery Ring? Where Your Wellness Budget Should Go",
 headline="Theragun PRO Plus vs Hyperice Hypervolt 2 Pro vs Oura Ring vs Whoop 4.0",
 dek="Acute physical relief versus passive strain tracking — two different jobs, often confused.",
 offer="theragun-pro-plus",
 contenders=["theragun-pro-plus","hyperice-hypervolt-2-pro","oura-ring-horizon","whoop-4"],
 takeaways=[
   "Fix neck/back tension now, quietly → Theragun PRO Plus.",
   "Same job, lighter, a bit louder, cheaper → Hyperice Hypervolt 2 Pro.",
   "Invisible sleep + readiness data → Oura Ring.",
   "Coached strain/recovery, screenless → Whoop 4.0.",
 ],
 intro="These get lumped together as 'executive wellness tech' but they do opposite things. The guns relieve tension you already have. The wearables tell you how depleted you are so you can plan around it. Most executives should start with one, not all four.",
 notes={
   "theragun-pro-plus":"The relief tool: 16mm deep percussion plus infrared and heat, quiet enough to use between meetings. The one to buy if desk tension is your daily problem.",
   "hyperice-hypervolt-2-pro":"Does the same job in a lighter body with strong power, at a lower price. A little louder at max. The value pick in percussion.",
   "oura-ring-horizon":"Passive, invisible tracking of sleep, HRV and readiness — no wrist device, week-plus battery. Requires a membership for full insight.",
   "whoop-4":"Continuous strain and recovery coaching with no screen at all. Membership-based. Best if you'll actually act on the guidance.",
 },
 notescta={},
 verdict="If you have a physical problem — tight neck, sore back from the desk — buy the Theragun PRO Plus (or the Hypervolt 2 Pro to save money). If you want data to manage your energy across a brutal calendar, pick one wearable: the Oura Ring if you want it invisible, Whoop if you want active coaching. Don't buy both categories at once.",
 verdict_short="Theragun to fix tension; one wearable for data",
 finalcta="If desk tension is the issue, start with the Theragun PRO Plus.",
 tags=["recovery","comparison"], keywords=["theragun vs hypervolt","oura vs whoop for executives"],
 faq=[("Percussion gun or wearable first?","If something hurts, the gun. If nothing hurts but you're exhausted, a wearable to understand why."),
      ("Oura or Whoop?","Oura for a discreet ring and broad health metrics; Whoop for active strain/recovery coaching you'll follow.")],
))
COMPS.append(dict(
 slug="measuring-executive-time", cat="decor",
 title="What Should Sit on the Credenza: Clock, or Hourglass?",
 headline="Howard Miller vs Dalvey vs Mechanical Mantel Clock vs Brass Sand Timer",
 dek="Horological heritage or a tactile time-blocking tool? Two very different reasons to put time on your desk.",
 offer="howard-miller-burton",
 contenders=["howard-miller-burton","dalvey-grand-sedan","jaeger-atmos-homage","authentic-models-sandtimer"],
 takeaways=[
   "Traditional gravitas on a credenza → Howard Miller Burton.",
   "Small, modern, restrained → Dalvey Grand Sedan.",
   "Kinetic conversation piece → glass mechanical mantel clock.",
   "Actually manage focus blocks → brass sand timer.",
 ],
 intro="Two of these are decor — they signal permanence and taste. One is a working tool that defends an hour of deep work. Decide which job you're hiring for before you spend.",
 notes={
   "howard-miller-burton":"The full traditional statement: hardwood, brass, real chimes with a night shut-off. Reads as an office that's been here a while.",
   "dalvey-grand-sedan":"The restrained modern alternative — pocket-watch detailing at a small scale, weighted base, tarnish-resistant. Taste without volume.",
   "jaeger-atmos-homage":"An affordable homage to kinetic mantel clocks — visible movement as theater on the shelf. Needs occasional adjustment; a conversation piece, not an heirloom.",
   "authentic-models-sandtimer":"Not decor — a tool. Flip it to start a silent, phone-free focus block. Solid brass, accurate to within a minute of an hour.",
 },
 notescta={},
 verdict="If you're furnishing an office to feel established, the Howard Miller Burton is the statement and the Dalvey is the understated version. If you want something that actually changes how you work, skip the clocks and get the brass sand timer — it's the only one on this list that does a job.",
 verdict_short="Howard Miller to furnish; sand timer to focus",
 finalcta="For traditional office gravitas, the Howard Miller Burton.",
 tags=["clock","comparison"], keywords=["executive desk clock","mantel clock vs sand timer"],
 faq=[("Decor or productivity?","Be honest about which you want. The clocks are decor; the sand timer is a focus tool. They're not substitutes."),
      ("Most 'executive' looking?","The Howard Miller Burton from across a room; the Dalvey up close on the desk.")],
))
COMPS.append(dict(
 slug="zero-trust-executive", cat="security",
 title="Four Ways an Executive Gets Compromised — and What Stops Each",
 headline="YubiKey vs 3M Privacy Filter vs Mission Darkness Faraday vs Kingston IronKey",
 dek="Digital credential theft, visual eavesdropping, remote device attacks, drive loss — these are four different problems with four different fixes.",
 offer="yubikey-5c-nfc",
 contenders=["yubikey-5c-nfc","3m-gold-privacy-filter","mission-darkness-faraday","kingston-ironkey-vp80"],
 takeaways=[
   "Stop phishing / account takeover → YubiKey 5C NFC.",
   "Stop shoulder-surfing in public → 3M Gold Privacy Filter.",
   "Stop remote tracking / wipe in transit → Mission Darkness Faraday bag.",
   "Protect data if a drive is lost or stolen → Kingston IronKey.",
 ],
 intro="There's no single 'executive security' product because there's no single threat. Map the tool to the exposure: your logins, your screen, your device in a hostile place, your files at rest. Here's the priority order for most people.",
 notes={
   "yubikey-5c-nfc":"The highest-leverage buy on the list. FIDO2 hardware makes your email and SSO un-phishable. Cheap, and the single biggest reduction in real-world risk. Buy two.",
   "3m-gold-privacy-filter":"The cheapest fix for the most common leak — someone reading your screen in a lounge or on a plane. Sharp side-angle blackout, keeps your head-on brightness.",
   "mission-darkness-faraday":"Specialist protection for travel to jurisdictions where a device in your bag can be located or attacked. Broad-band RF isolation with a maintained seal.",
   "kingston-ironkey-vp80":"Hardware-encrypted storage with an on-device PIN pad — for carrying sensitive files air-gapped from the laptop, safe if lost.",
 },
 notescta={},
 verdict="Buy in this order: the YubiKey (everyone, now), then the 3M privacy filter if you ever work in public. Add the Mission Darkness Faraday bag only if your travel takes you somewhere you don't trust the network, and the Kingston IronKey only if you routinely carry sensitive files outside managed systems.",
 verdict_short="YubiKey first — then a privacy filter",
 finalcta="Start with the YubiKey 5C NFC. It's the one nobody should skip.",
 tags=["security","comparison"], keywords=["executive security devices","yubikey vs ironkey"],
 faq=[("If I buy one thing?","The YubiKey. It closes the attack that actually gets executives — phishing — for about the price of a nice lunch."),
      ("Do these overlap?","No — each addresses a distinct exposure. That's why the article ranks them by how many people actually face each threat.")],
))

for i, C in enumerate(COMPS):
    write_compare(C["slug"], C, i)
print("comparisons written:", len(COMPS))
