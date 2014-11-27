(TeX-add-style-hook
 "abpic"
 (lambda ()
   (TeX-run-style-hooks
    "latex2e"
    "aastex"
    "aastex10")
   (LaTeX-add-labels
    "fig:lc")))

