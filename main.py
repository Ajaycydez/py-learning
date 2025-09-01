from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory "database"
students_db = []
next_id = 1  # auto-increment id


# ➡️ Create student
@app.route('/students', methods=['POST'])
def add_student():
    global next_id
    data = request.get_json()

    required_keys = {"name", "age", "grade"}
    if not required_keys.issubset(data.keys()):
        return jsonify({"error": "Invalid student data"}), 400

    student = {
        "id": next_id,
        "name": data["name"],
        "age": data["age"],
        "grade": data["grade"]
    }
    students_db.append(student)
    next_id += 1
    return jsonify({"message": "Student added successfully", "student": student}), 200


# ➡️ Read all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students_db), 200


# ➡️ Read single student
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200


# ➡️ Update student
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Update only provided fields
    for key in ["name", "age", "grade"]:
        if key in data:
            student[key] = data[key]

    return jsonify({"message": "Student updated successfully", "student": student}), 200


# ➡️ Delete student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students_db
    student = next((s for s in students_db if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    students_db = [s for s in students_db if s["id"] != student_id]
    return jsonify({"message": "Student deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
