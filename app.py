from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from src.textSummarizer.prediction.predictor import Predictor


class PredictRequest(BaseModel):
    texts: List[str]


# lazy predictor singleton
predictor = Predictor()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - lazy load on first request
    print("TextSummarizer API starting up...")
    yield
    # Shutdown
    print("TextSummarizer API shutting down...")


app = FastAPI(title="TextSummarizer Prediction API", lifespan=lifespan)


@app.get("/health")
def health():
	return {"status": "ok", "model_loaded": predictor.model is not None}


@app.post("/predict")
async def predict(req: PredictRequest):
	try:
		outputs = predictor.predict(req.texts)
		return {"predictions": outputs}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/upload")
async def predict_upload(file: UploadFile = File(...)):
	"""Accept a plain text file where each line is an input text."""
	content = await file.read()
	try:
		text = content.decode("utf-8")
	except Exception:
		raise HTTPException(status_code=400, detail="File must be utf-8 text")
	lines = [l.strip() for l in text.splitlines() if l.strip()]
	if not lines:
		raise HTTPException(status_code=400, detail="No text lines found in file")
	try:
		outputs = predictor.predict(lines)
		return {"predictions": outputs}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)

