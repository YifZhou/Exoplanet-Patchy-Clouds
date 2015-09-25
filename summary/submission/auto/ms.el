(TeX-add-style-hook
 "ms"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("emulateapj" "apj")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("hyperref" "breaklinks" "colorlinks" "citecolor=blue" "linkcolor=magenta")))
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
    "hyperref")
   (TeX-add-symbols
    "ima"
    "flt"
    "eps"
    "tinytim"
    "bpic"
    "vsini"
    "mjup"
    "natexlab")
   (LaTeX-add-labels
    "fig:1"
    "fig:2"
    "Results"
    "fig:3"
    "fig:4"
    "fig:5")
   (LaTeX-add-bibitems
    "Ackerman2001"
    "Allard2012"
    "Apai2013"
    "Baraffe2003"
    "Barman2011b"
    "Berta2012"
    "Biretta2014"
    "Bonnefoy2014"
    "Buenzli2012"
    "Buenzli2015"
    "Burrows2006a"
    "Chauvin2004"
    "Chauvin2005"
    "Currie2011"
    "dressel2012wide"
    "Ducourant2008"
    "Heinze2015"
    "Helling2008"
    "Klein2003"
    "Kostov2013"
    "Kreidberg2014"
    "Krist1995"
    "Mackenty2008"
    "Madhusudhan2011"
    "Mandell2013"
    "Marley2012"
    "Marley2010"
    "Marois2008a"
    "Metchev2015"
    "Mohanty2013"
    "Mohanty2007"
    "Patience2010"
    "Radigan2012"
    "Showman2013"
    "Skemer2011"
    "Skemer2012"
    "Snellen2014"
    "Song2006"
    "Sterzik2004"
    "Yang2015"
    "Zhang2014")))

