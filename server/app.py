from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import *
from schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


# ---------- Workouts ----------

@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'GET':
        all_workouts = Workout.query.all()
        return jsonify(workouts_schema.dump(all_workouts)), 200

    if request.method == 'POST':
        data = request.get_json()
        try:
            validated = workout_schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        try:
            new_workout = Workout(
                date=validated['date'],
                duration_minutes=validated['duration_minutes'],
                notes=validated.get('notes')
            )
            db.session.add(new_workout)
            db.session.commit()
        except ValueError as err:
            db.session.rollback()
            return jsonify({'error': str(err)}), 400

        return jsonify(workout_schema.dump(new_workout)), 201


@app.route('/workouts/<int:id>', methods=['GET', 'DELETE'])
def workout_by_id(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404

    if request.method == 'GET':
        return jsonify(workout_schema.dump(workout)), 200

    if request.method == 'DELETE':
        db.session.delete(workout)  # cascade removes associated WorkoutExercises
        db.session.commit()
        return jsonify({'message': f'Workout {id} deleted'}), 200


# ---------- Exercises ----------

@app.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'GET':
        all_exercises = Exercise.query.all()
        return jsonify(exercises_schema.dump(all_exercises)), 200

    if request.method == 'POST':
        data = request.get_json()
        try:
            validated = exercise_schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        try:
            new_exercise = Exercise(
                name=validated['name'],
                category=validated['category'],
                equipment_needed=validated.get('equipment_needed', False)
            )
            db.session.add(new_exercise)
            db.session.commit()
        except ValueError as err:
            db.session.rollback()
            return jsonify({'error': str(err)}), 400

        return jsonify(exercise_schema.dump(new_exercise)), 201


@app.route('/exercises/<int:id>', methods=['GET', 'DELETE'])
def exercise_by_id(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    if request.method == 'GET':
        result = exercise_schema.dump(exercise)
        result['workouts'] = workouts_schema.dump(exercise.workouts)
        return jsonify(result), 200

    if request.method == 'DELETE':
        db.session.delete(exercise)  # cascade removes associated WorkoutExercises
        db.session.commit()
        return jsonify({'message': f'Exercise {id} deleted'}), 200


# ---------- WorkoutExercises (join) ----------

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if not workout or not exercise:
        return jsonify({'error': 'Workout or Exercise not found'}), 404

    data = request.get_json() or {}
    try:
        validated = workout_exercise_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_we = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=validated.get('reps'),
        sets=validated.get('sets'),
        duration_seconds=validated.get('duration_seconds')
    )
    db.session.add(new_we)
    db.session.commit()

    return jsonify(workout_exercise_schema.dump(new_we)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
