import requests

question_paper = "430-1-1MATHEMATICS (BASIC)"

res = requests.get("http://localhost:8000/api/papers/?name={question_paper}}")

paper_id = res.json()[0]['id']

# Define the answers for each question
# This dictionary maps question number (int) to its answer (str)
questiona_all = {
    2: "4",
    3: "4",
    4: "2",
    5: "1",
    6: "2",
    7: "4",
    8: "1",
    9: "3",
    10: "4",
    11: "2",
    12: "3",
    13: "1",
    14: "4",
    15: "3",
    16: "3",
    17: "2",
    18: "3",
    19: "3",
    20: "1"
}

url = "http://localhost:8000/api/questions/"

# Common data for questions (marks)
common_question_data = {
    "paper": paper_id,
    "marks": 1
}

print("\n--- Inserting Questions (2 to 20) with Specific Answers ---")

# Loop for question numbers 2 to 20
for q_num in range(2, 21): # range(start, stop) - stop is exclusive
    # Get the specific answer for the current question number
    current_answer = questiona_all.get(q_num)

    if current_answer is None:
        print(f"⚠️ Warning: No answer found for Q{q_num}. Skipping or providing default 'Unknown'.")
        current_answer = "Unknown" # Or you could skip this question, depending on your requirement

    # Format the question number for the image path (e.g., Q02, Q10)
    q_num_str = f"Q{q_num:02d}" # :02d ensures two digits, e.g., 02, 03, ... 19, 20

    data = {
        "question_number": q_num,
        "image_path": f"/media/math_2024_430_1_1_BASIC/{q_num_str}.png",
        "answer": current_answer, # Now using the specific answer
        **common_question_data # Unpack common data (paper_id, marks)
    }

    print(f"Attempting to add question {q_num} (Answer: {current_answer})...")
    try:
        response = requests.post(url, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        if response.status_code in [200, 201]:
            print(f"✅ Question {q_num} Added Successfully: {response.json()}")

    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error for Question {q_num}: Ensure your Django server is running.")
        break # Break the loop if connection is lost
    except requests.exceptions.RequestException as e:
        print(f"❌ Error adding Question {q_num}: {e}")
        print(f"   Response content: {response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred for Question {q_num}: {e}")

print("\n--- Finished processing questions ---")