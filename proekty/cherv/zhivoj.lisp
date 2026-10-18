;;;; Метрики походки живого червя N2 на агаре (Open Worm Movement Database,
;;;; CC BY 4.0, лежит в wormlisp/reference/) тем же кодом, что у модели.
;;;;   cd ext/wormlisp && sbcl --noinform --non-interactive --no-sysinit --no-userinit \
;;;;        --load scripts/init.lisp --load ../../proekty/cherv/zhivoj.lisp
(asdf:load-system "worm")
(format t "~&живой N2 на агаре: ~S~%"
        (worm.analysis:track-gait (worm.analysis:read-track "reference/schafer-n2-agar/track.wcon")))
