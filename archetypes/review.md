+++
date = '{{ .Date }}'
draft = true
title = '{{ replace .File.ContentBaseName "-" " " | title }}'
headline = ''
dek = ''
weight = 50
categories = ['Executive Leather']
tags = []
keywords = []
# Key into data/offers.yaml. Drives the lead photo, hero link, sidebar, sticky bar,
# final CTA and every otherwise-unlinked image on the page. The photo itself comes
# from that product's `image` field (set by tools/fetch_unsplash.py). Only set an
# `image = "..."` here to override it for this one page.
offer = '{{ .File.ContentBaseName }}'
verdict = ''
cardCue = 'Read the review →'
finalCta = ''
faq = [
  { q = '', a = '' },
  { q = '', a = '' },
]
+++

{{</* key-takeaways offer="OFFER_KEY" */>}}
- Point one
- Point two
- Point three
{{</* /key-takeaways */>}}

## First section

Open with the problem, not the product. End the paragraph with a money link:
{{</* buy "OFFER_KEY" */>}}check the current Amazon price{{</* /buy */>}}.

{{</* offer-card "OFFER_KEY" */>}}

## Second section

The differentiating feature. Another money link with different anchor text.

{{</* img-link offer="OFFER_KEY" caption="One-line verdict" */>}}

## Third section

Practical details: sizing, care, what to check before ordering.

{{</* pros-cons */>}}
- Pro one
- Pro two
vs
- Con one
- Con two
{{</* /pros-cons */>}}

## Who it's for

One paragraph. Name the alternative for people this isn't right for — and link to
that review internally.

{{</* cta "OFFER_KEY" */>}}
