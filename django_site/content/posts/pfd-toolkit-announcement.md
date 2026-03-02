---
draft: false
id: 2
title: We’re sitting on over a decade of preventable-deaths data. Now we can actually use it.
seo_title: Turning PFD Reports Into Usable Safety Intelligence
seo_description: We show how PFD Toolkit converts Prevention of Future Deaths reports into a searchable, analysable dataset, enabling faster national reviews and more practical learning from preventable harm.
slug: pfd-toolkit-announcement
authors:
  - sam
  - dan-joyce
date: 2026-03-02
categories:
  - Announcement
  - Original research
image: assets/pfd-toolkit-cover.svg
meta:
  - property: og:image
    content: 
---

Prevention of Future Deaths (PFD) reports contain some of the clearest public evidence we have about where systems fail before further harm occurs, yet for years they have been trapped in an archive that is difficult to search, analyse, or learn from at scale. We outline our new paper in *BMJ Mental Health* and explain how PFD Toolkit turns that archive into something that can finally be used for rapid, reproducible safety learning.

<!-- more -->

---

When a coroner’s inquest concludes that a person’s death exposed risks that could claim further lives, a coroner may issue a Prevention of Future Deaths (PFD) report. These are written in the aftermath of tragedy. They set out where systems broke down, and identify the organisations expected to act so that it does not happen again.

In other words, PFD reports are an early-warning system. They can describe failures in clinical care, but also breakdowns in policing, prison safety, care coordination, housing provision, transport safety, and beyond. They often document gaps between agencies, missed opportunities to share information, unsafe environments, flawed processes and procedures, and overstretched services, to name a few. They are written at the sharp end of tragedy. And they are public.

Taken together, these reports represent one of the most direct, ground-level sources of safety intelligence in the country. But until recently, they have been almost impossible to use properly.



## The paradox: high-value data, low usability

The PFD archive contains thousands of reports dating back over a decade. Yet the system is not built to support data extraction, synthesis, harmonisation, or analysis by either humans or computers. Reports are dispersed across a judicial website, inconsistently categorised, and often available only as digital "photocopies". There is no structured dataset. No export button. And no reliable search functionality.

As a result, researching patterns and trends across preventable deaths has meant manually screening, extracting data, and synthesising across thousands of individual reports, sometimes taking months or even years. This is not hypothetical; it is how previous national reviews have had to operate.

The result is predictable: labour-intensive work, limited reproducibility, and an archive that remains largely under-used.

So the problem has never been that we lack the data to provide insight into preventable deaths. The problem has been access, with a high bar for converting the data contained in PFDs into actionable information for system learning and avoiding recurrence of preventable harm.

## Turning narrative into data

In our [paper](https://mentalhealth.bmj.com/content/29/1/e302212), recently published in *BMJ Mental Health*, we tested whether this barrier is now technically soluble with modern data-driven technology like AI.

We developed an automated pipeline that ingests the entire PFD archive, as published on the judiciary website, extracts text from both digital and scanned reports, screens reports for relevance to any chosen topic, identifies recurring themes, and produces a clean, analysable dataset.

To evaluate it rigorously, we replicated an [existing national thematic review](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/mentalhealth/bulletins/preventionoffuturedeathreportsforsuicideinchildreninenglandandwales/january2015tonovember2023) of child-suicide-related PFD reports conducted by the Office for National Statistics. The original manual review identified 37 relevant cases. Our automated system identified 73, nearly twice as many. The ONS analysis required months of work from a team of researchers to screen, code, and analyse reports. PFD Toolkit took just over 5 minutes on an ordinary laptop.

We then benchmarked the system against a panel of independent psychiatrists. The clinicians were blinded to the tool’s outputs and each other’s assessment, yet agreed with PFD Toolkit’s screening decisions 97% of the time, meaning PFD Toolkit performs at least as well as the expert clinicians involved in the study.

## Why this matters

At its core, this is a public safety story, rather than an AI one.

When coroners raise concerns, they intend to prevent recurrence and further harm. Yet without structured access to the archive, tracing recurring themes across 14 years of reports is extremely difficult.

Are the same failures being raised repeatedly? Do gaps between services persist over time? Is there an increase in particular types of concern? Do organisational responses lead to measurable change? Without usable data, these questions remain largely unanswered.

Converting unstructured narrative text contained in messy digital formats into harmonised, thematically structured, analysable data changes that. With our PFD Toolkit, the judiciary’s archive can now function as a living dataset rather than a static repository on a website, which can be analysed by directly asking pertinent questions of the data. This makes rapid national thematic reviews feasible, enables longitudinal monitoring of systemic risks, and supports more timely policy feedback.

## A shift in how we think about AI in healthcare

Much of the current conversation about AI in healthcare centres on prediction: risk scores, early warning models, and forecasts of future events.

Our work highlights a different application. Many risks are already documented in plain sight. They appear in documents such as coroners’ reports, serious incident investigations, regulatory findings, and other long-form documents. The difficulty lies in systematically reading and synthesising what has already been recorded.

In our case, we used large language models (LLMs) to make existing safety intelligence searchable, structured, and reproducible. Their function was not to predict outcomes, but to surface existing patterns embedded within thousands of pages of narrative text.

## From archive to infrastructure

For years, the [House of Commons Justice Committee has described](https://publications.parliament.uk/pa/cm5802/cmselect/cmjust/68/6810.htm) the official preventable deaths repository as providing the bare minimum for serious learning. PFD reports were designed to elicit action as a result of warnings and findings from the coronial inquest process, but the infrastructure to learn from them at scale has been limited by the absence of substantial human time and resource. We are now at a point where that infrastructure can exist.

The warnings have always been there. They were written by coroners, addressed to institutions, and published in the public domain. What has changed is our ability to systematically interrogate them. We are sitting on over a decade of preventable-deaths data.

Now we can actually use it.

<!-- post-footer -->

PFD Toolkit is available as an interactive web app at [pfdtoolkit.org](https://pfdtoolkit.org), as well as a Python package. Our paper is openly available [here](https://mentalhealth.bmj.com/content/29/1/e302212), and is authored by Sam Osian, Arpan Dutta, Sahil Bhandari, Iain Buchan, and Dan Joyce.



For any questions, please contact [Sam](mailto:samoand@liverpool.ac.uk).
