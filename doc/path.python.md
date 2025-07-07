Present current python search path for modules, with or without a virtualenv, it always works.
```sh
python3 -c "import sys; [print(p) for p in sys.path]"
```
