---
title: 'pyhector: A Python interface for the simple climate model Hector'
tags:
  - climate change
  - simple climate model
  - python-wrapper
authors:
 - name: Sven N Willner
   orcid: 0000-0001-6798-6247
   affiliation: 1, 2
 - name: Corinne Hartin
   orcid: 0000-0003-1834-6539
   affiliation: 3
 - name: Robert J Gieseke
   orcid: 0000-0002-1236-5109
   affiliation: 1
affiliations:
 - name: Potsdam Institute for Climate Impact Research
   index: 1
 - name: University of Potsdam
   index: 2
 - name: Joint Global Change Research Institute
   index: 3
date: 19 April 2017
bibliography: paper.bib
output: pdf_document
---

# Summary

Pyhector is a Python interface for the simple climate model Hector [@Hartin2015] developed in C++. Simple climate models like Hector can, for instance, be used in the analysis of scenarios within integrated assessment models like
GCAM^[<http://jgcri.github.io/gcam-doc/hector.html>],
in the emulation of complex climate models, and in uncertainty analyses.

Hector is an open-source, object oriented, simple global climate carbon cycle model. Its carbon cycle consists of a one pool atmosphere, three terrestrial pools which can be broken down into finer biomes or regions, and four carbon pools in the ocean component. The terrestrial carbon cycle includes primary production and respiration fluxes. The ocean carbon cycle circulates carbon via a simplified thermohaline circulation, calculating air-sea fluxes along with the marine carbonate system [@Hartin2016].

The model input is time series of greenhouse gas emissions; as example scenarios for
these the Pyhector package contains the Representative Concentration Pathways
(RCPs)^[<http://tntcat.iiasa.ac.at:8787/RcpDb/dsd?Action=htmlpage&page=welcome>].
These were developed to cover the range of baseline and mitigation emissions scenarios
and are widely used in climate change research and model intercomparison projects.
Using DataFrames from the Python library Pandas^[<http://pandas.pydata.org/>] as a data
structure for the scenarios simplifies generating and adapting scenarios.
Other parameters of the Hector model can easily be modified when running the model.

Pyhector can be installed using `pip` from the Python Package Index ^[<https://pypi.python.org/pypi/pyhector>].
Source code and issue tracker are available in Pyhector's GitHub
repository^[<https://github.com/openclimatedata/pyhector>].
Documentation is provided through
Readthedocs^[<http://pyhector.readthedocs.io/en/latest/>].
Usage examples are also contained in the repository as a Jupyter Notebook [@Perez2007; @Kluyver2016]. Courtesy of the Mybinder project^[<http://mybinder.org/>], the example
Notebook can also be executed and modified without installing pyhector locally.

# References
