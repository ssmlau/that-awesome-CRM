from flask import Flask, render_template, request, url_for, redirect
import sys
import pyrebase

config = {
    "apiKey": "AIzaSyApbbE90LsWekODFSlRLDz4nOIegHajMSc",
    "authDomain": "cs490-e9fd5.firebaseapp.com",
    "databaseURL": "https://cs490-e9fd5.firebaseio.com",
    "projectId": "cs490-e9fd5",
    "storageBucket": "",
    "messagingSenderId": "1073025923441",
    "appId": "1:1073025923441:web:1e5196bf90ba1485"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

HRconfig = {
    "apiKey": "AIzaSyCNkrsI8P9HH63yxZSDmvAEL4-vu6c8wl0",
    "authDomain": "recruitment-6cae5.firebaseapp.com",
    "databaseURL": "https://recruitment-6cae5.firebaseio.com",
    "projectId": "recruitment-6cae5",
    "storageBucket": "recruitment-6cae5.appspot.com",
    "messagingSenderId": "307067666683",
    "appId": "1:307067666683:web:39e93a69988eacbc"
}

HRfirebase = pyrebase.initialize_app(HRconfig)
HRdb = HRfirebase.database()

app = Flask(__name__)
app.config['useremail'] = None
app.config['nameofuser'] = None
app.config['consultantid'] = None

@app.route('/')
def index():
    return render_template('login.html')

###
# Login
###

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        resultdict = dict(request.form)
        user = auth.sign_in_with_email_and_password(resultdict['Username'], resultdict['Password'])

        queryresult = HRdb.child("employees").order_by_child("email").equal_to(resultdict['Username']).limit_to_first(1).get()
        queryresultval = queryresult.val()

        key = list(queryresultval)[0]
        name = queryresultval[key]['name']

        app.config['useremail'] = resultdict['Username']
        app.config['nameofuser'] = name
        app.config['consultantid'] = key

        # Post to other MIS
        HRdb.child("functionalcrm").push(key)

        return mainPage()
    else:
        return render_template('login.html')

@app.route('/signup', methods = ['POST'])
def signup():
    if request.method == 'POST':
        result = request.form
        resultdict = dict(request.form)
        user = auth.create_user_with_email_and_password(resultdict['Username'], resultdict['Password'])

        return render_template('index.html')
    else:
        return render_template('register.html')
    

# Created different functions for each datatype, assuming there will be specific things we need for each
# Placeholder functions with basic functionality for now

###
# Clients
###

@app.route('/addclient', methods = ['POST'])
def add_client():
    if request.method == 'POST':
        result = request.form
        resultdict = dict(request.form)
        iddict = db.child("clients").push(resultdict)
        #To add own id key
        #db.child("clients").child(1).set(new_client)
        # return render_template('clientpage.html', result = result, id = iddict['name'])
        return clientPage(iddict['name'])


@app.route('/updateclient', methods = ['POST'])
def update_client():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        resultdict = dict(request.form)
        del resultdict['ID']
        db.child("clients").child(id).update(resultdict)
        # return render_template('clientpage.html', result = result, id = id)
        return clientPage(id)

"""
@app.route('/removeclient', methods = ['POST'])
def remove_client():
    if request.method == 'POST':
        id_token = currentUser.getIdToken(True)
        claims = auth.verify_id_token(id_token)
        if claims['admin'] is True:
            result = request.form
            id = result['ID']
            db.child("clients").child(id).remove()
            return render_template('viewclient.html', result = result)
"""

@app.route('/deleteclient/<clientid>', methods = ['GET'])
def delete_client(clientid):
    # id_token = currentUser.getIdToken(True)
    # claims = auth.verify_id_token(id_token)
    # if claims['admin'] is True:
    db.child("clients").child(clientid).remove()
    # return redirect(url_for('mainPage'))
    return mainPage()

@app.route('/getclient', methods = ['POST'])
def get_client_info():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        info = db.child("clients").child(id).get()
        return render_template('clientpage.html', result = info.val(), id = id)

@app.route('/allclients', methods = ['GET', 'POST'])
def allclients():
        allclientsinfo = db.child("clients").get()
        return allclientsinfo

###
# Interactions
###

@app.route('/addinteraction', methods = ['POST'])
def add_interaction():
    if request.method == 'POST':
        result = request.form
        resultdict = dict(request.form)
        iddict = db.child("interactions").push(resultdict)
        #To add own id key
        #db.child("clients").child(1).set(new_client)
        return render_template('interactionpage.html', result = result, id = iddict['name'], comments=None)

@app.route('/updateinteraction', methods = ['POST'])
def update_interaction():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        resultdict = dict(request.form)
        del resultdict['ID']
        db.child("interactions").child(id).update(resultdict)
        return render_template('interactionpage.html', result = result, id = id)

"""
@app.route('/removeinteraction', methods = ['POST'])
def remove_interaction():
    if request.method == 'POST':
        id_token = currentUser.getIdToken(True)
        claims = auth.verify_id_token(id_token)
        if claims['admin'] is True:
            result = request.form
            id = result['ID']
            db.child("interactions").child(id).remove()
            return render_template('viewinteraction.html', result = result)
"""

@app.route('/deleteinteraction/<clientid>/<interactionid>', methods = ['GET'])
def delete_interaction(clientid, interactionid):
    # if request.method == 'POST':
    #     id_token = currentUser.getIdToken(True)
    #     claims = auth.verify_id_token(id_token)
    #     if claims['admin'] is True:
    #         result = request.form
    #         id = result['ID']
    db.child("interactions").child(interactionid).remove()
    return clientPage(clientid)

@app.route('/getinteraction', methods = ['POST'])
def get_interaction():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        info = db.child("interactions").child(id).get()
        return render_template('interactionpage.html', result = info.val(), id = id)

@app.route('/interactionsbyconsultant', methods = ['POST'])
def get_interactions_by_consultant():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        info = db.child("interactions").order_by_child("Consultant ID").equal_to(id).get()
        if info.pyres:
                return render_template('viewinteractionsbyconsultant.html', result = info.val())
        else:
                return render_template('viewinteractionsbyconsultant.html', id = id)

@app.route('/interactionsbyclient', methods = ['POST'])
def get_interactions_by_client():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        print(id)
        info = db.child("interactions").order_by_child("Client ID").equal_to(id).get()
        if info.pyres:
                return render_template('viewinteractionsbyclient.html', result = info.val())
        else:
                return render_template('viewinteractionsbyclient.html', id = id)

###
# Issues
###

@app.route('/addissue', methods = ['POST'])
def add_issue():
    if request.method == 'POST':
        result = request.form
        resultdict = dict(request.form)
        iddict = db.child("issues").push(resultdict)
        #To add own id key
        #db.child("clients").child(1).set(new_client)
        return render_template('issuepage.html', result = result, id = iddict['name'], comments=None)

@app.route('/updateissue', methods = ['POST'])
def update_issue():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        resultdict = dict(request.form)
        del resultdict['ID']
        db.child("issues").child(id).update(resultdict)
        return render_template('issuepage.html', result = result, id = id)

"""
@app.route('/removeissue', methods = ['POST'])
def remove_issue():
    if request.method == 'POST':
        id_token = currentUser.getIdToken(True)
        claims = auth.verify_id_token(id_token)
        if claims['admin'] is True:
            result = request.form
            id = result['ID']
            db.child("issues").child(id).remove()
            return render_template('viewissue.html', result = result)
"""

@app.route('/deleteissue/<clientid>/<issueid>', methods = ['GET'])
def delete_issue(clientid, issueid):
    # if request.method == 'POST':
    #     id_token = currentUser.getIdToken(True)
    #     claims = auth.verify_id_token(id_token)
    #     if claims['admin'] is True:
    #         result = request.form
    #         id = result['ID']
    db.child("issues").child(issueid).remove()
    return clientPage(clientid)

@app.route('/getissue', methods = ['POST'])
def get_issue():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        info = db.child("issues").child(id).get()
        return render_template('issuepage.html', result = info.val(), id = id)

@app.route('/issuesbyclient', methods = ['POST'])
def get_issues_by_client():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        info = db.child("issues").order_by_child("Client ID").equal_to(id).get()
        if info.pyres:
                return render_template('viewissuesbyclient.html', result = info.val())
        else:
                return render_template('viewissuesbyclient.html', id = id)

###
# Projects
###

@app.route('/addproject', methods = ['POST'])
def add_project():
    if request.method == 'POST':
        result = request.form
        resultdict = dict(request.form)
        iddict = db.child("projects").push(resultdict)
        #To add own id key
        #db.child("clients").child(1).set(new_client)
        return render_template('projectpage.html', result = result, id = iddict['name'], comments=None)

@app.route('/updateproject', methods = ['POST'])
def update_project():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        resultdict = dict(request.form)
        del resultdict['ID']
        db.child("projects").child(id).update(resultdict)
        return render_template('projectpage.html', result = result, id = id)

"""
@app.route('/removeproject', methods = ['POST'])
def remove_project():
    if request.method == 'POST':
        id_token = currentUser.getIdToken(True)
        claims = auth.verify_id_token(id_token)
        if claims['admin'] is True:
            result = request.form
            id = result['ID']
            db.child("projects").child(id).remove()
            return render_template('viewproject.html', result = result)
"""

@app.route('/deleteproject/<clientid>/<projectid>', methods = ['GET'])
def delete_project(clientid, projectid):
    # if request.method == 'POST':
    #     id_token = currentUser.getIdToken(True)
    #     claims = auth.verify_id_token(id_token)
    #     if claims['admin'] is True:
    #         result = request.form
    #         id = result['ID']
    db.child("projects").child(projectid).remove()
    return clientPage(clientid)      

@app.route('/getproject', methods = ['POST'])
def get_project():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        info = db.child("projects").child(id).get()
        return render_template('projectpage.html', result = info.val(), id = id)

@app.route('/projectsbyconsultant', methods = ['POST'])
def get_projects_by_consultant():
    if request.method == 'POST':
        result = request.form
        id = str(result['ID'])
        info = db.child("projects").order_by_child("Consultant ID").equal_to(id).get()
        if info.pyres:
                return render_template('viewprojectsbyconsultant.html', result = info.val())
        else:
                return render_template('viewprojectsbyconsultant.html', id = id)

@app.route('/projectsbyclient', methods = ['POST'])
def get_projects_by_client():
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        info = db.child("projects").order_by_child("Client ID").equal_to(id).get()
        if info.pyres:
                return render_template('viewprojectsbyconsultant.html', result = info.val())
        else:
                return render_template('viewprojectsbyconsultant.html', id = id)

@app.route('/redirect/<link>', methods = ['POST', 'GET'])
def redirect(link):
    if request.method == 'GET':
        return render_template(link)

### Comments
# Should check/make sure it's ordered by time?
@app.route('/addcommentissue/<issueid>', methods = ['POST', 'GET'])
def addcommentissue(issueid):
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        name = result['Name']
        comment = result['Comment']
        data = {"Comment": comment, "Name": name}
        info = db.child("issues").child(id).child("Comments").push(data)
        return issuePage(issueid)

@app.route('/addcommentinteraction/<interactionid>', methods = ['POST', 'GET'])
def addcommentinteraction(interactionid):
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        name = result['Name']
        comment = result['Comment']
        data = {"Comment": comment, "Name": name}
        info = db.child("interactions").child(id).child("Comments").push(data)
        return interactionPage(interactionid)

@app.route('/addcommentproject/<projectid>', methods = ['POST', 'GET'])
def addcommentproject(projectid):
    if request.method == 'POST':
        result = request.form
        id = result['ID']
        name = result['Name']
        comment = result['Comment']
        data = {"Comment": comment, "Name": name}
        info = db.child("projects").child(id).child("Comments").push(data)
        return projectPage(projectid)


#****************
# Link Routing
#****************

@app.route('/mainpage', methods = ['POST', 'GET'])
def mainPage():
        print(app.config['useremail'])
        print(app.config['nameofuser'])
        print(app.config['consultantid'])

        consultantid = app.config['consultantid']
        query1 = db.child("projects").order_by_child("Consultant ID").equal_to(consultantid).get()
        query2 = db.child("issues").order_by_child("Consultant ID").equal_to(consultantid).get()
        innerjoin = None

        query1val = None
        if query1.pyres:
                query1val = query1.val()

        query2val = None
        if query2.pyres:
                query2val = query2.val()

        if (query1val is None and query2val is None):
                innerjoin = None
        else:
                query1val.update(query2val)
                innerjoin = query1val
        print(innerjoin)
        
        return render_template('mainpage.html',
        result = allclients().val(),
        nameofuser = app.config['nameofuser'],
        joinresult = innerjoin)

@app.route('/clientpage/<clientid>', methods = ['POST', 'GET'])
def clientPage(clientid):
	clientinfo = db.child("clients").child(clientid).get()
	projectinfo = db.child("projects").order_by_child("Client ID").equal_to(clientid).get()
	interactioninfo = db.child("interactions").order_by_child("Client ID").equal_to(clientid).get()
	issueinfo = db.child("issues").order_by_child("Client ID").equal_to(clientid).get()

	clientval = None
	if clientinfo.pyres:
		clientval = clientinfo.val()
	projectval = None
	if projectinfo.pyres:
		projectval = projectinfo.val()
	interactionval = None
	if interactioninfo.pyres:
		interactionval = interactioninfo.val()
	issueval = None
	if issueinfo.pyres:
		issueval = issueinfo.val()

	return render_template('clientpage.html', id = clientid, 
	clientresult = clientval, projectresult = projectval,
	interactionresult = interactionval, issueresult = issueval)

@app.route('/projectpage/<projectid>', methods = ['POST', 'GET'])
def projectPage(projectid):
        info = db.child("projects").child(projectid).get()
        infoval = info.val()
        if 'Comments' in infoval:
                del infoval['Comments']
        commentinfo = db.child("projects").child(projectid).child("Comments").get()
        commentval = None
        if commentinfo.pyres:
                commentval = commentinfo.val()

        return render_template('projectpage.html', id = projectid, result = infoval, comments = commentval)

@app.route('/interactionpage/<interactionid>', methods = ['POST', 'GET'])
def interactionPage(interactionid):
        info = db.child("interactions").child(interactionid).get()
        infoval = info.val()
        if 'Comments' in infoval:
                del infoval['Comments']
        commentinfo = db.child("interactions").child(interactionid).child("Comments").get()
        commentval = None
        if commentinfo.pyres:
                commentval = commentinfo.val()
        return render_template('interactionpage.html', id = interactionid, result = infoval, comments = commentval)

@app.route('/issuepage/<issueid>', methods = ['POST', 'GET'])
def issuePage(issueid):
        info = db.child("issues").child(issueid).get()
        infoval = info.val()
        if 'Comments' in infoval:
                del infoval['Comments']
        commentinfo = db.child("issues").child(issueid).child("Comments").get()
        commentval = None
        if commentinfo.pyres:
                commentval = commentinfo.val()
        return render_template('issuepage.html', id = issueid, result = infoval, comments=commentval)

@app.route('/testrender')
def testRender():
    return render_template('index.html')

@app.route('/getconsultantname', methods = ['POST', 'GET'])
def get_consultant_name():
        result = request.form
        email = result['email']
        queryresult = HRdb.child("employees").order_by_child("email").equal_to("tony@starkindustries.com").limit_to_first(1).get()
        
        #queryresult = HRdb.child("employees").get()
        queryresultval = queryresult.val()
        #[('-LiuSbuP4C9lPQ019_iv', {'currently_employed': True, 'email': 'tony@starkindustries.com', 'name': 'Tony J. Stark', 'phone': '5156149354', 'role': '-LitljG0w2DQsseyJza9', 'salary': '480', 'superior': '-Ljw8tlYKzUTbsbhQ4Uw', 'terminated': False})]

        key = list(queryresultval)[0]
        name = queryresultval[key]['name']

        return render_template('loggedinname.html', result = name)

@app.route('/innerjoinprojectsandissuesonconsultant', methods = ['POST', 'GET'])
def innerjoinprojectsandissuesonconsultant():

        consultantid = app.config['consultantid']
        query1 = db.child("projects").order_by_child("Consultant ID").equal_to(consultantid).get()
        query2 = db.child("issues").order_by_child("Consultant ID").equal_to(consultantid).get()
        innerjoin = None

        query1val = None
        if query1.pyres:
                query1val = query1.val()

        query2val = None
        if query2.pyres:
                query2val = query2.val()

        if (query1val is None and query2val is None):
                print("None")
        else:
                query1val.update(query2val)

        innerjoin = query1val

        print(innerjoin)
