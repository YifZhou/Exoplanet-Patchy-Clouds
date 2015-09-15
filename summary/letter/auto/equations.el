(TeX-add-style-hook
 "equations"
 (lambda ()
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10")
   (TeX-add-symbols
    "amp"
    "ampJ"
    "ampH")))

