import ollama
#This is a sample code to test the ollama library. It sends a message to the model and prints the response.
response = ollama.chat(
    model='llama3.2:3b',
    messages=[
        {
            'role': 'user',
            'content': 'Hello'
        }
    ]
)

print(response['message']['content'])