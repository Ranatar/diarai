;;;; proekty/cherv/progon.lisp — один прогон червя Wormlisp (автор архива)
;;;; на третьем уровне управления: сеть 147 нейронов коннектома, агар.
;;;; Запуск из копии ext/wormlisp (inbox не трогаем):
;;;;   cd ext/wormlisp && sbcl --noinform --non-interactive --no-sysinit --no-userinit \
;;;;        --load scripts/init.lisp --load ../../proekty/cherv/progon.lisp
;;;; Повторяет то, что делает пакетный рабочий (src/batch/worker.lisp),
;;;; но в одном процессе и с печатью метрик походки.

(asdf:load-system "worm")

(defparameter *id* (or (uiop:getenv "CHERV_ID") "moi-1"))
(defparameter *model* (or (uiop:getenv "CHERV_MODEL") "WORM-3D-CONNECTOME"))
(defparameter *params* (or (uiop:getenv "CHERV_PARAMS") "agar-a-v1"))
(defparameter *duration* (parse-integer (or (uiop:getenv "CHERV_SEC") "12")))
(defparameter *dt* 1d-3)

(let* ((dir (merge-pathnames (format nil "runs/~A/" *id*) (uiop:getcwd)))
       (set (worm.params:load-param-set *params*))
       (model (worm.codegen:compile-model (find-symbol *model* :worm.components)
                                          :params set :cache t))
       (t0 (get-internal-real-time))
       (run (worm.runtime:start-run model :params set :dt *dt* :id *id* :directory dir
                                          :record t :frames-every 0.01d0
                                          :policy :batch :thread nil)))
  (worm.runtime:step-run (round *duration* *dt*) run)
  (format t "~&статус: ~A, ~,1F с стенных часов~%"
          (worm.runtime:run-status run)
          (/ (- (get-internal-real-time) t0) internal-time-units-per-second))
  (worm.runtime:stop-run run)
  (let ((m (worm.analysis:run-gait dir :from 4d0)))
    (format t "~&метрики походки (с 4-й секунды): ~S~%" m))
  (worm.analysis:write-run-metrics dir)
  (format t "~&каталог: ~A~%" dir))
