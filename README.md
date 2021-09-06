# Proyecto Final

## Setup

Se recomienda utilizar Python 3.8, y una buena forma de instalarlo es con [pyenv](https://github.com/pyenv/pyenv).
Tambien es recomendable utilizar un entorno aislado para evitar problemas con las dependencias:

```bash
python -m venv ~/.venv/ati
source ~/.venv/ati/bin/activate
```

Para instalar las dependencias con `pip` es necesario instalar algunos pre-requisitos:
```bash
sudo apt install -y libjpeg-dev zlib1g libtiff-dev # Ubuntu
pip install -r requirements.txt
```

Finalmente, para ejecutar:
```bash
cd src
PYTHONPATH=.. python app.py
```

Para editar las vistas con Qt Designer:
```bash
~/.venv/ati/bin/qt5-tools designer main_window.ui
```

Para generar las vistas con PyUIC:
```bash
python -m PyQt5.uic.pyuic main_window.ui -o main_window.py
```
