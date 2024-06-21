from flask import Flask, request, render_template, jsonify
from ExtractQuestion import generate_edsl_code


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate_question", methods=["POST"])
def generate_question():
    question_text = request.form["question_text"]
    print("Generate question called")
    question = generate_edsl_code(question_text)
    
    return jsonify({"result": repr(question)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
