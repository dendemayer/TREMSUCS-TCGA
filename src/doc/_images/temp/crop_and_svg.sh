#!/usr/bin/bash

pdfcrop standalone_subfigure6.pdf
pdfcrop standalone_subfigure7.pdf

pdftocairo -svg standalone_subfigure6-crop.pdf standalone_subfigure6-crop.svg
pdftocairo -svg standalone_subfigure7-crop.pdf standalone_subfigure7-crop.svg

mv standalone_subfigure*crop.* ../
