def test_get_workouts_empty(client):
    response = client.get("/workouts")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_workout(client):
    response = client.post(
        "/workouts",
        json={"date": "2026-07-27", "duration_minutes": 45, "notes": "Test"}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["duration_minutes"] == 45
    assert data["workout_exercises"] == []


def test_create_workout_invalid_duration(client):
    response = client.post(
        "/workouts",
        json={"date": "2026-07-27", "duration_minutes": -5}
    )
    assert response.status_code == 400


def test_get_workout_not_found(client):
    response = client.get("/workouts/999")
    assert response.status_code == 404


def test_create_exercise(client):
    response = client.post(
        "/exercises",
        json={"name": "Deadlift", "category": "strength", "equipment_needed": True}
    )
    assert response.status_code == 201
    assert response.get_json()["name"] == "Deadlift"


def test_create_exercise_invalid_category(client):
    response = client.post(
        "/exercises",
        json={"name": "Bad", "category": "not-real"}
    )
    assert response.status_code == 400


def test_create_exercise_empty_name(client):
    response = client.post(
        "/exercises",
        json={"name": "", "category": "strength"}
    )
    assert response.status_code == 400


def test_add_exercise_to_workout(client):
    workout_resp = client.post(
        "/workouts", json={"date": "2026-07-27", "duration_minutes": 30}
    )
    exercise_resp = client.post(
        "/exercises", json={"name": "Squat", "category": "strength"}
    )
    workout_id = workout_resp.get_json()["id"]
    exercise_id = exercise_resp.get_json()["id"]

    response = client.post(
        f"/workouts/{workout_id}/exercises/{exercise_id}/workout_exercises",
        json={"reps": 10, "sets": 3}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["reps"] == 10
    assert data["exercise_id"] == exercise_id

    workout_check = client.get(f"/workouts/{workout_id}")
    assert len(workout_check.get_json()["workout_exercises"]) == 1


def test_delete_workout_cascades(client):
    workout_resp = client.post(
        "/workouts", json={"date": "2026-07-27", "duration_minutes": 30}
    )
    workout_id = workout_resp.get_json()["id"]

    delete_resp = client.delete(f"/workouts/{workout_id}")
    assert delete_resp.status_code == 200

    get_resp = client.get(f"/workouts/{workout_id}")
    assert get_resp.status_code == 404
