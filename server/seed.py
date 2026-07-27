#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Clearing database...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    squat = Exercise(name="Squat", category="strength", equipment_needed=True)
    pushup = Exercise(name="Push-up", category="strength", equipment_needed=False)
    plank = Exercise(name="Plank", category="strength", equipment_needed=False)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    stretch = Exercise(name="Hamstring Stretch", category="flexibility", equipment_needed=False)

    db.session.add_all([squat, pushup, plank, running, stretch])
    db.session.commit()

    print("Seeding workouts...")
    leg_day = Workout(date=date(2026, 7, 20), duration_minutes=45, notes="Focused on lower body strength.")
    cardio_day = Workout(date=date(2026, 7, 22), duration_minutes=30, notes="Steady-state cardio.")
    full_body = Workout(date=date(2026, 7, 24), duration_minutes=60, notes="Full body with core work.")

    db.session.add_all([leg_day, cardio_day, full_body])
    db.session.commit()

    print("Seeding workout_exercises...")
    workout_exercises = [
        WorkoutExercise(workout=leg_day, exercise=squat, reps=10, sets=4),
        WorkoutExercise(workout=leg_day, exercise=stretch, duration_seconds=60),
        WorkoutExercise(workout=cardio_day, exercise=running, duration_seconds=1800),
        WorkoutExercise(workout=full_body, exercise=squat, reps=8, sets=3),
        WorkoutExercise(workout=full_body, exercise=pushup, reps=15, sets=3),
        WorkoutExercise(workout=full_body, exercise=plank, duration_seconds=45),
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print(f"Seeded {Exercise.query.count()} exercises, "
          f"{Workout.query.count()} workouts, "
          f"{WorkoutExercise.query.count()} workout_exercises.")
