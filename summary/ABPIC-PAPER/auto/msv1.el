(TeX-add-style-hook
 "msv1"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("emulateapj" "iop")))
   (TeX-run-style-hooks
    "latex2e"
    "emulateapj"
    "emulateapj10"
    "graphicx"
    "amssymb"
    "amsmath")))

