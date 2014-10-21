(TeX-add-style-hook "summary"
 (lambda ()
    (LaTeX-add-labels
     "fig:x_off"
     "fig:y_off"
     "fig:shifted"
     "fig:ringing")
    (TeX-add-symbols
     '("horrule" 1))
    (TeX-run-style-hooks
     "fancyhdr"
     "sectsty"
     "placeins"
     "section"
     "graphicx"
     "bm"
     "hyperref"
     "amsthm"
     "amsfonts"
     "amsmath"
     "babel"
     "english"
     "fourier"
     "fontenc"
     "T1"
     "latex2e"
     "scrartcl10"
     "scrartcl")))

