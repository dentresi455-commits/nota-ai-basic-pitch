import os
import tempfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.responses import JSONResponse
from basic_pitch.inference import predict, Model
from basic_pitch import ICASSP_2022_MODEL_PATH

app = FastAPI(title='NOTA AI Basic Pitch Service')
_model = None
MAX_BYTES = 12 * 1024 * 1024

@app.get('/health')
def health():
    return {'status': 'ok', 'model': 'spotify/basic-pitch', 'loaded': _model is not None}

@app.post('/analyze')
async def analyze(audio: UploadFile = File(...), x_api_key: str | None = Header(default=None)):
    secret = os.getenv('NOTA_ANALYSIS_KEY')
    if not secret or x_api_key != secret:
        raise HTTPException(401, 'Unauthorized')
    suffix = Path(audio.filename or '').suffix.lower()
    if suffix not in ('.wav', '.mp3', '.m4a', '.flac', '.ogg'):
        raise HTTPException(415, 'Unsupported audio format')
    raw = await audio.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise HTTPException(413, 'Audio too large (12 MB max)')
    global _model
    if _model is None:
        _model = Model(ICASSP_2022_MODEL_PATH)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / ('input' + suffix)
        path.write_bytes(raw)
        _, midi, events = predict(str(path), _model)
        notes = [{'start': round(float(start), 3), 'end': round(float(end), 3), 'midi': int(pitch), 'confidence': round(float(amp), 3)} for start, end, pitch, amp, *_ in events]
        return {'status': 'analyzed', 'note_count': len(notes), 'notes': notes[:2000], 'warning': 'Automatic transcription is approximate; this is not yet a score comparison.'}
