from fastapi import FastAPI, Request
import uvicorn
import requests
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title><center>Welcome to Health and wellness<center></title>
    </head>
    <body>
        <h1><center>HEALTH AND WELLNESS AWARENESS<center><h1>
        <h1>Welcome to Nutrition Information</h1>
        <p>This is a simple web application to retrieve nutrition information about various foods.</p>
        <p>To get started, you can visit the <a href="/nutrition">Nutrition Information</a> page.</p>
        <h1>Welcome to fitness-plans</h1>
        <p>This is a simple web application to retrieve fitness plans.</p>
        <p>To get started, you can visit the <a href="/fitness-plans">Fitness plans</a> page.</p>
        <h1>Welcome to Wellness</h1>
        <p>This is a simple web application to get some daily wellness quotes.</p>
        <p>To get started, you can visit the <a href="/wellness">Wellness</a> page.</p>
        <h1>Welcome to BMI calculator</h1>
        <p>This is a simple web application to calculation for BMI.</p>
        <p>To get started, you can visit the <a href="/bmi">Body mass index calculator</a> page.</p>
        <h1>Welcome to Calorie counter</h1>
        <p>This is a simple web application to count calories for a specific sport.</p>
        <p>To get started, you can visit the <a href="/calories-burnt">Calories Information</a> page.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/nutrition", response_class=HTMLResponse)
async def read_nutrition():
    url = "https://food-nutrition-information.p.rapidapi.com/food/1497465"
    headers = {
        "X-RapidAPI-Key": "17edc9d6f6msh25ea0148751b3e0p199bfbjsn8a8444c2a448",
        "X-RapidAPI-Host": "food-nutrition-information.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    html_content = "<!DOCTYPE html><html><head><title>Nutrition Information</title></head><body>"
    html_content += "<h1>Nutrition Information</h1>"
    html_content += "<p><strong>Description:</strong> {}</p>".format(data["description"])
    html_content += "<p><strong>Brand Name:</strong> {}</p>".format(data["brandName"])
    html_content += "<p><strong>Serving Size:</strong> {} {}</p>".format(data["servingSize"], data["servingSizeUnit"])
    html_content += "<h2>Nutrients:</h2>"
    html_content += "<ul>"
    for nutrient in data["foodNutrients"]:
        html_content += "<li><strong>{}</strong>: {} {}</li>".format(nutrient["nutrient"]["name"], nutrient["amount"],
                                                                     nutrient["nutrient"]["unitName"])
    html_content += "</ul>"
    html_content += "</body></html>"

    return HTMLResponse(content=html_content)


@app.get("/fitness-plans", response_class=HTMLResponse)
async def read_fitness_plans(request: Request):
    url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/chest"
    headers = {
        "X-RapidAPI-Key": "17edc9d6f6msh25ea0148751b3e0p199bfbjsn8a8444c2a448",
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    html_content = "<!DOCTYPE html><html><head><title>Fitness Plans</title></head><body>"

    for exercise in data:
        html_content += "<h2>{}</h2>".format(exercise["name"])
        html_content += "<p><strong>Body Part:</strong> {}</p>".format(exercise["bodyPart"])
        html_content += "<p><strong>Equipment:</strong> {}</p>".format(exercise["equipment"])
        html_content += "<img src='{}' alt='Exercise GIF'>".format(exercise["gifUrl"])
        html_content += "<h3>Instructions:</h3>"
        html_content += "<ol>"
        for instruction in exercise["instructions"]:
            html_content += "<li>{}</li>".format(instruction)
        html_content += "</ol>"

    html_content += "</body></html>"

    return HTMLResponse(content=html_content)


@app.get("/wellness", response_class=HTMLResponse)
async def read_wellness():
    url = "https://positivity-tips.p.rapidapi.com/api/positivity/wellness"
    headers = {
        "X-RapidAPI-Key": "17edc9d6f6msh25ea0148751b3e0p199bfbjsn8a8444c2a448",
        "X-RapidAPI-Host": "positivity-tips.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    html_content = "<!DOCTYPE html><html><head><title>Wellness Tip</title></head><body>"
    html_content += "<h1>Wellness Tip</h1>"
    html_content += "<p>{}</p>".format(data["tip"])
    html_content += "</body></html>"

    return HTMLResponse(content=html_content)


@app.get("/bmi", response_class=HTMLResponse)
async def calculate_bmi():
    url = "https://body-mass-index-bmi-calculator.p.rapidapi.com/metric"
    querystring = {"weight": "140", "height": "1.83"}
    headers = {
        "X-RapidAPI-Key": "17edc9d6f6msh25ea0148751b3e0p199bfbjsn8a8444c2a448",
        "X-RapidAPI-Host": "body-mass-index-bmi-calculator.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    bmi_data = response.json()

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BMI Calculator Result</title>
    </head>
    <body>
        <h1>BMI Calculator Result</h1>
        <p><strong>Weight:</strong> {} kg</p>
        <p><strong>Height:</strong> {} m</p>
        <p><strong>BMI:</strong> {}</p>
    </body>
    </html>
    """.format(querystring["weight"], querystring["height"], bmi_data["bmi"])

    return HTMLResponse(content=html_content)


@app.get("/calories-burnt", response_class=HTMLResponse)
async def get_calories_burnt(request: Request):
    url = "https://calories-burned-by-api-ninjas.p.rapidapi.com/v1/caloriesburned"
    querystring = {"activity": "cricket"}
    headers = {
        "X-RapidAPI-Key": "17edc9d6f6msh25ea0148751b3e0p199bfbjsn8a8444c2a448",
        "X-RapidAPI-Host": "calories-burned-by-api-ninjas.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    # Assuming the activity name and total calories burnt are the first item in the response
    activity = data[0]["name"]
    calories = data[0]["total_calories"]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Calories Burnt</title>
    </head>
    <body>
        <h1>Calories Burnt</h1>
        <p>Activity: {activity}</p>
        <p>Calories Burnt per hour: {calories}</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
