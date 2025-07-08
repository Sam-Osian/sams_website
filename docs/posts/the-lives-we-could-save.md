---
draft: true
title: What if we actually learned from preventable deaths?
authors:
  - sam
date: 2025-07-09
categories:
  - Announcements
  - PFD Toolkit
meta:
  - property: og:image
    content: /assets/myphoto.png
---

**How do we spot the same deadly mistakes before they happen again?**

Prevention of Future Deaths (PFD) reports shine a light on the risks that cost lives across England and Wales. But while each report warns of a specific danger, there’s been no easy way to see the bigger picture — to spot recurring patterns and systemic failings hiding in plain sight. 

[PFD Toolkit](https://pfdtoolkit.org) changes this. For the first time, researchers and analysts can screen reports for relevant cases, identify recurring themes, and pull out structured data from the written reports — all in a matter of minutes.

![Finding insight in PFD reports](https://videos.openai.com/vg-assets/assets%2Ftask_01jzkgw429eapa03xfx9jqq2k8%2F1751928243_img_0.webp?st=2025-07-08T16%3A54%3A17Z&se=2025-07-14T17%3A54%3A17Z&sks=b&skt=2025-07-08T16%3A54%3A17Z&ske=2025-07-14T17%3A54%3A17Z&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skoid=8ebb0df1-a278-4e2e-9c20-f2d373479b3a&skv=2019-02-02&sv=2018-11-09&sr=b&sp=r&spr=https%2Chttp&sig=xmlG0PmJKv4Vud%2BUEz%2B9M00gPoiWzIEJVPn%2Bn%2BBuXvY%3D&az=oaivgprodscus){ width="600" }

<!-- more -->

---

Here’s a grim truth: in England and Wales, coroners find that systemic safety issues play a part in _hundreds_ of preventable deaths each year. By "systemic," we mean risks that could lead to further deaths if nothing changes — problems that go beyond one-off mistakes.

When this happens, coroners write what’s called a **Prevention of Future Deaths** (or _PFD_) **report**. 

These reports aren't subtle. They're blunt, often painfully so. Each report is about a unique tragedy, but all echo the same basic message: _“This could happen again, unless action is taken.”_ The reports then get sent to whoever the coroner thinks might fix the problem, whether that’s a hospital, NHS Trust, government minister, or someone else.

Now, you might naturally assume — as I did — that there’d be some central system for learning from these reports, some way of connecting the dots and turning repeated warnings into action. But there isn’t. PFD reports are fired off and filed away, with no reliable way to bring them together, spot recurring issues, or make sure lessons turn into policy.

This problem hasn't gone completely unrecognised. A House of Commons Justice Committee [report](https://committees.parliament.uk/publications/6079/documents/75085/default/) has stated this system is entirely 'under-developed' for public safety. But perhaps [The Times](https://www.thetimes.com/comment/the-times-view/article/the-times-view-on-coroners-reports-warnings-unheeded-0qpb6phdx) said it best:

> So it is that Britain allows the opportunity to save thousands of lives to slip by.

## The pains of PFD research

Put yourself in the shoes of a researcher, tasked with analysing PFD reports on some specific topic. Say, for example, you wanted to look for issues related to suicide deaths, deaths in prisons, a certain medication error, or something more specific such as concerns related to 'being sectioned' under the Mental Health Act.

For this, you must read through potentially _thousands_ of reports by hand to determine whether each case is relevant to your research topic. You must then identify and code the themes or topics you're interested in, _one by one_.
  
This manual effort is compounded by there being no way of mass-downloading report content into a neat, tabular dataset. You must grapple with around 7 in 10 reports being miscategorised, with many reports being digital scans (which are processed as images, meaning they don't have any embedded text).

It’s a laborious process that can take _months_, or even _years_. Perhaps for this reason, research analysing PFD reports is exceedingly rare.


## The solution

This is where PFD Toolkit comes in. I built it because I was tired of knowing that similar mistakes could be slipping through the cracks, just because the evidence was scattered.

**PFD Toolkit is a Python package designed to do all the heavy lifting.**

![PFD Toolkit](https://pfdtoolkit.org/assets/header.png){ width="700" }

The Toolkit provides a suite of AI (large language model, LLM) tools to automate the process of collecting, screening and analysing reports for research. Instead of forcing researchers to read thousands of documents by hand, it lets you pull together a living, searchable dataset in minutes.

Through the Toolkit, you can:

 * Instantly load live PFD data into a dataset or spreadsheet, updated daily. 
 * Search for reports about any topic: deaths linked to medication errors, failures in mental health care, deaths in custody, or whatever else you need. You don't need to worry about keyword matching, as the Toolkit's AI handles this automatically.
 * Discover recurring themes within your filtered of PFD reports. You can let the model handle this entire process, or you can customise it by supplying a few 'seed topics' to get it started.
 * Pull out other kinds of structured features from the long text (e.g. age, sex, cause of death, or any other information that may be buried within each report).

PFD Toolkit can be pip installed through:

```python
pip install pfd_toolkit
```

Put simply: it turns a practically unworkable archive into an engine of insight for use in research, policy, healthcare or public interest journalism.


## What's next

We're really excited to see how other people will use PFD Toolkit for their own research, as well as hearing feedback on how the Toolkit can be adapted or strengthened further.

PFD Toolkit isn't the final answer. It’s just a tool — a way to open up the data, and invite others to interrogate it. I hope it will help researchers, journalists, clinicians, and campaigners dig deeper, ask new questions, and make the case for the kinds of changes that really matter.

---

_For more information on PFD Toolkit and a guide for getting started, please visit: [pfdtoolkit.org](https://pfdtoolkit.org/)_. 

_If you're not a coder but would still like to use PFD Toolkit, please do get in touch with me at <mailto:samoand@liverpool.ac.uk> — I'd be very happy to help you get started._ 

---