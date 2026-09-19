+++
title = "MCP Server Optimization, the Book"
pageTitle = "MCP Server Optimization, the Book — Findable, Trusted, Easy to Connect"
dek = "For software and AI engineers whose MCP server works but isn't getting found. Make it findable, trusted, and easy to connect."
# Must not be in the future — Hugo silently drops future-dated pages from the build.
date = 2026-09-18
layout = "landing"

# --- the product ------------------------------------------------------------
productName = "MCP Server Optimization, the Book"
asin = "B0HJXTLC9F"
# ONE link drives every button, image and text link on this page. This is an Amazon
# SiteStripe short link, so the affiliate tag is already inside it (it is NOT affected
# by [params].amazonTag in hugo.toml). To use the site-wide tag instead, delete this
# line: links then fall back to https://www.amazon.com/dp/<asin>?tag=<amazonTag>.
affiliateUrl = "https://amzn.to/3V05Ir2"

# --- the image (also used as og:image) --------------------------------------
image = "/img/mcp-server-optimization-book.webp"
imageAlt = "Cover graphic for MCP Server Optimization, the Book, for software and AI engineers: “Your MCP server works. Agents still can't find it.” Findable · Trusted · Easy to connect."
imageWidth = 1000
imageHeight = 1000

# --- hero copy --------------------------------------------------------------
eyebrow = "For software & AI engineers"
headline = "Make your MCP server easy for agents to find, trust, and connect to."
subhead = "Your server works. MCP Server Optimization, the Book is about what comes next: getting it found, trusted, and easy to connect to."
ctaText = "Get the Book on Amazon"
ctaNote = "Opens Amazon in a new tab · same price through our link"

# --- problem + pillars ------------------------------------------------------
problemTitle = "Working is not the same as discoverable"
problemBody = "You've done the hard part — the server runs and the tools respond. But agents, and the people who configure them, can only use what they can find, vet, and connect to. When any one of those steps fails, a good server sits unused."
pillars = [
  { icon = "search", title = "Findable", text = "If agents and developers can't discover your server, nothing else you built matters. How you name and describe it decides whether it's ever considered." },
  { icon = "shield", title = "Trusted", text = "Nobody wires an unfamiliar server into their workflow on faith. Clear signals of quality, safety, and upkeep turn a maybe into a yes." },
  { icon = "bolt", title = "Easy to connect", text = "Every extra setup step loses someone who was already interested. The easier it is to connect, the more discovery turns into real use." },
]
inlineLead = "Findable, trusted, easy to connect — that's the promise on the cover of MCP Server Optimization."
inlineCta = "See the book on Amazon"

# --- audience ---------------------------------------------------------------
audienceTitle = "Who it's for"
audience = [
  "Software and AI engineers who've built an MCP server and want more people — and agents — actually using it.",
  "Teams shipping an MCP server alongside an API, product, or platform.",
  "Anyone whose server works fine in a demo but isn't getting adopted in the wild.",
]

# --- FAQ (kept to things that are true regardless of what's in the book) -----
faqTitle = "Quick answers"
faq = [
  { q = "Where does the button take me?", a = "Straight to the book's page on Amazon, where you can see the current price, available formats, and buying options. There's nothing to sign up for here." },
  { q = "Do I pay more by using your link?", a = "No — the price is the same. As an Amazon Associate I earn from qualifying purchases, so if you buy, a small commission comes to us at no cost to you." },
  { q = "Where can I see what's inside?", a = "The book's Amazon page has the full description and details, and Amazon's preview (where offered) lets you look before you buy." },
  { q = "Who is the book for?", a = "Software and AI engineers who've built, or are building, an MCP server and want it to be found, trusted, and easy to connect to." },
]

# --- bottom of page ---------------------------------------------------------
finalTitle = "Your MCP server works. Let agents find it."
finalText = "Findable · Trusted · Easy to connect — one click to see the book, the current price, and the details on Amazon."
stickyTagline = "Findable · Trusted · Easy to connect"

# --- how this page is promoted elsewhere on the site -------------------------
# The homepage "This month's picks" card and the top-nav link both go STRAIGHT to
# affiliateUrl above (not to this page) and read their name/image/link from this
# front matter, so changing the link here updates all of them.
pickTagline = "Your MCP server works. Agents still can't find it."
pickImagePosition = "50% 55%"   # keeps the hook + book title inside the 16:10 card crop
pickHideCue = true              # on touch screens the "…on Amazon →" pill is always shown and would cover the
                                # book title baked into the cover graphic; the button right below says the same
+++
