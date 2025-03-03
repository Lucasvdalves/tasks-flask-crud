from flask import Flask, request, jsonify
from models.task import Task

# __name__ = "__main__"
app = Flask(__name__)

tasks = []
task_id_control = 1


@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(
        id=task_id_control, title=data["title"], description=data.get("description", "")
    )
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Task created successfully"}), 201


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks_list = [task.to_dict() for task in tasks]
    output = {"tasks": tasks_list, "total_tasks": len(tasks_list)}
    return jsonify(output)


@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({"message": "Task not found"}), 404


@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = None
    
    for t in tasks:
        if t.id == id:
            task = t
            break  

    if task is None:
        return jsonify({"message": "Task not found"}), 404

    data = request.get_json()
    task.title = data["title"]
    task.description = data.get("description", "")
    task.completed = data.get("completed", False)

    return jsonify({
        "message": "Task updated successfully",
        "task": task.to_dict()  
    })

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

        if not task:
            return jsonify({"message": "Task not found"}), 404  

        tasks.remove(task)
        return jsonify({"message": "Task deleted successfully"})   


if __name__ == "__main__":
    app.run(debug=True)
