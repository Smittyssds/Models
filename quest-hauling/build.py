#!/usr/bin/env python3
"""Static site generator for Quest Hauling (questhauling.com).

Run `python3 build.py` and upload the contents of ./public to any static host
(Netlify, Cloudflare Pages, GitHub Pages, Vercel...). Edit the BUSINESS block
below to change the phone, domain, price, etc. on every page at once.
"""
import html
import json
import os
import shutil
from datetime import date

# ---------------------------------------------------------------------------
# Business details. Change these and rebuild.
# ---------------------------------------------------------------------------
BUSINESS = {
    "name": "Quest Hauling",
    "domain": "https://www.questhauling.com",  # TODO: replace with the real domain
    "phone": "714-735-4664",
    "email": "questhauling1@gmail.com",
    "city": "Huntington Beach",
    "region": "CA",
    "price": 550,
    "days": 7,
    "tons": 1.5,
    "size": 16,
    # Form handler. FormSubmit emails each submission to the address below;
    # the first submission sends a one-time activation email to that inbox.
    "form_action": "https://formsubmit.co/questhauling1@gmail.com",
}

B = BUSINESS
PHONE_HREF = "tel:+1" + B["phone"].replace("-", "")
TODAY = date.today().isoformat()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

# ---------------------------------------------------------------------------
# Service areas. Each city gets its own landing page with local details so the
# pages are genuinely different, not copy-paste clones.
# ---------------------------------------------------------------------------
CITIES = [
    {
        "slug": "huntington-beach", "name": "Huntington Beach", "county": "Orange County",
        "zips": ["92646", "92647", "92648", "92649"],
        "hoods": ["Huntington Harbour", "Downtown & Main Street", "Seacliff", "Edwards Hill", "Huntington Continental", "Westside / Bolsa Chica"],
        "intro": "Huntington Beach is our home base, so Surf City customers get our fastest delivery windows. From garage cleanouts off Beach Boulevard to kitchen remodels in Huntington Harbour, a 16-yard roll-off handles most HB projects in a single drop.",
        "tip": "Many Huntington Beach homes near the coast have short driveways or alley-loaded garages. Tell us about tight access when you book and we'll plan placement so the bin doesn't block your neighbors.",
        "nearby": ["fountain-valley", "costa-mesa", "newport-beach", "long-beach"],
    },
    {
        "slug": "newport-beach", "name": "Newport Beach", "county": "Orange County",
        "zips": ["92625", "92657", "92660", "92661", "92662", "92663"],
        "hoods": ["Balboa Peninsula", "Corona del Mar", "Newport Coast", "Eastbluff", "Westcliff", "Newport Heights"],
        "intro": "Newport Beach remodels and estate cleanouts generate a lot of debris in a short time. Our 16-yard dumpster is sized for kitchen and bath renovations, flooring tear-outs and whole-home cleanouts from Balboa to Newport Coast.",
        "tip": "Narrow streets and alley access are common on the Peninsula and in Corona del Mar. Send a photo of your driveway when you book so we can confirm the best spot for the bin.",
        "nearby": ["costa-mesa", "huntington-beach", "irvine", "fountain-valley"],
    },
    {
        "slug": "costa-mesa", "name": "Costa Mesa", "county": "Orange County",
        "zips": ["92626", "92627"],
        "hoods": ["Eastside", "Westside", "Mesa Verde", "College Park", "Mesa del Mar", "South Coast Metro"],
        "intro": "Costa Mesa homeowners and contractors use our 16-yard roll-off for Eastside remodels, Mesa Verde yard makeovers and rental turnovers. One flat price covers delivery, a full week on site, pickup and disposal of up to 1.5 tons.",
        "tip": "If your project is a rental turnover or move-out, book the bin a day before the cleanout crew arrives so it's ready when the work starts.",
        "nearby": ["newport-beach", "fountain-valley", "huntington-beach", "santa-ana"],
    },
    {
        "slug": "fountain-valley", "name": "Fountain Valley", "county": "Orange County",
        "zips": ["92708"],
        "hoods": ["Green Valley", "Mile Square area", "Harbor Boulevard corridor", "Talbert area", "Warner & Brookhurst area"],
        "intro": "Fountain Valley sits right next door to our Huntington Beach yard, which means quick drop-offs for garage cleanouts, backyard projects and remodels across all of 92708.",
        "tip": "Most Fountain Valley homes have wide driveways that fit a 16-yard bin easily. Lay down a couple of boards where the rails will sit if you want extra protection for your concrete.",
        "nearby": ["huntington-beach", "costa-mesa", "santa-ana", "irvine"],
    },
    {
        "slug": "irvine", "name": "Irvine", "county": "Orange County",
        "zips": ["92602", "92603", "92604", "92606", "92612", "92614", "92617", "92618", "92620"],
        "hoods": ["Woodbridge", "Northwood", "Turtle Rock", "University Park", "Great Park", "Quail Hill"],
        "intro": "From Woodbridge to the Great Park neighborhoods, Irvine homeowners rent our 16-yard dumpster for remodels, move-outs and big decluttering projects. You get a full week to fill it, with delivery and pickup included.",
        "tip": "Most Irvine neighborhoods have an HOA. Check your HOA's rules on driveway containers before delivery day, and let us know about any placement or time-of-day limits.",
        "nearby": ["costa-mesa", "newport-beach", "santa-ana", "fountain-valley"],
    },
    {
        "slug": "santa-ana", "name": "Santa Ana", "county": "Orange County",
        "zips": ["92701", "92703", "92704", "92705", "92706", "92707"],
        "hoods": ["Floral Park", "French Park", "Downtown Santa Ana", "Riverview", "Washington Square", "Morrison Park"],
        "intro": "Santa Ana's historic homes in Floral Park and French Park often mean plaster, lath and old flooring during a remodel. A 16-yard roll-off gives you room for renovation debris without paying for a bigger bin than you need.",
        "tip": "Plaster, tile and other heavy remodel debris add up fast. If your project is mostly heavy material, ask us how much will fit within the included 1.5 tons before you start loading.",
        "nearby": ["fountain-valley", "costa-mesa", "irvine", "anaheim"],
    },
    {
        "slug": "anaheim", "name": "Anaheim", "county": "Orange County",
        "zips": ["92801", "92802", "92804", "92805", "92806", "92807", "92808"],
        "hoods": ["Anaheim Hills", "West Anaheim", "The Colony", "Platinum Triangle", "Anaheim Resort area", "Rancho Santa Ana area"],
        "intro": "Anaheim is a big city with every kind of project, from Anaheim Hills landscape overhauls to West Anaheim garage cleanouts. Our 16-yard dumpster covers most of them in one rental at one flat price.",
        "tip": "Hillside driveways in Anaheim Hills can be steep. Let us know the slope when you book so the driver can place the bin on the flattest, safest section.",
        "nearby": ["santa-ana", "fountain-valley", "irvine", "long-beach"],
    },
    {
        "slug": "long-beach", "name": "Long Beach", "county": "Los Angeles County", "region": "South LA & South Bay",
        "zips": ["90802", "90803", "90804", "90805", "90806", "90807", "90808", "90810", "90813", "90814", "90815"],
        "hoods": ["Belmont Shore", "Naples", "Bixby Knolls", "Los Altos", "Bluff Park", "California Heights"],
        "intro": "Long Beach sits between our Huntington Beach and Los Angeles yards, so delivery is quick from either one. We deliver 16-yard dumpsters for remodels in Bixby Knolls, cleanouts in Belmont Shore and yard projects in Los Altos.",
        "tip": "Belmont Shore and Naples lots are tight, and many homes rely on alleys. If the bin has to go on the street, check with the City of Long Beach about whether a permit is required for your block.",
        "nearby": ["huntington-beach", "torrance", "fountain-valley", "anaheim"],
    },
    {
        "slug": "los-angeles", "name": "Los Angeles", "county": "Los Angeles County", "region": "Central LA",
        "zips": ["90004", "90005", "90006", "90010", "90019", "90020", "90026", "90027", "90029", "90036", "90039", "90048"],
        "hoods": ["Koreatown", "Mid-City", "Mid-Wilshire", "Hancock Park", "Fairfax", "Silver Lake", "Echo Park", "Los Feliz"],
        "intro": "We deliver 16-yard dumpsters across the City of Los Angeles, from Koreatown apartment turnovers to Silver Lake hillside remodels and Mid-City bungalow renovations. Our Los Angeles yard keeps delivery quick across Central, West and South LA, at the same flat price as everywhere else we serve.",
        "tip": "Driveway placement doesn't need a permit. If the bin has to sit on a public street in the City of Los Angeles, you'll typically need a temporary permit from the city first, so plan for that before delivery day.",
        "nearby": ["hollywood", "downtown-los-angeles", "west-los-angeles", "south-los-angeles"],
    },
    {
        "slug": "hollywood", "name": "Hollywood", "county": "Los Angeles County", "region": "Central LA",
        "zips": ["90028", "90038", "90046", "90068"],
        "hoods": ["Central Hollywood", "Hollywood Hills", "East Hollywood", "Hollywood Dell", "Spaulding Square", "Melrose Hill"],
        "intro": "Hollywood projects range from apartment cleanouts off Sunset to full remodels up in the Hills. Our 16-yard roll-off is compact enough for tight Hollywood lots and big enough for a kitchen or whole-home cleanout.",
        "tip": "Streets in the Hollywood Hills are narrow and winding. Tell us about street width, tight turns and where a truck can turn around so we can confirm access before we roll.",
        "nearby": ["los-angeles", "downtown-los-angeles", "west-los-angeles", "culver-city"],
    },
    {
        "slug": "downtown-los-angeles", "name": "Downtown Los Angeles", "county": "Los Angeles County", "region": "Central LA",
        "zips": ["90012", "90013", "90014", "90015", "90017", "90021", "90071"],
        "hoods": ["Arts District", "Historic Core", "South Park", "Little Tokyo", "Fashion District", "Chinatown"],
        "intro": "In Downtown LA our dumpsters go to loft renovations, tenant improvements, office cleanouts and retail turnovers. One 16-yard bin at a flat price keeps small commercial jobs simple.",
        "tip": "Most DTLA buildings have no driveway. Check with building management about using a loading dock, lot or alley. If the bin has to go on the street, you'll need a city permit first.",
        "nearby": ["los-angeles", "hollywood", "south-los-angeles", "culver-city"],
    },
    {
        "slug": "west-los-angeles", "name": "West Los Angeles", "county": "Los Angeles County", "region": "West LA",
        "zips": ["90024", "90025", "90034", "90035", "90049", "90064", "90066", "90094", "90291"],
        "hoods": ["Westwood", "Brentwood", "Sawtelle", "Palms", "Mar Vista", "Venice", "Rancho Park", "Playa Vista"],
        "intro": "Westside homeowners use our 16-yard dumpster for Mar Vista remodels, Venice cottage renovations, Brentwood estate cleanouts and Palms rental turnovers. Delivery, a full week and pickup are included.",
        "tip": "Venice walk streets and many Westside lots are alley-loaded. If your only access is an alley, mention it when you book so we can plan placement that keeps the alley passable.",
        "nearby": ["santa-monica", "culver-city", "los-angeles", "hollywood"],
    },
    {
        "slug": "santa-monica", "name": "Santa Monica", "county": "Los Angeles County", "region": "West LA",
        "zips": ["90401", "90402", "90403", "90404", "90405"],
        "hoods": ["Ocean Park", "Sunset Park", "North of Montana", "Wilshire Montana", "Pico", "Mid-City"],
        "intro": "Santa Monica remodels, rental unit turnovers and move-outs all produce more debris than a trash can can handle. Our 16-yard roll-off fits most Santa Monica driveways and carries a full kitchen or garage cleanout.",
        "tip": "Santa Monica regulates bins placed on city streets, so a permit is usually needed if the dumpster can't go on your driveway or private property. Alley-facing garages often make the easiest placement.",
        "nearby": ["west-los-angeles", "culver-city", "los-angeles", "torrance"],
    },
    {
        "slug": "culver-city", "name": "Culver City", "county": "Los Angeles County", "region": "West LA",
        "zips": ["90230", "90232"],
        "hoods": ["Downtown Culver City", "Carlson Park", "Culver West", "Sunkist Park", "Blair Hills", "Fox Hills"],
        "intro": "Culver City bungalows and condos get a lot of remodeling work, and a 16-yard dumpster is usually the right size for it. We deliver to every Culver City neighborhood for the same flat price.",
        "tip": "Lots here can be compact. Make sure the truck has room to back in and that low tree branches and wires won't block the drop. Send a photo if you're unsure.",
        "nearby": ["west-los-angeles", "santa-monica", "inglewood", "los-angeles"],
    },
    {
        "slug": "south-los-angeles", "name": "South Los Angeles", "county": "Los Angeles County", "region": "South LA & South Bay",
        "zips": ["90007", "90008", "90016", "90018", "90037", "90043", "90044", "90047", "90062"],
        "hoods": ["West Adams", "Jefferson Park", "Crenshaw", "Baldwin Hills", "Leimert Park", "Hyde Park", "University Park", "Vermont Square"],
        "intro": "South LA is full of craftsman and bungalow renovations, garage-to-ADU conversions and family estate cleanouts. Our 16-yard roll-off handles all three at one flat price, from West Adams to Hyde Park.",
        "tip": "Garage-to-ADU conversions often mean stucco, concrete slab and tile, which are heavy. Ask how much of that will fit within the included 1.5 tons before you start loading.",
        "nearby": ["inglewood", "los-angeles", "downtown-los-angeles", "culver-city"],
    },
    {
        "slug": "inglewood", "name": "Inglewood", "county": "Los Angeles County", "region": "South LA & South Bay",
        "zips": ["90301", "90302", "90303", "90304", "90305"],
        "hoods": ["Morningside Park", "Fairview Heights", "Century Heights", "North Inglewood", "Lockhaven"],
        "intro": "Inglewood homeowners are renovating, adding ADUs and clearing out garages. We deliver 16-yard dumpsters across all five Inglewood ZIP codes with delivery and pickup included.",
        "tip": "Event days at SoFi Stadium and the Kia Forum jam local streets. If your project lines up with a big game or concert, pick a different delivery day so we're not stuck in traffic.",
        "nearby": ["south-los-angeles", "culver-city", "torrance", "west-los-angeles"],
    },
    {
        "slug": "torrance", "name": "Torrance", "county": "Los Angeles County", "region": "South LA & South Bay",
        "zips": ["90501", "90502", "90503", "90504", "90505"],
        "hoods": ["Old Torrance", "West Torrance", "North Torrance", "Walteria", "Seaside", "Hollywood Riviera"],
        "intro": "Torrance and the South Bay are a short drive from our Los Angeles yard. We drop 16-yard dumpsters for garage cleanouts, ranch-house remodels and yard overhauls all over Torrance.",
        "tip": "Most Torrance homes have wide driveways that fit the bin easily. Put a couple of boards under the rails if you want extra protection for your concrete.",
        "nearby": ["long-beach", "inglewood", "south-los-angeles", "santa-monica"],
    },
]
CITY = {c["slug"]: c for c in CITIES}

COUNTIES = [
    {
        "slug": "orange-county", "name": "Orange County",
        "intro": "Quest Hauling is based in Huntington Beach and delivers 16-yard roll-off dumpsters across Orange County. One size, one flat price: $550 for 7 days with 1.5 tons of disposal, delivery and pickup included.",
        "extra": ["Buena Park", "Cypress", "Fullerton", "Garden Grove", "Laguna Beach", "Laguna Niguel", "Lake Forest", "La Habra", "Los Alamitos", "Mission Viejo", "Orange", "Placentia", "Seal Beach", "Stanton", "Tustin", "Westminster", "Yorba Linda"],
        "cities": ["huntington-beach", "newport-beach", "costa-mesa", "fountain-valley", "irvine", "santa-ana", "anaheim"],
    },
    {
        "slug": "los-angeles-county", "name": "Los Angeles County",
        "intro": "From our Los Angeles yard we deliver 16-yard roll-off dumpsters across West LA, Central LA, South LA, the South Bay and Long Beach. One size, one flat price: $550 for 7 days with 1.5 tons of disposal, delivery and pickup included.",
        "extra": ["Beverly Hills", "West Hollywood", "Marina del Rey", "El Segundo", "Hawthorne", "Gardena", "Carson", "Manhattan Beach", "Redondo Beach", "Lakewood", "Signal Hill", "Bellflower", "Cerritos", "Downey"],
        "cities": ["los-angeles", "hollywood", "downtown-los-angeles", "west-los-angeles", "santa-monica", "culver-city", "south-los-angeles", "inglewood", "torrance", "long-beach"],
    },
]

# ---------------------------------------------------------------------------
# Shared copy
# ---------------------------------------------------------------------------
PROJECTS = [
    ("home-cleanout", "Home cleanouts", "Clear out years of furniture, boxes and clutter in one weekend."),
    ("garage-cleanout", "Garage cleanouts", "Get your parking spot back. Old shelving, bikes, boxes and junk."),
    ("remodeling-debris", "Remodeling projects", "Kitchen and bath tear-outs, cabinets, drywall and flooring."),
    ("construction-debris", "Construction debris", "Job-site waste from small builds, ADUs and renovations."),
    ("yard-cleanup", "Yard cleanups", "Branches, brush, old fencing and landscaping debris."),
    ("moving-cleanout", "Moving cleanouts", "Move-outs, rental turnovers and estate cleanouts."),
]

ALLOWED = ["Furniture and household junk", "Cabinets, countertops and fixtures", "Drywall, wood and flooring",
           "Yard waste, branches and fencing", "Carpet and padding", "Boxes, toys and general clutter"]
NOT_ALLOWED = [("hazard", "Hazardous materials", "Chemicals, solvents, fuels, asbestos and pesticides."),
               ("tire", "Tires", "Car and truck tires can't go in the bin."),
               ("paint", "Paint", "Wet paint and paint cans are not accepted.")]

FAQS = [
    ("How much does a dumpster rental cost in Orange County?",
     f"Our 16-yard dumpster is a flat ${B['price']}. That includes delivery, {B['days']} days on site, pickup, and disposal of up to {B['tons']} tons. No fuel surcharge or hidden fees on the standard rental."),
    ("How big is a 16-yard dumpster?",
     "A 16-yard dumpster holds 16 cubic yards of debris, which is roughly 6 to 8 pickup-truck loads. It's big enough for a garage or home cleanout or a kitchen or bathroom remodel, and small enough to fit in most residential driveways."),
    ("How much weight is included?",
     f"Up to {B['tons']} tons (3,000 lbs) of disposal is included. Light, bulky items like furniture and household junk rarely reach that limit. Heavy materials like concrete, dirt, brick, rock and tile add weight quickly, so fill levels for those will be lower."),
    ("Can I keep the dumpster longer than 7 days?",
     "Yes. Let us know before your 7 days are up and we can extend the rental. Ask for the current extra-day rate when you book."),
    ("What can't go in the dumpster?",
     "No hazardous materials (chemicals, fuels, solvents, asbestos, pesticides), no tires and no paint. If you're not sure about an item, call us before you toss it."),
    ("Do I need a permit?",
     "Not if the dumpster sits on your own driveway or private property. If it has to go on a public street, your city may require a permit. Check with your city, and we're happy to help you figure it out."),
    ("Where do you deliver?",
     "We have yards in Huntington Beach and Los Angeles and deliver throughout Orange County and across Los Angeles County, including West LA, Central LA, South LA, the South Bay and Long Beach. Call with your address to confirm delivery."),
    ("How do I book?",
     f"Call {B['phone']} or fill out the quote form on this page with your address and preferred delivery date. We'll confirm your drop-off time."),
]

# ---------------------------------------------------------------------------
# Icons (inline SVG, no image requests)
# ---------------------------------------------------------------------------
ICONS = {
    "bin": '<path d="M4 9h40l-4 26H8z" /><path d="M2 9h44" /><path d="M12 15v14M20 15v14M28 15v14M36 15v14" /><circle cx="12" cy="40" r="3" /><circle cx="36" cy="40" r="3" />',
    "calendar": '<rect x="5" y="9" width="38" height="33" rx="3" /><path d="M5 18h38M15 4v9M33 4v9" /><path d="M13 26h4M22 26h4M31 26h4M13 34h4M22 34h4" />',
    "weight": '<path d="M17 14a7 7 0 1 1 14 0" /><path d="M10 14h28l5 28H5z" />',
    "truck": '<path d="M3 10h26v24H3zM29 18h9l7 8v8H29z" /><circle cx="12" cy="37" r="4" /><circle cx="36" cy="37" r="4" />',
    "phone": '<path d="M14 4l6 10-4 4a26 26 0 0 0 14 14l4-4 10 6-3 8C22 44 4 26 6 7z" />',
    "check": '<path d="M8 25l10 10L40 13" />',
    "pin": '<path d="M24 44S9 29 9 18a15 15 0 0 1 30 0c0 11-15 26-15 26z" /><circle cx="24" cy="18" r="5" />',
    "home": '<path d="M5 22L24 6l19 16" /><path d="M10 18v22h28V18" /><path d="M20 40V28h8v12" />',
    "garage": '<path d="M4 18L24 6l20 12v24H4z" /><path d="M11 42V24h26v18M11 30h26M11 36h26" />',
    "remodel": '<path d="M8 40L30 18" /><path d="M26 8l14 14-6 6-14-14z" /><path d="M6 42h14" />',
    "construction": '<path d="M6 42h36" /><path d="M10 42V22l14-12 14 12v20" /><path d="M10 22h28M17 22v20M31 22v20" />',
    "yard": '<path d="M24 44V22" /><path d="M24 30c-9 0-14-6-14-14 9 0 14 5 14 14zM24 24c0-9 5-16 14-16 0 9-5 16-14 16z" />',
    "moving": '<rect x="6" y="20" width="18" height="18" /><rect x="24" y="10" width="18" height="28" /><path d="M6 29h18M24 24h18" />',
    "hazard": '<circle cx="24" cy="24" r="19" /><path d="M11 11l26 26" /><path d="M24 14v10M24 30v2" />',
    "tire": '<circle cx="24" cy="24" r="19" /><path d="M11 11l26 26" /><circle cx="24" cy="24" r="8" />',
    "paint": '<circle cx="24" cy="24" r="19" /><path d="M11 11l26 26" /><path d="M16 18h16v14H16zM20 14h8" />',
    "arrow": '<path d="M10 24h28M28 14l10 10-10 10" />',
}


def icon(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 48 48" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'


def esc(s):
    return html.escape(s, quote=True)


# Hero illustration: a lime roll-off with the wordmark, drawn in SVG so it is
# crisp at every size and costs ~1 KB instead of a 300 KB photo.
DUMPSTER_SVG = """<svg class="hero-art" viewBox="0 0 560 300" role="img" aria-label="Quest Hauling 16-yard lime green roll-off dumpster">
  <ellipse cx="290" cy="276" rx="250" ry="12" fill="#06204f" opacity=".35"/>
  <path d="M40 92 L520 70 L500 250 L70 250 Z" fill="#8ee02d"/>
  <path d="M40 92 L520 70 L516 104 L44 122 Z" fill="#a6f046"/>
  <path d="M70 250 L500 250 L496 262 L74 262 Z" fill="#5fa411"/>
  <g stroke="#6cb51a" stroke-width="5">
    <path d="M118 120 L124 248"/><path d="M196 117 L200 248"/><path d="M380 109 L376 248"/><path d="M450 106 L444 248"/>
  </g>
  <rect x="44" y="134" width="20" height="12" fill="#fff"/><rect x="44" y="134" width="10" height="12" fill="#e5322d"/>
  <rect x="496" y="122" width="20" height="12" fill="#fff"/><rect x="506" y="122" width="10" height="12" fill="#e5322d"/>
  <text x="290" y="196" text-anchor="middle" font-family="'Barlow Condensed',Impact,sans-serif" font-style="italic" font-weight="900" font-size="88" fill="#0a3aa8" letter-spacing="-2">QUEST</text>
  <text x="352" y="232" text-anchor="middle" font-family="'Barlow Condensed',Impact,sans-serif" font-style="italic" font-weight="800" font-size="30" fill="#0a3aa8" letter-spacing="2">HAULING</text>
  <g fill="#1d2633"><circle cx="110" cy="266" r="12"/><circle cx="460" cy="266" r="12"/></g>
  <g fill="#8a94a3"><circle cx="110" cy="266" r="5"/><circle cx="460" cy="266" r="5"/></g>
</svg>"""

LOGO = '<span class="logo-q">QUEST</span><span class="logo-h">HAULING</span>'

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0a3aa8"/><text x="32" y="47" text-anchor="middle" font-family="Impact,Arial Black,sans-serif" font-style="italic" font-weight="900" font-size="44" fill="#8ee02d">Q</text></svg>"""

# ---------------------------------------------------------------------------
# CSS (inlined in every page: one small file, zero render-blocking requests)
# ---------------------------------------------------------------------------
CSS = """
/* Layout: bold brand bands (lime / white / royal blue) stacked full-bleed, content in a 1160px column */
:root{
  --lime:#8ee02d; --lime-d:#5fa411; --lime-t:#effbdf;
  --blue:#0a3aa8; --blue-d:#06245f; --navy:#051a45;
  --ink:#14213d; --muted:#4a5875; --line:#d9e1ee; --paper:#ffffff; --mist:#eef3fb;
  --display:'Barlow Condensed',Impact,'Arial Narrow',sans-serif;
  --body:'Barlow',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  --r:12px; --wrap:1160px;
  color-scheme:light;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;overflow-x:clip}
body{margin:0;font:400 1.0625rem/1.6 var(--body);color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased}
img,svg{max-width:100%}
a{color:var(--blue)}
h1,h2,h3{font-family:var(--display);line-height:1.02;margin:0;text-wrap:balance;letter-spacing:-.01em}
h2{font-size:clamp(2rem,4.5vw,3rem);font-weight:800;color:var(--blue);text-transform:uppercase}
h3{font-size:1.4rem;font-weight:700}
p{margin:0}
.wrap{max-width:var(--wrap);margin-inline:auto;padding-inline:20px}
.sec{padding-block:clamp(48px,7vw,88px)}
.sec-head{display:grid;gap:10px;margin-bottom:36px;max-width:720px}
.sec-head p{color:var(--muted);font-size:1.125rem}
.eyebrow{font:700 .85rem/1 var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--lime-d)}
.skip{position:absolute;left:-999px;top:8px;background:var(--navy);color:#fff;padding:8px 14px;z-index:99}
.skip:focus{left:8px}
:focus-visible{outline:3px solid var(--blue);outline-offset:3px}
.ico{width:1em;height:1em;fill:none;stroke:currentColor;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;flex:none}

/* Header */
.top{background:var(--lime);position:sticky;top:0;z-index:50;box-shadow:0 2px 0 var(--lime-d)}
.top .wrap{display:flex;align-items:center;gap:24px;min-height:72px}
.logo{display:inline-flex;flex-direction:column;text-decoration:none;line-height:.82;font-family:var(--display);font-style:italic;color:var(--blue)}
.logo-q{font-size:2.4rem;font-weight:900;letter-spacing:-.02em}
.logo-h{font-size:.95rem;font-weight:800;letter-spacing:.18em;align-self:flex-end}
.nav{display:flex;gap:22px;margin-left:auto}
.nav a{color:var(--navy);text-decoration:none;font-weight:600;font-size:.98rem}
.nav a:hover{text-decoration:underline;text-underline-offset:4px}
.nav-toggle{display:none;margin-left:auto;background:none;border:2px solid var(--navy);border-radius:8px;padding:6px 10px;font:700 .9rem var(--body);color:var(--navy)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;font:800 1.15rem/1 var(--display);text-transform:uppercase;letter-spacing:.03em;text-decoration:none;border-radius:10px;padding:16px 22px;border:0;cursor:pointer;transition:transform .15s,box-shadow .15s}
.btn:hover{transform:translateY(-2px)}
.btn .ico{width:1.25em;height:1.25em}
.btn-blue{background:var(--blue);color:#fff;box-shadow:0 4px 0 var(--blue-d)}
.btn-lime{background:var(--lime);color:var(--navy);box-shadow:0 4px 0 var(--lime-d)}
.btn-ghost{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.7)}
.top .btn{padding:12px 16px;font-size:1.2rem}

/* Hero */
.hero{background:radial-gradient(120% 90% at 85% 10%,#1e5ad6 0%,var(--blue) 45%,var(--navy) 100%);color:#fff;overflow:hidden;position:relative}
.hero::after{content:"";position:absolute;inset:auto 0 0 0;height:10px;background:var(--lime)}
.hero .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:32px;align-items:center;padding-block:clamp(40px,6vw,72px)}
.hero-copy{display:grid;gap:18px;min-width:0}
.crumbs{font-size:.9rem;opacity:.85}
.crumbs a{color:#fff}
.hero h1{font-size:clamp(2.4rem,4.6vw,3.9rem);font-weight:900;text-transform:uppercase}
.hero h1 .hl{color:var(--lime);display:block}
.hero-sub{font-size:1.2rem;max-width:34em;opacity:.95}
.price{display:flex;align-items:center;flex-wrap:wrap;gap:6px 18px}
.price-num{font:900 clamp(4rem,10vw,6.5rem)/.85 var(--display);color:#fff;text-shadow:0 5px 0 var(--blue-d)}
.price-num sup{font-size:.45em;vertical-align:.9em;margin-right:2px}
.price-terms{display:grid;gap:4px;font:700 1.25rem/1.15 var(--display);text-transform:uppercase;color:var(--lime)}
.price-terms span:last-child{color:#fff;opacity:.85;font-size:1rem}
.cta-row{display:flex;flex-wrap:wrap;gap:14px;margin-top:6px}
.trust{display:flex;flex-wrap:wrap;gap:8px 22px;list-style:none;padding:0;margin:4px 0 0;font-weight:600;font-size:.98rem}
.trust li{display:flex;align-items:center;gap:8px}
.trust .ico{color:var(--lime);width:1.2em;height:1.2em}
.hero-visual{position:relative;min-width:0}
.hero-photo{display:block;width:100%;height:auto;border-radius:0 18px 18px 0;-webkit-mask-image:linear-gradient(90deg,transparent 0,transparent 22%,#000 46%);mask-image:linear-gradient(90deg,transparent 0,transparent 22%,#000 46%)}
.badge{position:absolute;top:-18px;right:-6px;background:var(--lime);color:var(--navy);font:900 1.1rem/1 var(--display);text-transform:uppercase;text-align:center;width:116px;height:116px;border-radius:50%;display:grid;place-content:center;gap:2px;transform:rotate(10deg);box-shadow:0 6px 0 var(--lime-d)}
.badge b{font-size:2.4rem;display:block}

/* Included strip */
.included{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border:2px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--paper)}
.inc{padding:28px 22px;display:grid;gap:8px;align-content:start;border-right:2px solid var(--line)}
.inc:last-child{border-right:0}
.inc .circle{width:64px;height:64px;border-radius:50%;background:var(--lime);color:var(--navy);display:grid;place-items:center;font-size:2rem;margin-bottom:6px}
.inc h3{color:var(--navy)}
.inc p{color:var(--muted)}

/* Steps */
.steps-bg{background:var(--mist)}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;list-style:none;padding:0;margin:0;counter-reset:s}
.steps li{counter-increment:s;background:var(--paper);border-radius:var(--r);padding:26px 22px;display:grid;gap:8px;align-content:start;border-top:6px solid var(--lime)}
.steps li::before{content:counter(s);font:900 2.8rem/1 var(--display);color:var(--blue)}
.steps p{color:var(--muted)}

/* Projects */
.projects{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.proj{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;align-items:start;padding:22px;border:2px solid var(--line);border-radius:var(--r)}
.proj .circle{grid-row:span 2;width:56px;height:56px;border-radius:14px;background:var(--blue);color:var(--lime);display:grid;place-items:center;font-size:1.7rem}
.proj img{grid-row:span 2;width:120px;height:88px;object-fit:cover;border-radius:10px;background:var(--mist)}
.proj h3{color:var(--navy);font-size:1.3rem}
.proj p{color:var(--muted);font-size:1rem}

/* Size / weight */
.size{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:stretch}
.size-card{background:var(--navy);color:#fff;border-radius:var(--r);padding:32px;display:grid;gap:18px;align-content:start}
.size-card h3{color:var(--lime);font-size:1.7rem;text-transform:uppercase}
.stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.stat{border-left:4px solid var(--lime);padding-left:12px}
.stat b{display:block;font:900 2.4rem/1 var(--display);font-variant-numeric:tabular-nums}
.stat span{font-size:.9rem;opacity:.85}
.meter{display:grid;gap:8px}
.meter-bar{height:16px;border-radius:99px;background:rgba(255,255,255,.15);overflow:hidden;display:flex}
.meter-bar i{display:block;height:100%}
.meter-key{display:flex;justify-content:space-between;font-size:.9rem;opacity:.9;gap:12px}
.rules{display:grid;gap:18px;align-content:start}
.rules h3{color:var(--navy)}
.list-ok{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:10px 18px}
.list-ok li{display:flex;gap:10px;align-items:flex-start}
.list-ok .ico{color:var(--lime-d);width:1.3em;height:1.3em;margin-top:2px}
.no-row{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.no{display:grid;justify-items:center;text-align:center;gap:6px;padding:16px 10px;border-radius:var(--r);background:#fff4f3;border:2px solid #f6cfcc}
.no .ico{color:#d92d27;width:52px;height:52px;stroke-width:3}
.no b{font-family:var(--display);font-size:1.2rem;color:var(--navy)}
.no span{font-size:.88rem;color:var(--muted)}
.note{background:var(--lime-t);border-left:5px solid var(--lime-d);padding:14px 16px;border-radius:8px;font-size:1rem}

/* Service area */
.area{background:linear-gradient(180deg,var(--blue) 0%,var(--navy) 100%);color:#fff}
.area h2{color:#fff}
.area h2 .hl{color:var(--lime)}
.area .sec-head p{color:#d6e2fb}
.area-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.area-col{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);border-radius:var(--r);padding:24px}
.area-col h3{color:var(--lime);text-transform:uppercase;margin-bottom:14px}
.area-col h3 a{color:inherit;text-decoration:none}
.area-col h3 a:hover{text-decoration:underline}
.area-col h4{font:700 .8rem/1 var(--body);letter-spacing:.12em;text-transform:uppercase;color:#d6e2fb;margin:16px 0 8px}
.area-col h3+h4{margin-top:0}
.chips{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:0}
.chips a,.chips span{display:inline-block;padding:7px 13px;border-radius:99px;font-weight:600;font-size:.95rem;text-decoration:none}
.chips a{background:var(--lime);color:var(--navy)}
.chips a:hover{background:#fff}
.chips span{background:rgba(255,255,255,.1);color:#fff}

/* Local (city pages) */
.local{display:grid;grid-template-columns:1.3fr 1fr;gap:36px;align-items:start}
.local-copy{display:grid;gap:16px;min-width:0}
.local-copy p{max-width:65ch}
.local-aside{display:grid;gap:18px;background:var(--mist);border-radius:var(--r);padding:26px}
.local-aside h3{color:var(--navy)}
.zips{display:flex;flex-wrap:wrap;gap:6px}
.zips span{background:var(--paper);border:1px solid var(--line);padding:4px 10px;border-radius:6px;font-variant-numeric:tabular-nums;font-weight:600}
.hoods{columns:2;padding-left:18px;margin:0}

/* FAQ */
.faq{display:grid;gap:12px;max-width:860px}
.faq details{border:2px solid var(--line);border-radius:var(--r);background:var(--paper)}
.faq summary{cursor:pointer;list-style:none;padding:18px 54px 18px 20px;font:700 1.3rem/1.2 var(--display);color:var(--navy);position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:20px;top:50%;transform:translateY(-50%);font-size:1.8rem;color:var(--blue)}
.faq details[open] summary::after{content:"\\2212"}
.faq details[open]{border-color:var(--lime-d)}
.faq details p{padding:0 20px 20px;color:var(--muted)}

/* Quote */
.quote-bg{background:var(--lime)}
.quote{display:grid;grid-template-columns:1fr 1.1fr;gap:40px;align-items:center}
.quote-copy{display:grid;gap:16px}
.quote-copy h2{color:var(--navy)}
.quote-copy p{font-size:1.15rem}
.contact-lines{display:grid;gap:10px;font-weight:700;font-size:1.15rem}
.contact-lines a{color:var(--navy);display:inline-flex;align-items:center;gap:10px;text-decoration:none;word-break:break-word}
.contact-lines .ico{width:1.3em;height:1.3em}
.form{background:var(--paper);border-radius:16px;padding:28px;display:grid;grid-template-columns:1fr 1fr;gap:14px;box-shadow:0 10px 0 var(--lime-d)}
.form h3{grid-column:1/-1;color:var(--blue);font-size:1.8rem;text-transform:uppercase}
.field{display:grid;gap:6px;min-width:0}
.field.full{grid-column:1/-1}
.field label{font-weight:700;font-size:.95rem}
.field input,.field textarea{font:inherit;font-size:1rem;padding:12px 14px;border:2px solid var(--line);border-radius:8px;background:#fff;color:var(--ink);width:100%}
.field input:focus,.field textarea:focus{border-color:var(--blue);outline:none}
.form .btn{grid-column:1/-1}
.form small{grid-column:1/-1;color:var(--muted);text-align:center}
.hp{position:absolute;left:-9999px}

/* Footer */
.foot{background:var(--navy);color:#cfdaf3;padding-block:56px 110px;font-size:.98rem}
.foot-grid{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:32px}
.foot .logo{color:#fff}
.foot .logo-h{color:var(--lime)}
.foot h3{color:#fff;font-size:1.2rem;text-transform:uppercase;margin-bottom:12px}
.foot ul{list-style:none;padding:0;margin:0;display:grid;gap:6px}
.foot a{color:#cfdaf3}
.foot a:hover{color:var(--lime)}
.foot address{font-style:normal;display:grid;gap:6px;margin-top:14px}
.legal{border-top:1px solid rgba(255,255,255,.15);margin-top:36px;padding-top:20px;font-size:.88rem}

/* Mobile call bar */
.callbar{display:none}

@media (max-width:960px){
  .hero .wrap,.size,.local,.quote{grid-template-columns:1fr}
  .hero-visual{max-width:600px}
  .hero-photo{border-radius:14px;-webkit-mask-image:none;mask-image:none;clip-path:inset(0 0 0 27% round 14px);margin-left:-37%;width:137%;max-width:none}
  .included{grid-template-columns:1fr 1fr}
  .inc:nth-child(2){border-right:0}
  .inc:nth-child(-n+2){border-bottom:2px solid var(--line)}
  .steps{grid-template-columns:1fr 1fr}
  .projects{grid-template-columns:1fr 1fr}
  .foot-grid{grid-template-columns:1fr 1fr}
}
@media (max-width:760px){
  .nav-toggle{display:block}
  .top .btn{display:none}
  .nav{display:none;position:absolute;left:0;right:0;top:100%;background:var(--lime);flex-direction:column;gap:0;padding:8px 20px 16px;box-shadow:0 8px 16px rgba(0,0,0,.15)}
  .nav.open{display:flex}
  .nav a{padding:12px 0;border-bottom:1px solid var(--lime-d);font-size:1.1rem}
  .callbar{display:grid;grid-template-columns:1fr 1fr;position:fixed;left:0;right:0;bottom:0;z-index:60;padding-bottom:env(safe-area-inset-bottom,0px);box-shadow:0 -4px 14px rgba(0,0,0,.2)}
  .callbar a{display:flex;align-items:center;justify-content:center;gap:8px;padding:16px 8px;font:800 1.15rem/1 var(--display);text-transform:uppercase;text-decoration:none}
  .callbar a:first-child{background:var(--blue);color:#fff}
  .callbar a:last-child{background:var(--lime);color:var(--navy)}
  .callbar .ico{width:1.2em;height:1.2em}
}
@media (max-width:560px){
  .included,.steps,.projects,.foot-grid,.form,.list-ok{grid-template-columns:1fr}
  .inc{border-right:0;border-bottom:2px solid var(--line)}
  .inc:last-child{border-bottom:0}
  .stat-row,.no-row{grid-template-columns:1fr 1fr 1fr;gap:8px}
  .stat b{font-size:1.8rem}
  .badge{width:92px;height:92px;font-size:.9rem}
  .badge b{font-size:1.8rem}
  .cta-row .btn{flex:1 1 100%}
  .hoods{columns:1}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.btn{transition:none}.btn:hover{transform:none}}
"""

JS = """
(function(){
  var t=document.querySelector('.nav-toggle'),n=document.getElementById('site-nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o)});
    n.addEventListener('click',function(e){if(e.target.tagName==='A'){n.classList.remove('open');t.setAttribute('aria-expanded','false')}})}
  var d=document.getElementById('q-date');
  if(d){var x=new Date();x.setDate(x.getDate()+1);d.min=x.toISOString().slice(0,10)}
})();
"""

# ---------------------------------------------------------------------------
# Structured data
# ---------------------------------------------------------------------------
BIZ_ID = B["domain"] + "/#business"


def business_schema():
    area = [{"@type": "AdministrativeArea", "name": "Orange County, CA"},
            {"@type": "AdministrativeArea", "name": "Los Angeles County, CA"}]
    area += [{"@type": "City", "name": f"{c['name']}, CA"} for c in CITIES]
    return {
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": BIZ_ID,
        "name": B["name"],
        "description": f"{B['size']}-yard roll-off dumpster rental in Orange County and Los Angeles County. ${B['price']} flat rate for {B['days']} days with {B['tons']} tons included.",
        "url": B["domain"] + "/",
        "telephone": "+1-" + B["phone"],
        "email": B["email"],
        "logo": B["domain"] + "/favicon.svg",
        "image": B["domain"] + "/og-image.png",
        "priceRange": f"${B['price']}",
        "address": {"@type": "PostalAddress", "addressLocality": B["city"], "addressRegion": B["region"], "addressCountry": "US"},
        "areaServed": area,
        "makesOffer": {
            "@type": "Offer",
            "price": str(B["price"]), "priceCurrency": "USD",
            "description": f"{B['days']}-day rental, up to {B['tons']} tons of disposal, delivery and pickup included.",
            "itemOffered": {"@type": "Service", "name": f"{B['size']}-Yard Dumpster Rental", "serviceType": "Roll-off dumpster rental"},
        },
    }


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": B["domain"] + u} for i, (n, u) in enumerate(trail)]}


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------
def header():
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="logo" href="/" aria-label="{B['name']} home">{LOGO}</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <a href="/#how-it-works">How It Works</a>
      <a href="/#what-fits">What Fits</a>
      <a href="/#service-area">Service Area</a>
      <a href="/#faq">FAQ</a>
      <a href="#quote">Get a Quote</a>
    </nav>
    <a class="btn btn-blue" href="{PHONE_HREF}">{icon('phone')}{B['phone']}</a>
  </div>
</header>"""


def hero(h1_main, h1_hl, sub, trail=None):
    crumbs = ""
    if trail:
        parts = [f'<a href="{u}">{esc(n)}</a>' for n, u in trail[:-1]] + [esc(trail[-1][0])]
        crumbs = f'<nav class="crumbs" aria-label="Breadcrumb">{" / ".join(parts)}</nav>'
    return f"""<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs}
      <h1>{h1_main}<span class="hl">{h1_hl}</span></h1>
      <p class="hero-sub">{sub}</p>
      <div class="price" aria-label="Price">
        <div class="price-num"><sup>$</sup>{B['price']}</div>
        <div class="price-terms"><span>{B['days']} days &bull; {B['tons']} tons included</span><span>Delivery &amp; pickup included</span></div>
      </div>
      <div class="cta-row">
        <a class="btn btn-lime" href="#quote">{icon('calendar')}Book your dumpster</a>
        <a class="btn btn-ghost" href="{PHONE_HREF}">{icon('phone')}Call {B['phone']}</a>
      </div>
      <ul class="trust">
        <li>{icon('check')}One flat price</li><li>{icon('check')}No hidden fees</li><li>{icon('check')}Local yards in OC &amp; LA</li>
      </ul>
    </div>
    <div class="hero-visual">
      <img class="hero-photo" src="/img/dumpster-rental-orange-county.webp" width="594" height="421" fetchpriority="high" decoding="async" alt="Quest Hauling 16-yard lime green roll-off dumpster parked by the Huntington Beach pier">
      <div class="badge" aria-hidden="true"><b>{B['size']}</b>Yard</div>
    </div>
  </div>
</section>"""


def included():
    items = [("bin", f"{B['size']}-yard dumpster", "The right size for most home cleanouts, remodels and job sites."),
             ("calendar", f"{B['days']}-day rental", "A full week on site to work at your own pace."),
             ("weight", f"Up to {B['tons']} tons", "3,000 lbs of disposal weight included in the price."),
             ("truck", "Delivery &amp; pickup", "We drop it off and haul it away when you're done.")]
    cells = "".join(f'<div class="inc"><div class="circle">{icon(i)}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in items)
    return f"""<section class="sec" id="pricing" aria-labelledby="pricing-h">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Simple dumpster rental</span><h2 id="pricing-h">What ${B['price']} gets you</h2>
    <p>One dumpster size and one flat price, so you know exactly what you'll pay before we deliver.</p></div>
    <div class="included">{cells}</div>
  </div>
</section>"""


def steps(place="your driveway"):
    s = [("Book online or by phone", "Tell us your address, delivery date and what you're tossing. We'll confirm your drop-off window."),
         ("We deliver the bin", f"Our driver places the {B['size']}-yard roll-off on {place} or job site."),
         ("Fill it up", f"Take up to {B['days']} days. Load it evenly and keep debris below the top rim."),
         ("We haul it away", "Call when you're done and we pick it up and handle the disposal.")]
    li = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in s)
    return f"""<section class="sec steps-bg" id="how-it-works" aria-labelledby="how-h">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">How it works</span><h2 id="how-h">Four steps to a clean project</h2></div>
    <ol class="steps">{li}</ol>
  </div>
</section>"""


def projects(city=None):
    where = f" in {city}" if city else ""
    cards = "".join(
        f'<div class="proj"><img src="/img/{i}.webp" width="140" height="102" loading="lazy" decoding="async" '
        f'alt="{t} with a Quest Hauling dumpster"><h3>{t}</h3><p>{d}</p></div>' for i, t, d in PROJECTS)
    return f"""<section class="sec" aria-labelledby="proj-h">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Perfect for</span><h2 id="proj-h">Projects our dumpster handles{where}</h2></div>
    <div class="projects">{cards}</div>
  </div>
</section>"""


def what_fits():
    ok = "".join(f"<li>{icon('check')}{x}</li>" for x in ALLOWED)
    no = "".join(f'<div class="no">{icon(i)}<b>{t}</b><span>{d}</span></div>' for i, t, d in NOT_ALLOWED)
    tons_lbs = int(B["tons"] * 2000)
    return f"""<section class="sec steps-bg" id="what-fits" aria-labelledby="fits-h">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Dumpster guidelines</span><h2 id="fits-h">What fits in a {B['size']}-yard dumpster</h2>
    <p>Roughly 6 to 8 pickup-truck loads of debris. Here's what you can toss and what has to stay out.</p></div>
    <div class="size">
      <div class="size-card">
        <h3>{B['size']}-yard roll-off at a glance</h3>
        <div class="stat-row">
          <div class="stat"><b>{B['size']}</b><span>cubic yards</span></div>
          <div class="stat"><b>{tons_lbs:,}</b><span>lbs included</span></div>
          <div class="stat"><b>{B['days']}</b><span>days on site</span></div>
        </div>
        <div class="meter">
          <strong>How fast weight adds up</strong>
          <div class="meter-bar" aria-hidden="true"><i style="width:30%;background:var(--lime)"></i><i style="width:35%;background:#f5c542"></i><i style="width:35%;background:#ef6b5b"></i></div>
          <div class="meter-key"><span>Furniture &amp; household junk: light</span><span>Concrete, dirt, rock: heavy</span></div>
        </div>
        <p>Fill levels vary for heavy materials such as concrete, dirt, brick, rock or similar dense debris. A bin full of concrete would weigh far more than {B['tons']} tons, so heavy loads stop well below the rim.</p>
      </div>
      <div class="rules">
        <h3>Good to go</h3>
        <ul class="list-ok">{ok}</ul>
        <h3>Not allowed</h3>
        <div class="no-row">{no}</div>
        <p class="note">Not sure about an item? Call <a href="{PHONE_HREF}">{B['phone']}</a> before you toss it.</p>
      </div>
    </div>
  </div>
</section>"""


def service_area():
    cols = []
    for co in COUNTIES:
        groups = {}
        for s in co["cities"]:
            groups.setdefault(CITY[s].get("region"), []).append(s)
        inner = ""
        for region, slugs in groups.items():
            links = "".join(f'<li><a href="/dumpster-rental/{s}/">{CITY[s]["name"]}</a></li>' for s in slugs)
            label = f'<h4>{esc(region)}</h4>' if region else ""
            inner += f'{label}<ul class="chips">{links}</ul>'
        extra = "".join(f"<li><span>{esc(n)}</span></li>" for n in co["extra"])
        inner += f'<h4>Also serving</h4><ul class="chips">{extra}</ul>'
        cols.append(f'<div class="area-col"><h3><a href="/dumpster-rental/{co["slug"]}/">{co["name"]}</a></h3>{inner}</div>')
    return f"""<section class="sec area" id="service-area" aria-labelledby="area-h">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">{icon('pin')} Service area</span>
    <h2 id="area-h">Serving Orange County <span class="hl">&amp; Los Angeles County</span></h2>
    <p>With yards in Huntington Beach and Los Angeles, we deliver across both counties. Don't see your city? Call us and we'll confirm delivery to your address.</p></div>
    <div class="area-grid">{''.join(cols)}</div>
  </div>
</section>"""


def faq(faqs, heading="Dumpster rental questions"):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
    return f"""<section class="sec" id="faq" aria-labelledby="faq-h">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">FAQ</span><h2 id="faq-h">{heading}</h2></div>
    <div class="faq">{items}</div>
  </div>
</section>"""


def quote(city=None):
    where = city or "Orange County or LA County"
    return f"""<section class="sec quote-bg" id="quote" aria-labelledby="quote-h">
  <div class="wrap quote">
    <div class="quote-copy">
      <span class="eyebrow" style="color:var(--blue)">Get a quote or book now</span>
      <h2 id="quote-h">Book your {B['size']}-yard dumpster</h2>
      <p>${B['price']} flat for {B['days']} days and {B['tons']} tons, delivered anywhere in {esc(where)}. Send the form and we'll confirm your delivery date, or call for the fastest booking.</p>
      <div class="contact-lines">
        <a href="{PHONE_HREF}">{icon('phone')}{B['phone']}</a>
        <a href="mailto:{B['email']}"><svg class="ico" viewBox="0 0 48 48" aria-hidden="true"><rect x="5" y="10" width="38" height="28" rx="3"/><path d="M5 12l19 14 19-14"/></svg>{B['email']}</a>
      </div>
    </div>
    <form class="form" action="{B['form_action']}" method="POST">
      <h3>Request delivery</h3>
      <input type="hidden" name="_subject" value="New dumpster request{(' - ' + esc(city)) if city else ''}">
      <input type="hidden" name="_template" value="table">
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="field"><label for="q-name">Name</label><input id="q-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="q-phone">Phone</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" required></div>
      <div class="field full"><label for="q-email">Email</label><input id="q-email" name="email" type="email" autocomplete="email"></div>
      <div class="field"><label for="q-addr">Delivery address</label><input id="q-addr" name="address" autocomplete="street-address" required></div>
      <div class="field"><label for="q-date">Delivery date</label><input id="q-date" name="delivery_date" type="date"></div>
      <div class="field full"><label for="q-details">Project details (optional)</label><textarea id="q-details" name="details" rows="3" placeholder="Garage cleanout, kitchen remodel, yard waste..."></textarea></div>
      <button class="btn btn-blue" type="submit">Book your dumpster {icon('arrow')}</button>
      <small>We'll call or text to confirm. No payment needed to request a date.</small>
    </form>
  </div>
</section>"""


def footer():
    cities = "".join(f'<li><a href="/dumpster-rental/{c["slug"]}/">Dumpster rental {c["name"]}</a></li>' for c in CITIES)
    counties = "".join(f'<li><a href="/dumpster-rental/{c["slug"]}/">{c["name"]}</a></li>' for c in COUNTIES)
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="/">{LOGO}</a>
        <p style="margin-top:14px">{B['size']}-yard roll-off dumpster rental. ${B['price']} flat, {B['days']} days, {B['tons']} tons included.</p>
        <address>
          <span>{B['name']} &middot; {B['city']}, {B['region']}</span>
          <a href="{PHONE_HREF}">{B['phone']}</a>
          <a href="mailto:{B['email']}">{B['email']}</a>
        </address>
      </div>
      <div><h3>Service areas</h3><ul>{counties}{cities}</ul></div>
      <div><h3>Quick links</h3><ul>
        <li><a href="/#pricing">Pricing</a></li><li><a href="/#how-it-works">How it works</a></li>
        <li><a href="/#what-fits">What fits</a></li><li><a href="/#faq">FAQ</a></li><li><a href="#quote">Get a quote</a></li>
      </ul></div>
    </div>
    <p class="legal">&copy; {date.today().year} {B['name']}. Dumpster rental serving Orange County and Los Angeles County, California.</p>
  </div>
</footer>
<nav class="callbar" aria-label="Quick contact">
  <a href="{PHONE_HREF}">{icon('phone')}Call now</a>
  <a href="#quote">{icon('calendar')}Book</a>
</nav>"""


def page(path, title, desc, body, schema_nodes):
    url = B["domain"] + path
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": B["domain"] + "/#website", "url": B["domain"] + "/", "name": B["name"], "publisher": {"@id": BIZ_ID}},
        business_schema(),
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
         "isPartOf": {"@id": B["domain"] + "/#website"}, "about": {"@id": BIZ_ID}, "dateModified": TODAY},
    ] + schema_nodes}
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#8ee02d">
<meta name="geo.region" content="US-CA">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{B['name']}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{B['domain']}/og-image.png">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;0,800;0,900;1,800;1,900&family=Barlow:wght@400;600;700&display=swap">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(graph, separators=(',', ':'))}</script>
</head>
<body>
{header()}
<main id="main">
{body}
</main>
{footer()}
<script>{JS}</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def home():
    title = f"Dumpster Rental Orange County & LA County | ${B['price']} 16-Yard | {B['name']}"
    desc = (f"16-yard dumpster rental in Orange County & Los Angeles County for a flat ${B['price']}: "
            f"{B['days']} days, {B['tons']} tons, delivery and pickup included. Yards in Huntington Beach and LA. Call {B['phone']}.")
    body = "\n".join([
        hero(f"{B['size']}-Yard Dumpster Rental", "in Orange County &amp; Los Angeles County",
             f"One size. One price. No hassle. Roll-off dumpsters delivered from our Huntington Beach and Los Angeles yards for cleanouts, remodels and job sites."),
        included(), steps(), projects(), what_fits(), service_area(), faq(FAQS), quote(),
    ])
    return page("/", title, desc, body, [faq_schema(FAQS)])


def city_page(c):
    n = c["name"]
    path = f"/dumpster-rental/{c['slug']}/"
    county_slug = "orange-county" if c["county"] == "Orange County" else "los-angeles-county"
    trail = [("Home", "/"), (c["county"], f"/dumpster-rental/{county_slug}/"), (f"Dumpster Rental {n}", path)]
    title = f"Dumpster Rental {n}, CA | ${B['price']} 16-Yard Roll-Off | {B['name']}"
    desc = (f"Rent a 16-yard dumpster in {n} for ${B['price']} flat: {B['days']} days, {B['tons']} tons, "
            f"delivery and pickup included. Fast local service from our {yard_for(c['county'])} yard. Call {B['phone']}.")
    faqs = [
        (f"How much is a dumpster rental in {n}?",
         f"A 16-yard roll-off dumpster in {n} is ${B['price']} flat, including delivery, {B['days']} days on site, pickup and up to {B['tons']} tons of disposal."),
        (f"Do I need a permit for a dumpster in {n}?",
         f"No permit is needed when the dumpster sits on your driveway or private property. If it needs to go on a public street, check with the City of {n} first."),
        (f"Which {n} ZIP codes do you serve?",
         f"We deliver to all of {n}, including ZIP codes {', '.join(c['zips'])}."),
    ] + [f for f in FAQS if f[0].startswith(("How big", "How much weight", "What can't"))]
    hoods = "".join(f"<li>{esc(h)}</li>" for h in c["hoods"])
    zips = "".join(f"<span>{z}</span>" for z in c["zips"])
    nearby = "".join(f'<li><a href="/dumpster-rental/{s}/">Dumpster rental {CITY[s]["name"]}</a></li>' for s in c["nearby"])
    local = f"""<section class="sec" aria-labelledby="local-h">
  <div class="wrap local">
    <div class="local-copy">
      <span class="eyebrow">Local dumpster service</span>
      <h2 id="local-h">Roll-off dumpsters for {esc(n)} homes and job sites</h2>
      <p>{esc(c['intro'])}</p>
      <p>Every rental is the same simple deal: a {B['size']}-yard dumpster, {B['days']} days to fill it, {B['tons']} tons of disposal and delivery and pickup, all for ${B['price']}. No sorting through five bin sizes or guessing at add-on fees.</p>
      <p class="note"><strong>{esc(n)} tip:</strong> {esc(c['tip'])}</p>
    </div>
    <aside class="local-aside" aria-label="{esc(n)} service details">
      <h3>Neighborhoods we serve</h3>
      <ul class="hoods">{hoods}</ul>
      <h3>{esc(n)} ZIP codes</h3>
      <div class="zips">{zips}</div>
      <h3>Nearby service areas</h3>
      <ul class="hoods">{nearby}</ul>
    </aside>
  </div>
</section>"""
    body = "\n".join([
        hero("Dumpster Rental", f"in {esc(n)}, CA",
             f"{B['size']}-yard roll-off dumpsters delivered to {esc(n)} driveways and job sites. One size, one flat price, no hassle.", trail),
        local, included(), steps(f"your {n} driveway"), projects(n), what_fits(), faq(faqs, f"Dumpster rental in {esc(n)}: FAQ"), quote(n),
    ])
    return page(path, title, desc, body, [faq_schema(faqs), crumbs_schema(trail)])


def county_page(co):
    n = co["name"]
    path = f"/dumpster-rental/{co['slug']}/"
    trail = [("Home", "/"), (f"Dumpster Rental {n}", path)]
    title = f"Dumpster Rental {n} | ${B['price']} 16-Yard Dumpsters | {B['name']}"
    desc = (f"16-yard dumpster rental across {n} for ${B['price']} flat: {B['days']} days, {B['tons']} tons, delivery and pickup included. Call {B['phone']}.")
    city_cards = "".join(
        f'<div class="proj"><div class="circle">{icon("pin")}</div><h3><a href="/dumpster-rental/{s}/">{CITY[s]["name"]}</a></h3><p>{esc(CITY[s]["intro"].split(". ")[0])}.</p></div>'
        for s in co["cities"])
    extra = ", ".join(co["extra"])
    cities_sec = f"""<section class="sec" aria-labelledby="cities-h">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">{esc(n)} service area</span><h2 id="cities-h">Dumpster rental across {esc(n)}</h2>
    <p>{esc(co['intro'])}</p></div>
    <div class="projects">{city_cards}</div>
    <p style="margin-top:24px;max-width:70ch">We also deliver to {esc(extra)} and surrounding communities. Call <a href="{PHONE_HREF}">{B['phone']}</a> to confirm your address.</p>
  </div>
</section>"""
    faqs = [(f"Do you deliver dumpsters everywhere in {n}?",
             f"We deliver throughout {n} from our {yard_for(n)} yard. Call with your address and we'll confirm your delivery window.")] + FAQS[:4]
    body = "\n".join([
        hero("Dumpster Rental", f"in {esc(n)}", f"{B['size']}-yard roll-off dumpsters for {esc(n)} cleanouts, remodels and construction projects. ${B['price']} flat.", trail),
        cities_sec, included(), steps(), what_fits(), faq(faqs, f"{esc(n)} dumpster rental FAQ"), quote(n),
    ])
    return page(path, title, desc, body, [faq_schema(faqs), crumbs_schema(trail)])


def yard_for(county):
    return "Huntington Beach" if county == "Orange County" else "Los Angeles"


def write(rel, content):
    p = os.path.join(OUT, rel.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    urls = ["/"]
    write("index.html", home())
    for co in COUNTIES:
        urls.append(f"/dumpster-rental/{co['slug']}/")
        write(f"dumpster-rental/{co['slug']}/index.html", county_page(co))
    for c in CITIES:
        urls.append(f"/dumpster-rental/{c['slug']}/")
        write(f"dumpster-rental/{c['slug']}/index.html", city_page(c))
    write("favicon.svg", FAVICON)
    static = os.path.join(os.path.dirname(OUT), "static")
    if os.path.isdir(static):
        shutil.copytree(static, OUT, dirs_exist_ok=True)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {B['domain']}/sitemap.xml\n")
    sm = "".join(f"  <url><loc>{B['domain']}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    print(f"Built {len(urls)} pages into {OUT}")


if __name__ == "__main__":
    main()
