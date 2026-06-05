from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.wrappers import Response
from flask_wtf.csrf import CSRFProtect  # type: ignore
import requests
import uuid
import qrcode  # type: ignore
from io import BytesIO
import base64
from datetime import datetime
from typing import Union, List, TypedDict

class PollOption(TypedDict):
    text: str
    votes: int
    percentage: int

class Poll(TypedDict):
    question: str
    options: List[PollOption]
    created_at: str

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Change this in production
app.config['WTF_CSRF_SECRET_KEY'] = 'anothersupersecretkey'  # Change this in production
csrf = CSRFProtect(app)

# Backend base URL
BACKEND_URL = "http://localhost:8080/api"

@app.after_request
def after_request(response: Response) -> Response:
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    return response

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create-poll", methods=["GET", "POST"])
def create_poll():
    if request.method == "POST":
        question = request.form.get("question")
        options = request.form.getlist("option")
        poll_id = str(uuid.uuid4())[:8].upper()
        
        # In a real application, save to database
        # For now, we'll just use session
        if "polls" not in session:
            session["polls"] = {}
            
        session["polls"][poll_id] = {
            "question": question,
            "options": [{"text": opt, "votes": 0} for opt in options if opt],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        session.modified = True
        
        return redirect(url_for("poll_created", poll_id=poll_id))
        
    return render_template("create_poll.html")

@app.route("/poll-created/<poll_id>")
def poll_created(poll_id: str) -> Union[str, Response]:
    if "polls" not in session or poll_id not in session["polls"]:
        flash("Poll not found")
        return redirect(url_for("home"))
        
    # Generate QR code
    poll_link = request.host_url + "poll/" + poll_id
    img = qrcode.make(poll_link)
    buffered = BytesIO()
    img.save(buffered)
    qr_img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return render_template(
        "poll_created.html", 
        poll_id=poll_id,
        poll_link=poll_link,
        qr_code=qr_img_str
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            res = requests.post(f"{BACKEND_URL}/auth/login", json={"username": username, "password": password})
            if res.status_code == 200:
                session["user"] = res.json()
                return redirect(url_for("vote"))
            else:
                flash("Login failed")
        except Exception as e:
            flash(f"Error: {e}")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            res = requests.post(f"{BACKEND_URL}/auth/register", json={"username": username, "password": password})
            if res.status_code == 200:
                flash("Registered successfully. Please log in.")
                return redirect(url_for("login"))
            else:
                flash("Registration failed")
        except Exception as e:
            flash(f"Error: {e}")
    return render_template("register.html")

@app.route("/poll/<poll_id>", methods=["GET", "POST"])
def view_poll(poll_id: str) -> Union[str, Response]:
    if "polls" not in session or poll_id not in session["polls"]:
        flash("Poll not found")
        return redirect(url_for("join_poll"))
    
    poll = session["polls"][poll_id]  # type: ignore
    
    if request.method == "POST":
        option_index = int(request.form.get("option", -1))
        if 0 <= option_index < len(poll["options"]):  # type: ignore
            poll["options"][option_index]["votes"] += 1
            session.modified = True
            return redirect(url_for("poll_thanks", poll_id=poll_id))
        else:
            flash("Please select an option")
    
    return render_template("view_poll.html", poll=poll, poll_id=poll_id)

@app.route("/poll/<poll_id>/thanks")
def poll_thanks(poll_id: str) -> str:
    return render_template("poll_thanks.html")

@app.route("/poll/<poll_id>/results")
def poll_results(poll_id: str) -> Union[str, Response]:
    if "polls" not in session or poll_id not in session["polls"]:
        flash("Poll not found")
        return redirect(url_for("join_poll"))
    
    poll = session["polls"][poll_id]  # type: ignore
    total_votes = sum(option["votes"] for option in poll["options"])  # type: ignore
    
    # Calculate percentages if there are any votes
    if total_votes > 0:
        for option in poll["options"]:  # type: ignore
            option["percentage"] = round((option["votes"] / total_votes) * 100)  # type: ignore
    else:
        for option in poll["options"]:  # type: ignore
            option["percentage"] = 0
    
    return render_template("poll_results.html", poll=poll, poll_id=poll_id, total_votes=total_votes)

@app.route("/join-poll", methods=["GET", "POST"])
def join_poll():
    if request.method == "POST":
        poll_id = request.form.get("poll_id", "").strip().upper()
        if "polls" in session and poll_id in session["polls"]:
            return redirect(url_for("view_poll", poll_id=poll_id))
        else:
            flash("Poll not found. Please check the ID or link.")
    
    return render_template("join_poll.html")

@app.route("/vote", methods=["GET", "POST"])
def vote():
    if "user" not in session:
        return redirect(url_for("login"))
    candidates = []
    try:
        res = requests.get(f"{BACKEND_URL}/results")
        if res.status_code == 200:
            candidates = res.json()
        if not candidates:
            flash("No candidates available for voting. Please contact admin.")
            return render_template("vote.html", candidates=[])
    except Exception as e:
        flash(f"Error loading candidates: {e}")
        return render_template("vote.html", candidates=[])
    
    if request.method == "POST":
        if "candidate" not in request.form:
            flash("Please select a candidate to vote")
            return render_template("vote.html", candidates=candidates)
        try:
            candidate_id = request.form["candidate"]
            res = requests.post(f"{BACKEND_URL}/vote/submit", json={
                "userId": session["user"]["userId"],  # type: ignore
                "candidateId": int(candidate_id)
            })
            if res.status_code == 200:
                flash("Vote submitted!")
            else:
                flash("Voting failed")
        except Exception as e:
            flash(f"Error: {e}")
    return render_template("vote.html", candidates=candidates)

@app.route("/admin")
def admin():
    votes = []
    try:
        res = requests.get(f"{BACKEND_URL}/admin/votes")
        if res.status_code == 200:
            votes = res.json()
    except Exception as e:
        flash(f"Error loading votes: {e}")
    return render_template("admin.html", votes=votes)

@app.route("/admin/add_candidate", methods=["POST"])
def admin_add_candidate():
    name = request.form.get("name")
    if not name:
        flash("Candidate name is required")
        return redirect(url_for("admin"))
    try:
        res = requests.post(f"{BACKEND_URL}/admin/candidates", json={"name": name})
        if res.status_code == 200:
            flash(f"Added candidate: {name}")
        else:
            flash("Failed to add candidate")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect(url_for("admin"))

@app.route("/admin/remove_candidate/<int:candidate_id>", methods=["POST"])
def admin_remove_candidate(candidate_id: int) -> Response:
    try:
        res = requests.delete(f"{BACKEND_URL}/admin/candidates/{candidate_id}")
        if res.status_code == 200:
            flash("Candidate removed")
        else:
            flash("Failed to remove candidate")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect(url_for("admin"))

@app.route("/admin/reset_votes", methods=["POST"])
def admin_reset_votes():
    try:
        res = requests.delete(f"{BACKEND_URL}/admin/votes/reset")
        if res.status_code == 200:
            flash("All votes have been reset")
        else:
            flash("Failed to reset votes")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect(url_for("admin"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
