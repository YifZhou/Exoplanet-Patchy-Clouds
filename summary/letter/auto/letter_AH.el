(TeX-add-style-hook
 "letter_AH"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("emulateapj" "apj")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("xcolor" "dvipsnames") ("hyperref" "breaklinks" "colorlinks" "citecolor=blue" "linkcolor=magenta")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "emulateapj"
    "emulateapj10"
    "graphicx"
    "amssymb"
    "amsmath"
    "natbib"
    "color"
    "xcolor"
    "hyperref")
   (TeX-add-symbols
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
    "Jamp"
    "Hperiod"
    "Hamp")
   (LaTeX-add-labels
    "fig:1"
    "fig:2"
    "Results"
    "fig:3"
    "fig:4"
    "sec:discussion"
    "fig:5")
   (LaTeX-add-bibliographies
    "ref.bib")))

