from pydantic import BaseModel

class TrafficInput(BaseModel):
    packet_ratio: float
    high_activity: int
