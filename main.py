from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functions import func
import os
from constants import AUTH_ADMIN_CODES

app = Flask(__name__)
app.secret_key = 'lmao'


@app.route('/')
def index():
    return render_template('index.html')



@app.route("/<role>/new_user", methods=['POST'])
def regpt(role):
    name = request.form['rname']
    email = request.form['remail']
    password = request.form['rpassword']
    if role == 'admin':
        if request.form['admincode'] not in AUTH_ADMIN_CODES:
            return render_template('admin.html', error="Invalid Admin Code")
        if func.check_admin_exists(email):
            return render_template('admin.html', error="User already exists")
        if func.new_admin(name, email, password):
            session['user'] = email
            session['username'] = name
            return redirect(url_for('loginpage', role=role))
        return render_template('admin.html', error="Error Occured")
    if role == 'user':
        phone = request.form['rphone']
        if func.check_user_exists(email):
            return render_template('user.html', error="User already exists")
        if func.add_newuser(name, email, password, phone):
            session['user'] = email
            session['username'] = name
            return redirect(url_for('loginpage', role=role))
        return render_template('user.html', error="Error Occured")
    if role == 'agent':
        job = request.form['assigned_partner']
        if func.check_agent_exists(email):
            return render_template('agent.html', error="User already exists")
        if func.new_agent(name, email, password, job):
            session['user'] = email
            session['username'] = name
            return redirect(url_for('loginpage', role=role))
        return render_template('agent.html', error="Error Occured")



@app.route("/<role>/login")
def loginpage(role):
    return render_template(role+'.html', role=role)

@app.route("/<role>/login", methods=['POST'])
def loginpost(role):
    email = request.form['email']
    password = request.form['password']
    if role == 'agent':
        if func.check_agent(email, password):
            session['user'] = email
            return redirect('/agent/home')
        return render_template(role+'.html', error="Invalid Credentials")
    if role == 'user':
        if func.check_user(email, password):
            session['user'] = email
            return redirect('/user/home')
        return render_template(role+'.html', error="Invalid Credentials")
    if role == 'admin':
        if func.check_admin(email, password):
            session['user'] = email
            return redirect('/admin/home')
        return render_template(role+'.html', error="Invalid Credentials")
            


@app.route('/<role>/home')
def usrhome(role):
    if not session.get('user'):
        return redirect(url_for('loginpage', role=role))
    if role == 'user':
        usercomplaints = func.get_user_complaints(session.get('user'))
        return render_template('userhome.html', username=session.get('user'), complaints=usercomplaints)
    if role == 'admin':
        complaints = func.get_all_complaints()
        partners = func.fetch_agents()   
        return render_template('adminhome.html', username=session.get("user"), complaints=complaints, partners=partners)
    if role == 'agent':
        complaints = func.get_tasks(session.get('user'))
        return render_template('agenthome.html', username=session.get("user"), complaints=complaints)




@app.route("/assign-partner", methods=['POST'])
def assginepartner():
    if not session.get('user'):
        return redirect(url_for('loginpage', role='admin'))
    id = request.args.get('id')
    partner = request.form['assigned-partner']
    func.assigntask(id, partner)
    complaints = func.get_all_complaints()
    partners = func.fetch_agents()   
    return  render_template("adminhome.html", message="Partner Assigned", complaints=complaints, partners=partners)

@app.route("/<role>/delete-issue", methods=['POST'])
def deletecomp(role):
    if not session.get('user'):
        return redirect(url_for('loginpage', role='admin'))
    id = request.args.get('id')
    func.deletecomplaint(id)
    complaints = func.get_all_complaints()
    partners = func.fetch_agents()   
    if role == 'user':
        return render_template("userhome.html", message="Complaint Deleted", complaints=complaints)
    return render_template("adminhome.html", message="Complaint Deleted", complaints=complaints, partners=partners)




@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    if not session.get('user'):
        return redirect(url_for('loginpage', role='admin'))
    file = request.files['complaint_image']
    title = request.form['complaint_type']
    description = request.form['complaint_description']
    latitute = request.form['latitude']
    longitute = request.form['longitude']
    location_details = request.form['location_details']
    mail = session.get('user')
    print(title, description, latitute, longitute, location_details, mail)
    if file.filename == '':
        return render_template("userhome.html", message="No file selected")
    if file:
        ticketid = func.generate_random_string(10)
        filename = f"temp/{ticketid}.jpg"
        file.save(filename)
        image_url = func.upload_file(filename)
        func.new_complaint(title, description, mail, image_url, latitute, longitute, location_details, ticketid)
        os.remove(filename)
        return render_template("userhome.html", message=f"Complaint Submitted Successfully. Ticket ID: {ticketid}")
    return render_template('userhome.html')


@app.route("/update", methods=['POST'])
def imgupdate():
    if not session.get('user'):
        return redirect(url_for('loginpage', role='agent'))
    complaints = func.get_tasks(session.get('user'))
    file = request.files['image_after']
    progress = request.form['progress']
    id = request.form['complaint_id']
    print(progress, id)
    if file.filename == '':
        return render_template("userhome.html", message="No file selected")
    if file:
        ticketid = func.generate_random_string(10)
        filename = f"temp/{ticketid}.jpg"
        file.save(filename)
        image_url = func.upload_file(filename)
        func.update_status(id, progress, image_url)
        os.remove(filename)
        return render_template("agenthome.html", message=f"Complaint Upated Successfully.", complaints=complaints)
    return render_template('agenthome.html', complaints=complaints, message="Error Occured")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact", methods=['POST'])
def contactpost():
    return render_template("contact.html", message="Message Sent Successfully")

@app.route("/logout")
def logout():
    session['user'] = None
    return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
