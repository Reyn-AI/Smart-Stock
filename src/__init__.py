from pathlib import Path
import sys
from .analysis.tushare_analysis import *
from src.backtest.strategys import *
from src.utils.common import import_modules_from_py

import_modules_from_py(str(Path(__file__).resolve().parents[0] / 'strategys'))
import_modules_from_py(str(Path(__file__).resolve().parents[0] / 'select'))