# Importing libraries
from fastapi import FastAPI, HTTPException
import requests
import httpx
import base64

app = FastAPI()

# Endpoint to obtain an image from AI Model 1, send it to Model 2, and then send it to Spring Boot API
@app.post("/process_images")
async def process_images():
    try:
        # Endpoint of AI Model 1
        ai_model1_endpoint = ""
        response_model1 = requests.post(ai_model1_endpoint)
        # Check for successful response
        response_model1.raise_for_status()

        # Get the image from AI Model 1
        result_from_model1 = response_model1.content
        result_from_model1_base64 = base64.b64encode(result_from_model1).decode("utf-8")

        # Endpoint of AI Model 2
        ai_model2_endpoint = ""
        # Send the image to AI Model 2
        response_model2 = requests.post(ai_model2_endpoint, json={"image": result_from_model1_base64})

        # Check for successful response
        response_model2.raise_for_status()

        # Get the result from AI Model 2
        result_from_model2 = response_model2.json()["result"]

        # Send image and result to Spring Boot API
        async with httpx.AsyncClient() as client:
            response_spring_boot = await client.post(
                "",
                json={"image_model2": result_from_model2}
            )

        # Check for a successful response
        response_spring_boot.raise_for_status()

        return {"status": "Successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Endpoint om een afbeelding van AI Model 1 te verkrijgen, naar Model 2 te sturen en naar Spring Boot API te verzenden
# @app.post("/process_images")
# async def process_images(image_model1: UploadFile = File(...), timestamp: str = None):
#     try:
#         result_from_model1 = await image_model1.read()
#         result_from_model1_base64 = base64.b64encode(result_from_model1).decode("utf-8")

#         # Define the endpoint of AI Model 2
#         ai_model2_endpoint = "http://ai-model2-endpoint/process_image"

#         # Send the image to AI Model 2
#         response = requests.post(ai_model2_endpoint, json={"image": result_from_model1_base64})

#         #check for successful response
#         response.raise_for_status()

#         # Get the result from AI Model 2
#         result_from_model2 = response.json()["result"]

#        # Send image and result to Spring Boot API
#         async with httpx.AsyncClient() as client:
#           response = await client.post(
#               "http://spring-boot-api/submit_data",
#               json={"image_model2": result_from_model2, "timestamp": timestamp}
#           )


#         # Controleer op een succesvolle respons
#         response.raise_for_status()

#         return {"status": "Successful"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

