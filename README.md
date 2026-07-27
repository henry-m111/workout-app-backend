# Workout Application Backend

## Project Description

A Flask + SQLAlchemy + Marshmallow REST API for a workout tracking application used by personal trainers. The API tracks **Workouts** and **Exercises**, connected through a **WorkoutExercise** join model that records reps, sets, and/or duration for each exercise performed in a given workout. Exercises are reusable across multiple workouts.

The backend enforces data integrity at three layers:
- **Table constraints** (database-level `CHECK` constraints)
- **Model validations** (`@validates` decorators in SQLAlchemy)
- **Schema validations** (Marshmallow field validators on incoming request data)

## Entity Relationships

- A `Workout` has many `WorkoutExercises`
- An `Exercise` has many `WorkoutExercises`
- A `Workout` has many `Exercises` through `WorkoutExercises`
- An `Exercise` has many `Workouts` through `WorkoutExercises`
- Deleting a `Workout` or `Exercise` cascades to delete its associated `WorkoutExercise` rows

## Installation

**Requirements:** Python 3.8+ (tested on 3.12), Pipenv

```bash
git clone https://github.com/henry-m111/workout-app-backend.git
cd workout-app-backend
pipenv install --dev
pipenv shell
```

If `pipenv` can't find a Python version automatically:

```bash
pipenv --python $(which python3)
pipenv install --dev
```

## Database Setup

All commands below are run from inside the `server/` directory, with `FLASK_APP` set:

```bash
cd server
export FLASK_APP=app.py
flask db upgrade head
python3 seed.py
```

This creates `server/instance/app.db` and seeds it with example exercises, workouts, and workout-exercise records.

## Running the App

```bash
cd server
python3 app.py
```

The API runs at `http://127.0.0.1:5555`.

## Running Tests

```bash
cd server
python3 -m pytest -v
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get a single workout, including its exercises with reps/sets/duration |
| POST | `/workouts` | Create a workout (`date`, `duration_minutes`, `notes`) |
| DELETE | `/workouts/<id>` | Delete a workout (cascades to its WorkoutExercises) |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get a single exercise, including its associated workouts |
| POST | `/exercises` | Create an exercise (`name`, `category`, `equipment_needed`) |
| DELETE | `/exercises/<id>` | Delete an exercise (cascades to its WorkoutExercises) |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with `reps`, `sets`, and/or `duration_seconds` |

### Example Requests

**Create an exercise:**
```bash
curl -X POST http://127.0.0.1:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Deadlift", "category": "strength", "equipment_needed": true}'
```

**Create a workout:**
```bash
curl -X POST http://127.0.0.1:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-07-27", "duration_minutes": 40, "notes": "Leg day"}'
```

**Add an exercise to a workout:**
```bash
curl -X POST http://127.0.0.1:5555/workouts/1/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"reps": 10, "sets": 3}'
```

## Validations

**Table Constraints:**
- `Workout.duration_minutes` must be greater than 0
- `WorkoutExercise` must have at least one of `reps`, `sets`, or `duration_seconds` set
- `WorkoutExercise.reps`, `sets`, and `duration_seconds` must each be positive if set

**Model Validations:**
- `Exercise.name` cannot be empty
- `Exercise.category` must be one of: `strength`, `cardio`, `flexibility`, `balance`
- `Workout.duration_minutes` must be a positive number of minutes

**Schema Validations:**
- `ExerciseSchema.category` must be one of the allowed categories
- `WorkoutExerciseSchema.reps` / `sets` / `duration_seconds` must be at least 1 if provided

## Project Structure

```
workout-app-backend/
├── Pipfile / Pipfile.lock
├── .gitignore
└── server/
    ├── app.py          # Flask app and routes
    ├── models.py       # SQLAlchemy models, relationships, validations
    ├── schemas.py       # Marshmallow schemas and validations
    ├── seed.py         # Database seed script
    ├── migrations/     # Flask-Migrate/Alembic migrations
    └── tests/
        ├── conftest.py
        ├── test_models.py
        └── test_app.py
```
