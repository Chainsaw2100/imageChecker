import datetime
from flask import render_template, flash, redirect, url_for, request,Response
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User,FileContents
from io import BytesIO
from PIL import Image
import random





@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')



@app.route('/api/upload', methods = ['POST'])
@login_required
def upload():
    file = request.files['file_photo']
    data_red = file.read()
    image_bytes = BytesIO(data_red)
    file.save(image_bytes)
    image_file_size = int(file.tell())//1000
    img = Image.open(image_bytes)
    size = img.size
    date_upl=str(datetime.datetime.now())
    user_upl = current_user.username
    newFile = FileContents(name=file.filename,data=data_red,size = image_file_size,res_h=size[1],res_w=size[0],form=file.filename.split(".")[-1],date_orig=date_upl,user_orig=user_upl,date_dupl="null",user_dupl="null")
    checkDouble = FileContents.query.filter_by(data=data_red).first()
    if checkDouble == None:
        # print('Hello')
        # do_async_upload.apply_async(args=[checkDouble], countdown=15)
        db.session.add(newFile)
        db.session.commit()

        return 'Saved, id: ' + str(newFile.id)
    else:
        if checkDouble.date_dupl == "null":
            checkDouble.date_dupl=date_upl
        else:
            checkDouble.date_dupl+=" " + date_upl

        if checkDouble.user_dupl == "null":
            checkDouble.user_dupl=user_upl
        else:
            checkDouble.user_dupl+=" " + user_upl
            
        db.session.add(checkDouble)   
        db.session.commit()

        return "File exists, date and user fields updated"    


@app.route(r'/api/show/<int:image_id>', methods = ['GET'])
def show(image_id):
    pic = FileContents.query.filter_by(id=image_id).first()
    if pic:
        
        # return send_file(io.BytesIO(pic.data),mimetype=pic.form,as_attachment=True,attachment_filename='%s.jpg' % pic.name)
        return Response(pic.data, mimetype='image/jpeg')
        # do_async_show.apply_async(args=[pic], countdown=random.randint(1,21))
    else:
        return "No picture found"






@app.route(r'/api/info/<int:image_id>', methods = ['GET'])
@login_required
def info(image_id): 
    pic = FileContents.query.filter_by(id=image_id).first()
    if pic != None:
        # do_async_info.apply_async(args=[pic], countdown=random.randint(1,21))
        pic = pic.__repr__()
        return {'pic': pic}
    else:
        return "No picture found"   






@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)





@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))






@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)









@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
