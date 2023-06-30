import os
import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
openai.api_key = "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"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        recipe = request.form["recipe"]
        servings = request.form["servings"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(recipe, servings),
            temperature=0.4,
        )
        result = response.choices[0].text.strip()
        return render_template("index.html", result=result)

    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    recipe = request.form["recipe"]
    servings = request.form["servings"]

    # Use OpenAI to generate a response
    prompt = generate_prompt(recipe, servings)
    model = "text-davinci-002"
    completions = openai.Completion.create(engine=model, prompt=prompt, max_tokens=1024)
    response = completions.choices[0].text.strip()

    # Log the response to the console
    print(response)

    # Extract the ingredients and preparation sections from the response
    sections = response.split("##")
    ingredients_section = sections[1].strip()
    preparation_section = sections[2].strip()

    # Format the sections as HTML
    formatted_response = {
        "ingredients": ingredients_section,
        "preparation": preparation_section
    }

    return jsonify(formatted_response)


def generate_prompt(recipe, servings):
    return f"""
    Generate a detailed step-by-step Thermomix TM6 recipe, including all weights, settings, measurements, and times
    for '{recipe}' and for {servings} servings. This must be a recipe specifically for the Thermomix TM6.
    Refer to the settings, accessories and any configuration for the TM6 required.
    Please try to use the Thermomix more than any other appliance where possible.
    Please use fun and conversational language, make it nice and encouraging to read.
    Please make the response in HTML markup. This will be parsed straight into an IDE.
    Please use metric and not imperial.
    Ingredients and Preparation should be <h2>, bullet points for Ingredients and a numbered list for Preparation.
    For all the Thermomix settings please bold the settings:
    e.g. Add egg, milk, and pumpkin puree to the <b>TM bowl and mix for 20 seconds on speed setting 4</b>.
    Use the following format and keep the HTML tags intact and the ## in the response (do not remove or change them):

    ##<h2>Ingredients</h2>
    <li>bullet points of ingredients</li>

    ##<h2>Preparation</h2>
    <ol>numbered list of preparation steps for the Thermomix TM6</ol>
    """
