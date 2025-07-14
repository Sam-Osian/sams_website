---
draft: false
title: Rethinking 'significance' — Has the p-value overstayed its welcome?
slug: rethinking-significance
authors:
  - sam
date: 2025-07-15
categories:
  - Opinion
  - Statistics
meta:
  - property: og:image
    content: 
---

In research, the p-value is often treated as the ultimate test of truth. But should all statistical analysis be held to the same statistical standard? 

In this post, I argue that the p-value is too often used as a universal yardstick, regardless of context or consequences. Sometimes, what counts as “enough” evidence depends on the risks and decisions at stake, not just on whether a result falls below an arbitrary threshold.

![Is significance just?](https://videos.openai.com/vg-assets/assets%2Ftask_01jzwvhes2f7vs6e1qw9dpfjsr%2F1752241428_img_0.webp?st=2025-07-11T12%3A15%3A11Z&se=2025-07-17T13%3A15%3A11Z&sks=b&skt=2025-07-11T12%3A15%3A11Z&ske=2025-07-17T13%3A15%3A11Z&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skoid=aa5ddad1-c91a-4f0a-9aca-e20682cc8969&skv=2019-02-02&sv=2018-11-09&sr=b&sp=r&spr=https%2Chttp&sig=Ls0ySDsQcQ2gyn9LvYhWVylTiInT8siN3HzSbDMMY1c%3D&az=oaivgprodscus){ width="600" }

<!-- more -->

---

## Explaining the p-value

If you're somewhat familiar with law (or have at least watched a courtroom drama... or if you're me, Judge Judy), you'll probably know that there are different standards of proof depending on the type of court. 

In criminal cases, this bar is set really high. A jury must be sure “beyond a reasonable doubt” that the defendant did in fact commit the crime. We can (loosely) quantify this as needing to be ~99.5% certain. In civil disputes, it’s “on the balance of probabilities” — essentially, what’s more likely than not (i.e. being at least 51% sure). 

It makes intuitive sense to say that different situations require different thresholds of confidence for making decisions, depending on what's at stake, and how important the end decision is. In criminal court, we can hardly send someone to jail if the evidence _points towards_ but ultimately does not _clearly demonstrate_ that they did in fact carry out the alleged crime. For civil disputes, where neither party faces criminal conviction, the stakes are much lower.

Yet, in statistical research, we often fail to extend this logic. The p-value — usually pegged at 0.05 — has become a one-size-fits-all verdict on what counts as evidence. 

At its simplest, the p-value tells us how likely it is to observe results as extreme as the ones we got, just by random chance, if there was actually no effect at all. The lower the p-value, the less likely it is that our results are a fluke. Below the _0.05_ threshold, a result is often deemed “statistically significant”; above it, often written off as lacking sufficient evidence. 

The effect of this threshold obscures a much more prudent question: _what level of evidence is appropriate for the decision at hand?_



## Where things start to fall apart

Consider this hypothetical scenario: a school-based breakfast programme is trialled to see if it improves pupils’ attendance. The study finds a positive effect: among a sample of students with poor baseline attendance, attendance improved by 14% following engagement with the breakfast programme.

A statistical researcher plugs these data into a model of some kind, and reports this effect alongside a p-value of _0.11_. This misses the conventional threshold of _0.05_ and, consequently, the researcher deems the results as “statistically insignificant.” The school principal, reading the report, decides to drop the breakfast programme entirely. 

But let’s look at the real-world context. Assume that providing breakfast at school is low-cost, low-risk, and easy to implement. The wider literature may also suggest potential knock-on benefits, such as improved community cohesion. In other words, there’s little to lose, and the evidence — though not definitive — certainly suggests a likely benefit. The effect size itself is modest but it's absolutely _practically_ significant. In other words, the programme is likely to make a positive difference to the school.

If this were a civil court, we’d simply ask: is it more likely than not that this intervention is associated with improved attendance? On that standard, the answer is a clear _yes_. The effect size and the p-value, when taken together, cleanly pass the “the balance of probabilities” threshold. Given the low-cost, low-risk nature of the programme, this seems to be vastly more appropriate than applying a “beyond reasonable doubt” standard.


## ...But let's not go too far

Introducing new medication is a completely different story. The risks could be higher (especially if the drug has major side effects), and the consequences more serious. Medical ethics correctly tells us to be vigilant that we're acting in a given patient's best interests. In this case, a much lower p-value — something closer to “beyond reasonable doubt” — is entirely justified and most likely _necessary_. 

The point I'm endeavouring to make is that while relying on fixed, uncritical statistical thresholds may be a convenient rule, it's not a particularly useful or thoughtful one. By insisting on a universal threshold, we end up applying the same standard whether the stakes are routine or life-changing. Worse, it encourages us to treat the result as binary: significant or not, yes or no. This doesn't match the grey, murkiness of real-world uncertainty.

The broader issue here is that statistical prediction isn’t the same as decision-making. Prediction should inform our choices, but complex decisions require a layer of human judgement to mediate between numbers and action. In this way, the p-value should not be used 'checklist' style but rather _interpreted_ within the context of the research area, as well as related statistical metrics like the point estimate, confidence interval, and measures of dispersion.

*[point estimate]: Our best guess of the population-level effect (e.g. improved attendance by 14%).
*[confidence interval]: A range of plausible values for our point estimate.
*[measures of dispersion]: How varied or 'spread out' our data is. 

## Language is important

Language plays a part. The phrase “not significant” is a way of stepping back from judgment, leaving the interpretation to the number itself. If instead we said, “There is moderate evidence, but uncertainty remains,” we would be more honest — and probably more useful to anyone trying to make a real-world decision. 

Most researchers have felt the frustration of working on a promising project, only for a regression model to return a p-value of, say, _0.054_. It's frustrating precisely because we _know_ that our results provide moderate evidence towards our research aim, yet they are still “insignificant” for all intents and purposes. 

This leads some researchers to adopt awkward, and sometimes quite comical, phrasing. [One study](https://www.tandfonline.com/doi/full/10.1080/07315724.2018.1461147) researching the potential health impacts of green coffee consumption regularly used the phrase “almost statistically significant” to describe their p-values, which hovered around _0.06_. I’m not criticising the researchers here, but it does show that the gravitational pull of the 0.05 threshold is strong — even when we know, deep down, that reality is rarely so clear-cut.



![alt text](../assets/images/paper-almost-significant.png)
/// caption
A published research paper using the phrase ‘almost statistically significant’ for p-values just missing the conventional threshold.
///



I do want to be transparent here: everything I've said above isn't a novel critique. Many have already been arguing for a more nuanced approach before, particularly in epidemiology where framing of the p-value in terms of providing “low / moderate / strong / very strong” evidence has already started to take hold. 

But still, the checkbox culture persists, especially within the social sciences. We can do better by recognising that the appropriate standard of evidence depends on context — not by pretending that 0.05 has universal applicability.

In the end, statistics is a tool for making sense of uncertainty, not erasing it. A p-value is just one part of the story. The real work lies in making thoughtful decisions about what evidence means for the world outside the dataset.
