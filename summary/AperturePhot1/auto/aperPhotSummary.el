(TeX-add-style-hook
 "aperPhotSummary"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("scrartcl" "paper=letter" "fontsize=11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("fontenc" "T1") ("babel" "english") ("placeins" "section")))
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
    '("horrule" 1))
   (LaTeX-add-labels
    "fig:shift1"
    "fig:shift2"
    "eqn:fit"
    "fig:subcomp"
    "fig:lightcurve"
    "fig:glenn")))

