;;;; proekty/cherv/progon.lisp — один прогон червя Wormlisp (автор архива)
;;;; на третьем уровне управления: сеть 147 нейронов коннектома, агар.
;;;; Запуск из копии ext/wormlisp (inbox не трогаем):
;;;;   cd ext/wormlisp && sbcl --noinform --non-interactive --no-sysinit --no-userinit \
;;;;        --load scripts/init.lisp --load ../../proekty/cherv/progon.lisp
;;;; Повторяет то, что делает пакетный рабочий (src/batch/worker.lisp),
;;;; но в одном процессе и с печатью метрик походки.

(asdf:load-system "worm")

;;; Параметры: после --end-toplevel-options идут  id params секунды dt
;;; (песочница не пускает переменные окружения перед командой).
(defparameter *args* (rest (member "--end-toplevel-options" sb-ext:*posix-argv* :test #'string=)))
(defparameter *id* (or (first *args*) "moi-1"))
(defparameter *model* "WORM-3D-CONNECTOME")
(defparameter *params* (or (second *args*) "agar-a-v1"))
(defparameter *duration* (parse-integer (or (third *args*) "12")))
(defparameter *dt* (if (fourth *args*) (let ((*read-default-float-format* 'double-float))
                                        (coerce (read-from-string (fourth *args*)) 'double-float))
                       1d-3))

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
