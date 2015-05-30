(TeX-add-style-hook
 "TinyTimPSF"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("scrartcl" "paper=letter" "fontsize=11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("fontenc" "T1") ("babel" "english") ("placeins" "section")))
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
    "scrartcl"
    "scrartcl10"
    "fontenc"
    "fourier"
    "babel"
    "amsmath"
    "amsfonts"
    "amsthm"
    "hyperref"
    "bm"
    "graphicx"
    "placeins"
    "sectsty"
    "fancyhdr")
   (TeX-add-symbols
    '("horrule" 1)
    "chisq"
    "PSF"
    "Img"
    "PSFI"
    "PSFII")
   (LaTeX-add-labels
    "eq:chisq"
    "eq:calchisq"
    "eq:1")))

