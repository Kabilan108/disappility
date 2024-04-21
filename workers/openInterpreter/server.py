from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uvicorn

import oiProcessor


app = FastAPI()


class Data(BaseModel):
    prompt: str


@app.post("/oiprocessor")
async def oi_processor(data: Data, background: BackgroundTasks):
    background.add_task(oiProcessor.prompt_pipeline, data.prompt)

    return {"message": "working on it!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
