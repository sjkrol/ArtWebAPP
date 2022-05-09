import json
import random
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "8w57ghz3TGgIkL_cdqD5BTRt69w"

paintings = ["a-cow-in-a-landscape", 
             "a-saddled-race-horse-tied-to-a-fence-1828",
             "herdsman-with-resting-cattle",
             "hip-hip-hurrah-1888",
             "james-abercromby-of-tullibody-esq-1779",
             "paris-a-rainy-day-1877",
             "tennis-triptych-centre-panel-1930"]

#load art data
with open("static/json/art-info.json") as f:
    art_data = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/experiment")
def experiment():
    return render_template("experiment.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/gallery/painting/<string:image_name>", methods=["GET"])
def painting_data(image_name):
    
    image_name = image_name[1:len(image_name)-5]
    video_name = "/videos/" + image_name + ".mp4"
    session["video_name"] = video_name
    session["painting_name"] = image_name

    return redirect(url_for("painting"))

@app.route("/gallery/painting")
def painting():

    video_name = session["video_name"]
    painting_data = art_data[session["painting_name"]]

    return render_template("painting.html", 
                            video_name=video_name,
                            title=painting_data["Title"],
                            artist=painting_data["Artist"],
                            year=painting_data["Year"],
                            artistpic=painting_data["ArtistPic"],
                            artistDesc=painting_data["ArtistDesc"],
                            artistbirthdeath=painting_data["ArtistBirthDeath"],
                            paintingdesc=painting_data["PaintingDesc"]
                            )

@app.route("/experiment/consent")
def consent():

    return render_template("consent.html")

@app.route("/experiment/demographic", methods=['GET', 'POST'])
def demographic():

    if request.method == 'GET':
        # assign user ID
        participant_id = now = datetime.now().strftime("%d%m%Y%H%M%S")

        session["participant_id"] = participant_id
        session["data"] = {
            "demographic" : {"id" : participant_id, "gender" : None, "age" : None, "lowvision" : None},
            "responses" : []
            }

        return render_template("demographic.html")
    
    if request.method == 'POST':

        demographic = json.loads(request.data)
        session["data"]["demographic"]["age"] = demographic['age']
        session["data"]["demographic"]["lowvision"] = demographic['lowvision']
        if demographic['gender'] == "Other":
            session["data"]["demographic"]["gender"] = demographic['other']
        else:
            session["data"]["demographic"]["gender"] = demographic['gender']
        session["data"]["responses"] = []

        session.modified = True
        
        # set painting index
        session["painting_n"] = 0
        random.shuffle(paintings)

        return 'success', 200

@app.route('/experiment/questions', methods=["GET", "POST"])
def questions():
    
    if request.method == 'GET':

        try:
            painting_name = paintings[session["painting_n"]]
            painting_data = art_data[painting_name]
            video_name = "/videos/" + painting_name + ".mp4"
            template = render_template("questions.html",
                                video_name=video_name,
                                title=painting_data["Title"],
                                artist=painting_data["Artist"],
                                year=painting_data["Year"],
                                paintingdesc=painting_data["PaintingDesc"],
                                painting_n=session["painting_n"])
            session["painting_n"] += 1

        except IndexError:

            filename = f'static/data/{session["data"]["demographic"]["id"]}.json'
            with open(filename, "w") as f:
                json.dump(dict(session["data"]), f)
            template = render_template("thankyou.html")
        return template
    
    if request.method == 'POST':

        responses = json.loads(request.data)
        painting = paintings[session["painting_n"]-1]
        session["data"]["responses"].append({"painting" : painting,
                                             "pleasant" : responses["pleasant"], 
                                             "representative" : responses["representative"]})
        session.modified=True

        return 'success', 200

@app.route('/experiment/questions/back', methods=["POST"])
def experiment_back():

    if request.method == "POST":

        # pop previous data
        session["data"]["responses"].pop()
        painting_n = session["painting_n"]
        painting_n -= 2
        session["painting_n"] = painting_n

        session.modified = True
    
    return 'success', 200

@app.route("/thankyou")
def thankyou():

    return render_template("thankyou.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

