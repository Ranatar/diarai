# Запуск render_archive.py со своими шрифтами (без установки в систему).
import os, sys, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ["FONTCONFIG_FILE"] = os.path.join(HERE, "fonts.conf")
sys.path.insert(0, HERE)
os.chdir(HERE)
sys.argv = ["render_archive.py"] + sys.argv[1:]
runpy.run_path(os.path.join(HERE, "render_archive.py"), run_name="__main__")
