from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from addressverification import verifyaddress
import os

# create a FastAPI instance
app = FastAPI()

@app.post('/verifyaddresssmarty')
async def verifyaddresssmarty(request: Request):

    try:
    #     read the JSON data from the GET request
        request_data = await request.json()

        lookupadress = {
            "input_id": request_data["input_id"],
            "street": request_data["street"],
            "street2": request_data["street2"],
            "city": request_data["city"],
            "state": request_data["state"],
            "zipcode": request_data["zipcode"]
        }

        # process the JSON data
        op = verifyaddress(lookupadress)

        # return the result
        return JSONResponse(op)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={'detail': e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': f'An unexpected error occurred : {e}'})


@app.get('/health')
async def health_check():
    build_tag = os.getenv("BUILD_TAG", "dev")
    return JSONResponse(content={"status": "ok", "build_tag": f"{build_tag}"})
