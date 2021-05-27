from flask import Flask, render_template, request, redirect, abort
from models import db, MemberModel
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html',title='home')

@app.route('/data/create', methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html',title='create')
    if request.method == 'POST':
        name = request.form['name']
        relation = request.form['relation']
        image = request.form['image']
        member = MemberModel(name=name, relation=relation, image=image)
        db.session.add(member)
        db.session.commit()
        return redirect('/')

@app.route('/data/<int:id>')
def RetrieveMember(id):
    members = MemberModel.query.all()
    return render_template('datalist.html', members=members)

@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    member = MemberModel.query.filter_by(member_id=id).first()
    if request.method == 'POST':
        if member:
            db.session.delete(member)
            db.session.commit()
            name = request.form['name']
            relation = request.form['relation']
            image = request.form['image']
            member = MemberModel(id=id, name=name,relation=relation,image=image)
            db.session.add(member)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Member with id = {id} Does nit exist"

    return render_template('update.html', member=member)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    member = MemberModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if member:
            db.session.delete(member)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html', title='delete')


if __name__ == '__main__':
    app.run(host='localhost', port=2000, debug=True)
