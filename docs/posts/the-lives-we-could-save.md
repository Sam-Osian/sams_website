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

Here’s a grim truth: in England and Wales, coroners find that systemic safety issues play a part in _hundreds_ of preventable deaths each year. By "systemic," we mean risks that could lead to further deaths if nothing changes — essentially, problems that go beyond one-off mistakes.

When this happens, coroners document their concerns in what’s called a **Prevention of Future Deaths** (or _PFD_) **report**.

These reports aren't subtle. They're blunt, often painfully so. Each report is about a unique tragedy, but all echo the same basic message: _“This could happen again, unless action is taken.”_ The reports then get sent to whoever the coroner determines is best placed to address these concerns, whether that’s a hospital, NHS Trust, Government minister, or someone else.

Now, you might naturally assume — as I did — that there must be a robust national system for learning from these reports. Some way of connecting the dots and turning repeated warnings into action. Unfortunately not. PFD reports are fired off and filed away, with no reliable way to bring them together, spot recurring issues, or make sure lessons turn into policy.

This problem hasn't gone unrecognised. A House of Commons Justice Committee [report](https://committees.parliament.uk/publications/6079/documents/75085/default/) has stated this system is entirely “under-developed” for public safety. This is a _damning_ verdict for a system fundamentally set-up to save lives. But perhaps [The Times](https://www.thetimes.com/comment/the-times-view/article/the-times-view-on-coroners-reports-warnings-unheeded-0qpb6phdx) said it best:

> “So it is that Britain allows the opportunity to save thousands of lives to slip by.”

## The pains of PFD research

Put yourself in the shoes of a researcher, tasked with analysing PFD reports on some specific topic. Say, for example, you wanted to look for recurring issues coroners have raised related to an issue such as: suicide, deaths in prisons, a certain medication error, or perhaps something more specific such as cases related to 'being sectioned' under the Mental Health Act.

For this, you must read through potentially _thousands_ of reports by hand to determine whether each individual PFD report is relevant to your research topic. You must then identify and code each report against the themes you're interested in, one by one.
  
This manual effort is compounded by there being no way of mass-downloading report content into a neat, tabular dataset. You must also grapple with around 7 in 10 reports being miscategorised. Many reports are also, unhelpfully, low quality photocopies, which lack embedded text.

It’s a laborious process that can take _months_, or even _years_. Perhaps for this reason, research analysing PFD reports is exceedingly rare (and all use highly manual methods of screening reports).


## The solution

This is where [PFD Toolkit](https://pfdtoolkit.org) comes in. 

**PFD Toolkit is a Python package designed to do all the heavy lifting in PFD research.**

![PFD Toolkit](https://pfdtoolkit.org/assets/header.png){ width="700" }

I built this package as I was tired of knowing that — without a way of monitoring recurring issues — similar mistakes could be slipping through the cracks, just because the evidence was scattered.

The Toolkit provides a suite of AI tools, courtesy of large language models (or 'LLMs'), to automate the process of collecting, screening and analysing PFD reports. Instead of forcing researchers to read thousands of documents by hand, it lets you pull together a living, searchable dataset in minutes.

Through the Toolkit, you can:

 * Instantly load live and fully cleaned PFD data into a dataset or spreadsheet, updated weekly.
 * Search for reports about any topic: deaths linked to medication errors, failures in mental health care, deaths in custody, or whatever else you need. You don't need to worry about keyword matching, as the Toolkit's AI handles this automatically.
 * Discover recurring themes within your filtered set of PFD reports. You can either let the model handle this entire process, or you can customise it by supplying a few 'seed topics' to get it started.
 * Pull out other kinds of structured features from the long text (e.g. age, sex, cause of death, or any other information that may be buried within each report).


_PFD Toolkit can be pip installed through:_

```python
pip install pfd_toolkit
```

Put simply: PFD Toolkit turns a previously unworkable archive into an engine of insight for use in research, policy, healthcare or public interest journalism.



## What's next

We're really excited to see how other people will use PFD Toolkit for their own research, as well as hearing feedback on how the Toolkit can be adapted or strengthened further.

For us, the next stage is to evaluate the Toolkit's performance by considering how well it 'agrees' with expert clinicians' own judgement. We also want to measure the time saved using the toolkit against the previous manual methods used.

PFD Toolkit isn't the final answer. It’s just a tool — a way to open up the data, and invite others to interrogate it. I hope it will help researchers, journalists, clinicians, and campaigners dig deeper, ask new questions, and make the case for the kinds of changes that really matter.


---



_For more information on PFD Toolkit and a guide for getting started, please visit: [pfdtoolkit.org](https://pfdtoolkit.org/)_. 

_If you're not a coder but would still like to use PFD Toolkit, please do get in touch with me at <mailto:samoand@liverpool.ac.uk> — I'd be very happy to help you get started._ 

_Many thanks to [Jonathan Pytches](https://www.linkedin.com/in/jonathan-pytches/) for contributing towards this project._ 

---