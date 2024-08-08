from typing import Optional, List, Union
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from fastapi import FastAPI
from argparse import ArgumentParser
import uvicorn
from src.web.routers import select_stock_api
from src.web.routers import kline_api
from src.web.routers import overall_api
from src.web.routers import user_api
from src.web.routers import order_api
from src.web.routers import analysis_api
from src.web.routers import backtrade_api
from src.web.routers import stock_inofs_api

app = FastAPI()
app.include_router(select_stock_api.router)
app.include_router(kline_api.router)
app.include_router(overall_api.router)
app.include_router(user_api.router)
app.include_router(order_api.router)
app.include_router(analysis_api.router)
app.include_router(backtrade_api.router)
app.include_router(stock_inofs_api.router)

def launch(host:str='0.0.0.0', port:int=38888, reload:bool=True):
    uvicorn.run(app='main:app', host=host, port=port, reload=reload, loop='uvloop')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=38888)
    parser.add_argument('--reload', action='store_true')
    args = parser.parse_args()
    
    launch(host=args.host, port=args.port, reload=args.reload)
