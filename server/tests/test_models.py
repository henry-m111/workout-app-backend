import pytest
from datetime import date

from models import db, Exercise, Workout, WorkoutExercise


def test_exercise_requires_nonempty_name(app):
    with pytest.raises(ValueError):
        Exercise(name="", category="strength")


def test_exercise_requires_valid_category(app):
    with pytest.raises(ValueError):
        Exercise(name="Squat", category="not-a-category")


def test_valid_exercise_can_be_created(app):
    e = Exercise(name="Squat", category="strength", equipment_needed=True)
    db.session.add(e)
    db.session.commit()
    assert e.id is not None


def test_workout_requires_positive_duration(app):
    with pytest.raises(ValueError):
        Workout(date=date(2026, 7, 27), duration_minutes=-10)


def test_workout_exercise_requires_reps_sets_or_duration(app):
    workout = Workout(date=date(2026, 7, 27), duration_minutes=30)
    exercise = Exercise(name="Plank", category="strength")
    db.session.add_all([workout, exercise])
    db.session.commit()

    we = WorkoutExercise(workout_id=workout.id, exercise_id=exercise.id)
    db.session.add(we)
    with pytest.raises(Exception):
        db.session.commit()
    db.session.rollback()


def test_workout_has_many_exercises_through_workout_exercise(app):
    workout = Workout(date=date(2026, 7, 27), duration_minutes=30)
    exercise = Exercise(name="Squat", category="strength")
    db.session.add_all([workout, exercise])
    db.session.commit()

    we = WorkoutExercise(workout_id=workout.id, exercise_id=exercise.id, reps=10, sets=3)
    db.session.add(we)
    db.session.commit()

    assert exercise in workout.exercises
    assert workout in exercise.workouts
