import requests
import json # Import json for pretty printing if needed

# Define the API endpoint URL
# Note: The URL you provided "http://localhost:8000/api/questions/teachers"
# seems a bit unusual if 'teachers' is a top-level endpoint.
# It's more common to have "http://localhost:8000/api/teachers/".
# I will use the one you provided, but keep this in mind if it doesn't work.
API_URL = "http://localhost:8000/api/teachers/"

# Teacher data to be sent
teacher_data = {
    "email": "abc@xyz.com",
    "teacher_id": "abc2",
    "name": "teacher_2",
    "password": "qwerty@123456" # The Django model's save method will hash this
}

print(f"Attempting to add teacher: {teacher_data['name']} (ID: {teacher_data['teacher_id']})...")
print(f"Sending POST request to: {API_URL}")

try:
    # Make the POST request
    response = requests.post(API_URL, json=teacher_data)

    # Raise an HTTPError for bad responses (4xx or 5xx)
    response.raise_for_status()

    # If the request was successful (200 or 201 status code)
    if response.status_code in [200, 201]:
        print("\n✅ Teacher added successfully!")
        print("Response:")
        # Use json.dumps for pretty printing the JSON response
        print(json.dumps(response.json(), indent=4))
    else:
        # This block might not be reached if raise_for_status() is used,
        # but it's good for explicit handling of non-error success codes if any.
        print(f"\n⚠️ Unexpected success status code: {response.status_code}")
        print("Response:")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("\n❌ Connection error: Could not connect to the Django server.")
    print("Please ensure your Django development server is running at http://localhost:8000.")
except requests.exceptions.HTTPError as e:
    print(f"\n❌ HTTP Error occurred: {e}")
    print(f"Status Code: {response.status_code}")
    print("Response Content:")
    print(response.text)
except requests.exceptions.RequestException as e:
    print(f"\n❌ An error occurred during the request: {e}")
except Exception as e:
    print(f"\n❌ An unexpected error occurred: {e}")

print("\nScript finished.")