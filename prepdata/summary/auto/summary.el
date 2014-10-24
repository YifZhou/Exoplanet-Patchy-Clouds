(TeX-add-style-hook
 "summary"
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
    "fig:x_off"
    "fig:y_off"
    "fig:shifted"
    "fig:ringing")))

