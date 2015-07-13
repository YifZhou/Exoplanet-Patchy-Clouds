(TeX-add-style-hook
 "msv1"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("emulateapj" "apj")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("hyperref" "breaklinks" "colorlinks" "citecolor=blue" "linkcolor=magenta")))
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
    "emulateapj"
    "emulateapj10"
    "graphicx"
    "amssymb"
    "amsmath"
    "natbib"
    "hyperref")
   (TeX-add-symbols
    "ima"
    "flt"
    "eps")
   (LaTeX-add-labels
    "fig:1"
    "fig:fig2"
    "fig:3")
   (LaTeX-add-bibliographies
    "ref.bib")))

