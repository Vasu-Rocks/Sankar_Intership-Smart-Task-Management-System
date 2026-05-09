import requests

BASE_URL = 'http://127.0.0.1:5000'

def run_tests():
    # We use a session object to persist cookies (for login)
    session = requests.Session()

    print("--- 1. Testing Security: 401 Unauthorized ---")
    response = session.get(f"{BASE_URL}/api/tasks/")
    print(f"GET /api/tasks/ (No Login) -> Status: {response.status_code}")
    print(response.json())
    print()

    print("--- 1.5. Registering Test User ---")
    register_data = {'username': 'testuser', 'password': 'testpassword'}
    # We ignore the response here because it might already be registered, which is fine!
    session.post(f"{BASE_URL}/register", data=register_data)

    print("--- 2. Logging In ---")
    login_data = {'username': 'testuser', 'password': 'testpassword'}
    response = session.post(f"{BASE_URL}/login", data=login_data)
    
    if "Login successful" in response.text:
        print("Login successful! Session cookie obtained.")
    else:
        print("Login failed! Did you register the 'testuser' account?")
        return
    print()

    print("--- 3. Create a Task (POST) ---")
    new_task = {
        'title': 'Learn REST APIs',
        'description': 'Building Phase 3 of the task manager.'
    }
    response = session.post(f"{BASE_URL}/api/tasks/", json=new_task)
    print(f"POST /api/tasks/ -> Status: {response.status_code}")
    print(response.json())
    task_id = response.json().get('id')
    print()

    if not task_id:
        return

    print("--- 4. Get All Tasks (GET) ---")
    response = session.get(f"{BASE_URL}/api/tasks/")
    print(f"GET /api/tasks/ -> Status: {response.status_code}")
    print(response.json())
    print()

    print("--- 5. Update a Task (PUT) ---")
    update_data = {
        'status': 'Completed',
        'priority': 'High'
    }
    response = session.put(f"{BASE_URL}/api/tasks/{task_id}", json=update_data)
    print(f"PUT /api/tasks/{task_id} -> Status: {response.status_code}")
    print(response.json())
    print()

    print("--- 5.5. Get Analytics (GET) ---")
    response = session.get(f"{BASE_URL}/api/analytics/")
    print(f"GET /api/analytics/ -> Status: {response.status_code}")
    print(response.json())
    print()

    print("--- 6. Delete a Task (DELETE) ---")
    response = session.delete(f"{BASE_URL}/api/tasks/{task_id}")
    print(f"DELETE /api/tasks/{task_id} -> Status: {response.status_code}")
    print(response.json())
    print()

if __name__ == '__main__':
    run_tests()
