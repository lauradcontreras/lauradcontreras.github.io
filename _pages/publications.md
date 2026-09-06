---
layout: page
permalink: /research/
title: research
description: Job market paper, working papers, and work in progress.
nav: true
nav_order: 1
---

<!-- _pages/publications.md -->

<div class="publications">

## Job market paper

{% bibliography --query @*[stage=jmp] %}

## Working papers

{% bibliography --query @*[stage=working] %}

## Work in progress

{% bibliography --query @*[stage=wip] %}

</div>

<p style="margin-top:2rem; font-size:0.9em; opacity:0.7;"><em>* scheduled.</em></p>
