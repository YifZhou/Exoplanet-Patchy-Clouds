(TeX-add-style-hook
 "reply"
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
    "fancyhdr"
    "scalerel"
    "calc")
   (TeX-add-symbols
    '("embed" 1)
    '("horrule" 1))
   (LaTeX-add-counters
    "embedlevel")
   (LaTeX-add-lengths
    "embedspace")))

