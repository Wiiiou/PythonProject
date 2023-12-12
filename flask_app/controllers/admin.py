from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.models.admin import Admin
from flask_app.models.voter import Voter
from flask_app.models.candidate import Candidate
<<<<<<< HEAD
from flask_app.models.img import Img
import pandas as pd
from flask_bcrypt import Bcrypt
import plotly.express as px
# import plotly.offline as pyo
import pandas as pd
import plotly.express as px

# Your data


# create a bcrypt variable to acces to the Bcrypt class and use the function to hash the password
bcrypt = Bcrypt(app)
=======
# import pandas as pd
from flask_bcrypt import Bcrypt
from flask import jsonify
# import plotly.express as px
# import plotly.offline as pyo

# Create a dictionary with data
# data = {
#     'Name': [],
#     'Percentage': [],  # Numeric values without '%' symbol
#     'City': []
# }

# # Convert the dictionary into a DataFrame


# print(df)
# fig = px.bar(df, x='Name', y='Percentage', hover_data=['City'], barmode='stack')
# fig.update_traces(texttemplate='%{y}%', textposition='outside')  # Add percentage to bars
# fig.update_layout(yaxis_tickformat='%') # Show y-axis in percentage format
# fig.show()
# html_file_path = 'plotly_chart.html'
# pyo.plot(fig, filename=html_file_path, auto_open=False)
>>>>>>> 3c3bf16395b435605074b89d4d06bb470246df0d


# to show the main page
@app.route("/")
def index():
    return render_template("index.html")


@app.route('/show/candidate/plotly.html')
def show_plotly():
    return render_template('plotly.html')


@app.route('/indexhmema.html')
def show_three():
    return render_template('indexhmema.html')

# to display the login admin page where can the admin  login to his only account
@app.route("/login/admin")
def admin_login():
    return render_template("admin.html", session=session)


# this will display the login for the voters only where they can login
@app.route("/login/voter")
def voters_login():
    return render_template("admin.html", session=session)


# this will display the login for the candidate only where they can login
@app.route("/login/candidate")
def candidates_login():
    session["role"] = "candidate"
    return render_template("admin.html", session=session)


@app.route("/login/candidate", methods=["POST"])
def login_candidate_():
    candidate_from_db = Candidate.get_voter_by_email({"email": request.form["email"]})
    session["candidate_id"] = candidate_from_db.id
    if not candidate_from_db:
        flash("Email dosent exit .Pls Try Again", "login")
        return redirect("/login/candidate")
    if not bcrypt.check_password_hash(
        candidate_from_db.password, request.form["password"]
    ):
        flash("the Password Is Invalid please Try again", "login")
        return redirect("/login/candidate")
    # if candidate_from_db.is_banned==1:
    #     return redirect('/yourebanned')
    return redirect(f"/show/candidate/{candidate_from_db.id}")


# to validate the select where to locate him
@app.route("/validate", methods=["POST"])
def validate():
    if request.form["role"] == "admin":
        session["role"] = "admin"
        return redirect("/login/admin")
    elif request.form["role"] == "candidate":
        session["role"] = "candidate"
        return redirect("/login/candidate")
    elif request.form["role"] == "voter":
        session["role"] = "voter"
        return redirect("/login/voter")
    else:
        return redirect("/")


# this route where can the we validate the form for the admin if he got his data correct or not
@app.route("/login", methods=["POST"])
def login():
    data = {**request.form}
    if Admin.validate(data):
        return redirect("/login/dashboard")
    return redirect("/login/admin")


# to show him the admin dashboard
@app.route("/login/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")


@app.route("/admin/created")
def show_create():
    return render_template("create_voter.html")


@app.route("/admin/alphacreated")
def show_jmal():
    return render_template("create_candidates.html")


# this route to make the admin to create the voter
@app.route("/admin/create/voter", methods=["POST"])
def create():
    data = {**request.form}
    voters=Voter.get_all()
    if Voter.validate(data):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {**request.form, "password": pw_hash}
        voter_id = Voter.create(data)
        session["voter_id"] = voter_id
        session['voter_first_time']=1
        Voter.update_first_time({"first_time":session['voter_first_time'],"id":session['voter_id']})
        return redirect("/admin/dashboard/voters")
    return redirect("/admin/created")


# to check the information that the candidat has entered
@app.route("/admin/create/candidates", methods=["POST"])
def create_cand():
    data = {**request.form}
    if Candidate.validate(data):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {**request.form, "password": pw_hash}
        cand_id = Candidate.create(data)
        session["cand_id"] = cand_id
        return redirect("/candidates")
    return redirect("/admin/alphacreated")


@app.route('/voter_change_password')
def change_password_pls():
    return render_template('change_password.html')

#this for the page to change the password after the change this will redirect you to the login page for the candidates
@app.route('/login/change_password/<int:id>', methods=['POST'])
def change_password(id):
    voter=Voter.get_voter_by_id({"id":id})
    data={
        **request.form,"id":id
    }
    print(request.form['new_password'])
    if validate_the_new_password(request.form['new_password']) and request.form['new_password']==request.form['confirm_password']:
        if  not bcrypt.check_password_hash(voter.password,request.form['password']):
            flash('the password you just enterd is not the older password pls try again')
            return redirect('/voter_change_password')
        if request.form['new_password']!=request.form['confirm_password']:
            flash('the password you just entere in not the same Check Pls')
            return redirect('/voter_change_password')
        pw_hash=bcrypt.generate_password_hash(request.form['new_password'])
        data={**request.form,"password":pw_hash,"id":id}
        Voter.update_first(data)
        return redirect('/login/voter')
    return render_template('change_password.html')


@app.route("/candidates")
def show_candidates():
    all_candidates = Candidate.get_all()
    return render_template("all_candidates.html", all_candidates=all_candidates)


# to edit the candidate
@app.route("/edit/candidate/<int:id>")
def edit_candidate(id):
    all_candidates = Candidate.get_candidate_by_id({"id": id})
    return render_template("edit_candidate.html", all_candidates=all_candidates)


@app.route("/edited/candidate/<int:id>", methods=["POST"])
def updated_candidates(id):
    data = {**request.form, "id": id}
    Candidate.update(data)
    return redirect("/candidates")


@app.route("/admin/dashboard/voters")
def show_voters():
    voters = Voter.get_all()
    return render_template("voters.html", voters=voters)

# this route for the voters login page where i can check if the email exist or the password in the db
@app.route("/login/voter", methods=["POST"])
def login_voter():
    voter_from_db = Voter.get_voter_by_email({"email": request.form["email"]})
    if voter_from_db.email!=request.form['email']:
        flash("Email dosent exit .Pls Try Again", "login")
        return redirect("/login/voter")
    if not bcrypt.check_password_hash(voter_from_db.password, request.form["password"]):
        flash("the Password Is Invalid please Try again", "login")
        return redirect("/login/voter")
    if voter_from_db.is_banned == 1:
        return redirect("/yourebanned")
    if voter_from_db.first_time==1:
        session['voter_id']=voter_from_db.id
        return redirect(f"/voter_change_password")
    return redirect("/voter/dashboard")
#""""""""""""""""



@app.route("/yourebanned")
def bannedpls():
    return render_template("youre_banned.html")


# this route to render me the create pages for the candidate
@app.route("/admin/candidate")
def create_candidate():
    return render_template("create_candidates.html", session=session)


# this route where will show the data of the candidate
@app.route("/show/candidate/<int:id>")
def show_the_candidate_info(id):
    candidates = Candidate.get_candidate_by_id({"id": id})
    print(candidates)
    session["candidate_id"] = id
    if candidates:
        return render_template("Candidate.html", candidates=candidates)
    return redirect("/voter/dashboard")


@app.route("/creat/plan/<int:id>")
def redir_plan(id):
    candidates = Candidate.get_candidate_by_id({"id": id})
    return render_template("create_pla.html", candidates=candidates)


@app.route("/create/plans/<int:id>", methods=["POST"])
def create_the_plan(id):
    data = {
        **request.form,
        "id": id,
    }
    print(data)
    if Img.validate(request.form):
        Candidate.update_plan(data)
        Img.save(
            {"file": request.form["file"], "condidate_id": session["candidate_id"]}
        )
        return redirect(f"/show/candidate/{id}")
    return redirect(f"/create/plan/{id}")




#this route where he can see the candidate his  plan
@app.route('/show/plan/<int:id>')
def show_the_plan(id):
    candidate=Candidate.get_candidate_by_id({"id":id})
    img_src=Img.get_img_by_candidate_id({"condidate_id":id,"id":id})
    if candidate:
        return render_template('show_the_plan.html',candidate=candidate,img_src=img_src)
    return redirect('/admin/alphacreated')

@app.route('/edit/plan/<int:id>')
def edit_the_plan(id):
    candidate=Candidate.get_candidate_by_id({"id":id})
    img_src=Img.get_img_by_candidate_id({"condidate_id":id,"id":id})
    if candidate:
        return render_template('edit_the_plan.html',candidate=candidate,img_src=img_src)
    return('/')

@app.route('/edit/plan/<int:id>',methods=['POST'])
def edit_thsi_plan_after(id):
    candidate=Candidate.get_candidate_by_id({"id":id})
    data={
        **request.form,
        "id":id,
        "first_name":candidate.first_name,
        "last_name":candidate.last_name,
        "email":candidate.email,
        "password":candidate.password,
        "birthdate":candidate.birthdate,"region":candidate.region,
    }
    if Candidate.validate(data) or Img.validate(data):
        Candidate.update_whole({"id":id,"bio":request.form['bio'],"plan":request.form['plan']})
        Img.update({"file":request.form['file'],"condidate_id":session['candidate_id'],"id":id})
        return redirect(f'/show/plan/{id}')
    return redirect(f'/edit/plan/{id}')
# this route will show the the dashboard of the voters
@app.route("/voter/dashboard")
def show_candidat_voters():
    candidates = Candidate.get_all()
    return render_template("dashboard_voters.html", candidates=candidates)


# to get back to the old one
@app.route("/back", methods=["POST"])
def back():
    session.clear()
    return redirect("/login/dashboard")


# his for banning
@app.route("/banned/<int:id>", methods=["POST"])
def banned_users(id):
    data = {"x": 1, "id": id}
    Voter.update(data)
    return redirect("/admin/dashboard/voters")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")


<<<<<<< HEAD




#this for validations for the new password because we dont have in our database
def validate_the_new_password(password):
    is_valid=True
    countM=0
    countm=0
    countnumber=0
    for i in range(len(password)):
        if "A"<=password[i]<="Z":
            countM+=1
        elif "a"<=password[i]<="z":
            countm+=1
        else:
            countnumber+=1
    if countM==0 or countm==0 or countnumber==0:
        is_valid=False
    return is_valid
=======
@app.route('/vote',methods=['POST'])
def voter():
    data={
        **request.form
    }
    res=Voter.vote(data)
    return res
    
@app.route('/show/candidate/votes/<int:id>')
def show_the_candidate_votes(id):
    vote_count = Candidate.get_candidate_votes({"id": id})
    

    if vote_count is not None:
        return jsonify({'candidate_id': id, 'vote_count': vote_count})
    else:
        return jsonify({'message': 'No votes found for the candidate ','candidat':id}), 404
>>>>>>> 3c3bf16395b435605074b89d4d06bb470246df0d
