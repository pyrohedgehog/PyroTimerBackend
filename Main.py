from Database import *
import Database


@app.route("/", methods=["GET"])
def blankPage():
    return "The app is running, all clear here!"


@app.route('/user', methods=['POST'])
def createUser():
    if not request.json:
        return "Error, no user information given"
    else:
        re = request.json
        user = User.genNewUserFromDict(re)
        User.session.add(user)
        return user.to_dict()


@app.route("/user/<name>")
def getUser(name):
    foo = User.query.filter_by(username=str(name)).first()
    if (foo != None):
        print("{} has just loggedIn".format(foo))
        return foo.to_dict()
    return "500"


@app.route('/getAllTasks/<id>', methods=['GET'])
def getAllTasks(id):
    if not request.json:
        return "Error, no user given"
    try:
        re = request.json
        firstTask = int(id)
        task = getTaskById(firstTask)
        tasks = []
        task.getAllLinkedTasks(tasks)
        return json.dumps(tasks)
    except Exception as e:
        return str(e)


@app.route('/getTask/<id>', methods=["GET"])
def getTask(id):
    try:
        re = request.json
        return json.dumps(getTaskById(id))
    except Exception as e:
        return str(e)


@app.route("/tasks", methods=['GET', 'PUT'])
def tasksActions():
    if request.method == "GET":
        id = request.json['ID']
        return getTaskById(id)
    elif request.method == "PUT":
        print("creating new tasks with args {}".format(request.args))
        try:
            # page = request.args.get("page", 0, type=int)
            # pageSize = request.args.get("pageSize", 100, type=int)
            # apartment = request.args.get("apartment", -1, type=int)
            # active = request.args.get("active", False, type=bool)
            # task = request.args.get("task", -1, type=int)
            # employee = request.args.get("employee", -1, type=int)
            d = request.args.to_dict()
            print(d)
            task = Database.Task([d["ID"], d['ID']], d["ID"], d["title"], d["info"])
            print(task)
            db.session.add(task)
            db.session.commit()
            print("IT WORKS")
            print(task)

            return task.to_dict()
        except Exception as e:
            print(str(e))
            return "NOT a fully formed task!"


def getTaskById(id):
    return Task.query.filter_by(id=int(id)).first()


if __name__ == "__main__":
    #    db.create_all()
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
else:
    app.jinja_env.auto_reload = True
    app.run(host="0.0.0.0", port=8080, debug=False)
