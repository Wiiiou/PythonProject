from flask_app import app
from flask import render_template,redirect,session,flash,request
from flask_app.models.admin import Admin
from flask_app.models.voter import Voter
from flask_app.models.candidate import Candidate
# import pandas as pd
from flask_bcrypt import Bcrypt
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

#create a bcrypt variable to acces to the Bcrypt class and use the function to hash the password
bcrypt=Bcrypt(app)

# to show the main page
@app.route('/')
def index():
    return render_template('index.html')

# to display the login admin page where can the admin  login to his only account
@app.route('/login/admin')
def admin_login():
    return render_template('admin.html',session=session)


#this will display the login for the voters only where they can login
@app.route('/login/voter')
def voters_login():
    return render_template('admin.html',session=session)

#this will display the login for the candidate only where they can login
@app.route('/login/candidate')
def candidates_login():
    session['role']='candidate'
    return render_template('admin.html',session=session)

# to validate the select where to locate him
@app.route('/validate',methods=['POST'])
def validate():
    if request.form['role'] == "admin":
        session['role']="admin"
        return redirect('/login/admin')
    elif(request.form['role']=="candidate"):
        session['role']="candidate"
        return redirect('/login/candidate')
    elif request.form['role']=="voter":
        session['role']="voter"
        return redirect('/login/voter')
    else:
        return redirect('/')


#this route where can the we validate the form for the admin if he got his data correct or not
@app.route('/login',methods=['POST'])
def login():
    data={
        **request.form
    }
    if Admin.validate(data): 
        return redirect('/login/dashboard')
    return redirect('/login/admin')

#to show him the admin dashboard
@app.route('/login/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/created')
def show_create():
    return render_template('create_voter.html')


@app.route('/admin/alphacreated')
def show_jmal():
    return render_template('create_candidates.html')
#this route to make the admin to create the voter
@app.route('/admin/create/voter',methods=['POST'])
def create():
    data={
        **request.form
    }
    if Voter.validate(data):
        pw_hash=bcrypt.generate_password_hash(request.form['password'])
        data={**request.form,'password':pw_hash}
        voter_id=Voter.create(data)
        session['voter_id']=voter_id
        return redirect('/admin/dashboard/voters')
    return redirect('/admin/created')

# to check the information that the candidat has entered
@app.route('/admin/create/candidates',methods=['POST'])
def create_cand():
    data={
        **request.form
    }
    if Candidate.validate(data):
        pw_hash=bcrypt.generate_password_hash(request.form['password'])
        data={**request.form,'password':pw_hash}
        cand_id=Candidate.create(data)
        session['cand_id']=cand_id
        return redirect('/candidates')
    return redirect('/admin/alphacreated')

@app.route('/candidates')
def show_candidates():
    all_candidates=Candidate.get_all()
    return render_template('all_candidates.html',all_candidates=all_candidates)


@app.route('/admin/dashboard/voters')
def show_voters():
    voters=Voter.get_all()
    return render_template('voters.html',voters=voters)


# this route for the voters login page where i can check if the email exist or the password in the db
@app.route('/login/voter',methods=['POST'])
def login_voter():
    voter_from_db=Voter.get_voter_by_email({'email':request.form['email']})
    if not voter_from_db:
        flash('Email dosent exit .Pls Try Again',"login")
        return redirect('/login/voter')
    if not bcrypt.check_password_hash(voter_from_db.password,request.form['password']):
        flash('the Password Is Invalid please Try again',"login")
        return redirect('/login/voter')
    if voter_from_db.is_banned==1:
        return redirect('/yourebanned')
    return redirect('/voter/dashboard')


@app.route('/yourebanned')
def bannedpls():
    return render_template('youre_banned.html')
#this route to render me the create pages for the candidate
@app.route('/admin/candidate')
def create_candidate():
    return render_template('create_candidates.html',session=session)

@app.route('/show/candidate/<int:id>')
def show_the_candidate_info(id):
    candidates=Candidate.get_candidate_by_id({"id":id})
    print(candidates)
    if candidates:
        return render_template('Candidate.html',candidates=candidates)
    return redirect('/voter/dashboard')

#this route will show the the dashboard of the voters
@app.route('/voter/dashboard')
def show_candidat_voters():
    return render_template('dashboard_voters.html')

# to get back to the old one
@app.route('/back' , methods=['POST'])
def back():
    session.clear()
    return redirect('/login/dashboard')

#his for banning 
@app.route('/banned/<int:id>', methods=['POST'])
def banned_users(id):
    data={'x':1,'id':id}
    Voter.update(data)
    return redirect('/admin/dashboard/voters')


@app.route('/logout',methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

