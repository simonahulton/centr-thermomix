import os
import openai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        recipe = request.form["recipe"]
        servings = request.form["servings"]
        response = generate_response(recipe, servings)
        return render_template("index.html", response=response)

    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    recipe = request.form["recipe"]
    servings = request.form["servings"]
    response = generate_response(recipe, servings)
    return jsonify(response)


def generate_response(recipe, servings):
    prompt = f"""
        Generate a detailed step-by-step Thermomix TM6 recipe, including all weights, settings, measurements, and times
        for '{recipe}' and for {servings} servings. This must be a recipe specifically for the Thermomix TM6.
        Include all TM6 settings, accessories, and any configuration required.
        Include details for the weight/amounts and timings in the instructions.
        Use the Thermomix more than any other appliance where possible.
        Use metric and not imperial. Do not include an introduction or conclusion message - just the format below.
        Bold (using <b> and </b>) only key words (eg ingredients in Preparation section, settings, speeds, accessories, temperatures and times)
        Use the following format and keep the HTML tags I have included intact in the response:
        
        <h2>{recipe}</h2>
        <b>{servings} servings</b>
        
        <h3>Ingredients</h3>
        <li>bullet points of ingredients</li>

        <h3>Thermomix Instructions</h3>
        <li>bullet points of preparation steps for the Thermomix TM6</li>
    """

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": ""}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=1.0,
        n=1,
        stop=None
    )

    assistant_reply = response["choices"][0]["message"]["content"]
    print(f"AI Response: {assistant_reply}")  # Print AI response in the terminal/console
    return {"response": assistant_reply}


if __name__ == "__main__":
    app.run()