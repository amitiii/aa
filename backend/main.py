from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:3000",
    "https://conci-ai.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IntentRequest(BaseModel):
    text: str

@app.post("/process_intent")
async def process_intent(req: IntentRequest):
    text = req.text.lower()
    reply = ""

    if "towel" in text:
        reply = "Sure, a fresh towel will be sent to your room shortly."
    elif "spa" in text or "massage" in text:
        reply = "Spa appointment booked for 5 PM. Would you like a reminder?"
    elif "restaurant" in text or "food" in text:
        reply = "The nearest Italian restaurant is Trattoria Roma, 2 minutes away. Should I book a table?"
    elif "lights" in text and ("on" in text or "off" in text):
        state = "on" if "on" in text else "off"
        reply = f"Turning the lights {state} now."
    elif "help" in text or "emergency" in text:
        reply = "Emergency detected. Alerting hotel staff immediately."
    else:
        reply = "I'm not sure about that request, but I’ll ask the staff to assist you shortly."

    return {"reply": reply}

# To run locally
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
