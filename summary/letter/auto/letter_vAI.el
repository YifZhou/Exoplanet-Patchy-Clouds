(TeX-add-style-hook
 "letter_vAI"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("emulateapj" "apj")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("xcolor" "dvipsnames") ("hyperref" "breaklinks" "colorlinks" "citecolor=blue" "linkcolor=magenta")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "url")
   (TeX-run-style-hooks
    "latex2e"
    "F125W"
    "F160W"
    "emulateapj"
    "emulateapj10"
    "graphicx"
    "amssymb"
    "amsmath"
    "natbib"
    "color"
    "xcolor"
    "multirow"
    "hyperref")
   (TeX-add-symbols
    '("reviseTwo" 1)
    '("revise" 1)
    "ima"
    "flt"
    "eps"
    "tinytim"
    "bpic"
    "vsini"
    "mjup"
    "period"
    "Jperiod"
    "Jperiodd"
    "Jamp"
    "Hperiod"
    "Hperiodd"
    "Hamp"
    "natexlab")
   (LaTeX-add-labels
    "fig:1"
    "fig:2"
    "fig:3"
    "sec:MCMC"
    "fig:4"
    "Results"
    "sec:discussion"
    "fig:5")
   (LaTeX-add-bibitems
    "Ackerman2001"
    "Biretta2014"
    "Burrows2006a"
    "dressel2012wide"
    "Kostov2013"
    "Krist1995"
    "Lodato2005"
    "Marley2011"
    "Reiners2008"
    "Showman2013"
    "Zhang2014")))

