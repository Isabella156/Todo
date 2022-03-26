from datetime import datetime
from flask import render_template, redirect, url_for, request
from app import app, db
from .models import Todo, Code, Title
from .forms import TodoForm


# home page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


# list page
@app.route('/list', methods=['GET', 'POST'])
def list():
    form = TodoForm()
    todo_list = Todo.query.all()
    code_list = Code.query.with_entities(Code.code).distinct().all()
    return render_template("list.html", todo_list=todo_list, code_list=code_list, form=form)


# search assessments
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = TodoForm()
    # check the conditions
    searchCode = request.form.get("searchCode")
    if searchCode == "No requirements":
        searchCode = None

    searchTitle = request.form.get("searchTitle")
    if searchTitle == "":
        searchTitle = None

    searchState = request.form.get("searchState")
    if searchState == "Uncompleted":
        searchState = False
    elif searchState == "Completed":
        searchState = True
    else:
        searchState = None

    filterList = []
    if searchCode is not None:
        filterList.append(Todo.code == searchCode)
    if searchTitle is not None:
        filterList.append(Todo.title.like('%' + searchTitle + '%'))
    if searchState is not None:
        filterList.append(Todo.complete == searchState)

    todo_list = Todo.query.filter(*filterList).all()
    code_list = Code.query.with_entities(Code.code).distinct().all()

    return render_template("list.html", todo_list=todo_list, code_list=code_list, form=form)


# add new assessment
@app.route("/add", methods=["POST"])
def add():
    form = TodoForm()
    if form.validate_on_submit():
        # add new assessment
        new_todo = Todo(code=form.code.data, deadline=form.deadline.data, title=form.title.data,
                        description=form.description.data, complete=False)
        # test roll back
        # new_todo = Todo(id=1, code=form.code.data, deadline=form.deadline.data, title=form.title.data,
        #                 description=form.description.data, complete=False)
        db.session.add(new_todo)
        # add new code
        new_code = Code(code=form.code.data)
        db.session.add(new_code)
        # add new title
        new_title = Title(title=form.title.data)
        db.session.add(new_title)
        try:
            db.session.commit()
        except Exception as e:
            # test roll back
            # print("before roll back")
            db.session.rollback()
            # print("after roll back")
        return redirect(url_for("list"))
    return redirect(url_for("list"))


# update the status of the assessment
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for("list"))


# delete the assessment
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    code = Code.query.filter_by(code=todo.code).first()
    title = Title.query.filter_by(title=todo.title).first()
    db.session.delete(title)
    db.session.delete(code)
    db.session.delete(todo)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for("list"))


# edit the assessment
@app.route("/edit/<int:todo_id>", methods=["POST"])
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    # check the content of the form
    code = request.form.get("editCode")
    if code != "":
        editCode = Code.query.filter_by(code=todo.code).first()
        todo.code = code
        editCode.code = code

    title = request.form.get("editTitle")
    if title != "":
        editTitle = Title.query.filter_by(title=todo.title).first()
        todo.title = title
        editTitle.title = title

    deadline = request.form.get("editDate")
    if deadline != "":
        deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
        todo.deadline = deadline

    description = request.form.get("editDescription")
    if description != "":
        todo.description = description

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for("list"))
