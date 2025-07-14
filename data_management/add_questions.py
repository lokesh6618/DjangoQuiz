import requests

# URL to your local API endpoint (adjust if deployed or port differs)
BASE_URL = "http://localhost:8000/api/papers/"

# List of question paper names (extracted from your provided file names)
question_paper_names = [
    "430-3-1MATHEMATICS (BASIC)",
    "430-5-1MATHEMATICS (BASIC)",
    "430-1-2MATHEMATICS (BASIC)",
    "430-3-2MATHEMATICS (BASIC)",
    "430-5-2MATHEMATICS (BASIC)",
    "430-1-3MATHEMATICS (BASIC)",
    "430-3-3MATHEMATICS (BASIC)",
    "430-5-3MATHEMATICS (BASIC)",
    "430-2-1MATHEMATICS (BASIC)",
    "430-4-1MATHEMATICS (BASIC)",
    "430(B) Maths Basic for VI",
    "430-2-2MATHEMATICS (BASIC)",
    "430-4-2MATHEMATICS (BASIC)",
    "430-2-3MATHEMATICS (BASIC)",
    "430-4-3MATHEMATICS (BASIC)",
]

# Common payload data for all question papers
common_payload_data = {
    "subject": "Maths",
    "time_minutes": 30,
    "total_marks": 20
}

print("Attempting to insert multiple question papers...")
print("-" * 40)

# Iterate through each name and send a POST request
for name in question_paper_names:
    # Create a new payload for the current paper
    payload = {
        "name": name,
        **common_payload_data  # Unpack common data into the payload
    }

    print(f"Sending request for: {name}...")
    try:
        response = requests.post(BASE_URL, json=payload)

        # Print results
        if response.status_code == 201:
            print(f"✅ Successfully created: {name}")
            # print(response.json()) # Uncomment to see full response for each
        else:
            print(f"❌ Failed to create: {name}")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error for {name}: {e}")
        print("   Please ensure your Django server is running at http://localhost:8000.")
    except Exception as e:
        print(f"❌ An unexpected error occurred for {name}: {e}")
    print("-" * 40)

print("Finished processing all question papers.")