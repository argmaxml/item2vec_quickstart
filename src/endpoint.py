import sys, json, os, threading, time, signal, collections
from typing import Optional, List, Union
import numpy as np
import pandas as pd
from fastapi import FastAPI
from decouple import config

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "OK"}

def die():
    time.sleep(1)
    os.kill(os.getpid(),signal.SIGKILL)

@app.get("/restart")
async def restart():
    threading.Thread(target=die).start()
    return "Shutting down"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", host="127.0.0.1", port=5000)
