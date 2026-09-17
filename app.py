from fastapi import FastAPI, HTTPException

app = FastAPI()

readings = [
    {"name": "front-door", "room": "hall",    "temp": 27.4, "online": True},
    {"name": "hall-lamp",  "room": "hall",    "temp": 26.1, "online": True},
    {"name": "attic",      "room": "attic",   "temp": 31.9, "online": True},
    {"name": "fridge",     "room": "kitchen", "temp": 4.2,  "online": False},
    {"name": "patio",      "room": "outside", "temp": 29.8, "online": True},
]

def hottest(data: list[dict]) -> dict:
    if not data:
        raise HTTPException(status_code=444, detail="No readings available")
    # Python's built-in max function directly finds the item with the highest temp
    return max(data, key=lambda item: item["temp"])

def average_temp(R):
        temp = 0
        for index, item in enumerate(R):
            for key, value in R[index].items():
                if key == "temp":
                    temp = temp + value 
        avg_temp = temp/len(readings)
        return round(avg_temp, 2)

def only_online(data: list[dict]):
    online_list = []
    for index, item in enumerate(readings):
        for key, value in readings[index].items():
            if value == True:
                online_list.append(readings[index])
    return online_list

@app.get("/devices")
async def all_devices():
    return readings

@app.get("/devices/hottest")
async def hottest_devices():
    return hottest(readings)

@app.get("/devices/online")
async def online_devices():
    return only_online(readings)

@app.get("/devices/{name}")  
async def get_name(name):  
    for item in readings:
        if item["name"] == name:
            return item 
    raise HTTPException(status_code=404, detail=f"No device called '{name}' ")

@app.get("/stats")
async def temp_avg():
    return {"average_temperature": average_temp(readings)}
 