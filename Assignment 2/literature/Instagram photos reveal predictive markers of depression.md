---
title: Instagram photos reveal predictive markers of depression
created: '2019-10-01T20:15:23.238Z'
modified: '2019-10-01T20:56:08.214Z'
---

# Instagram photos reveal predictive markers of depression
This document contains a summary of the article titled with: "Instagram photos reveal predictive markers of depression".

**Reference**
> Reece, A. G., & Danforth, C. M. (2017). Instagram photos reveal predictive markers of depression. EPJ Data Science, 6(1), 15.Reece, A. G., & Danforth, C. M. (2017). Instagram photos reveal predictive markers of depression. EPJ Data Science, 6(1), 15.Reece, A. G., & Danforth, C. M. (2017). Instagram photos reveal predictive markers of depression. EPJ Data Science, 6(1), 15.

## Introduction
The paper attempts to detect psychiatric disorders using images posted on instagram instead of the text. According to them, analysis on text, is the more traditional, but proven to be ineffective.

**Hypothesis 1**
> Instagram posts made by individuals diagnosed with depression can be reliably distinguished from posts made by healthy controls, using only measures extracted computationally from posted photos and associated metadata.

### Photographic markes of depression
The paper states that colour values, such as hue, saturation, and brightness, provide valuable insights into someones psychiatric state (e.g. depression involves more darker, grayer colours).

The posting frequency is used as metric for user engagement.

**Hypothesis 2**
>Instagram posts made by depressed individuals prior to the date of first clinical diagnosis can be reliably distinguished from posts made by healthy controls.

*General practitioners were able to correctly rule out depression in non-depressed patients 81% of the time, but only diagnosed depressed patients correctly 42% of the time.*

The researchers in the paper wonder whether it is possible for machines / computes to classify an image as happy or sad based on machine-like data (e.g. pixel values, saturation).

## Method

### Improving data quality
All participants with five or fewer instagram posts were excluded. They also excluded participants with a **CES-D** score of 22 or higher. This score indicates an optimal cutoff for identifying clinically relevant depression.

**Based on this cutoff, there may be an optimal cutoff for wellbeing?**

### Feature extraction
**Primary model**
- User activity is measured with *total posts per user, per day*.
- Community reaction is measured with *number of comments and likes per photograph*.
- Social activity level is measured with *number of faces in a photo*.
- Pixel level averages are computed for HSV values.
- Use of an instagram filter or not.

**Secondary model** (predictors)
- happy
- sad
- likeable
- interesting

### Units of observation
The paper states that depression is not a state that is persistently active during a set period of time for every moment of every day. Therefore, using someone's entire post history as a single unit is rather spacious. It also states that the other extreme, using every post as a single unit of observation runs the risk of being too granular.
>  De Choudhury et al. [2] looked at all of a given user’s posts in a single day, and aggregated those data into **per-person, per-day units of observation. We adopted this precedent of ‘user-days’ as a unit of analysis**.
