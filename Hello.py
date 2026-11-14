
import ollama

messages = []

print("AI Chatbot with Memory")
print("Type 'exit' to stop")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("Chat ended!")
        break

    messages.append({
        "role": "user",
        "content": question
    })

    response = ollama.chat(
        model="llama3.2:1b",
        messages=messages
    )

    answer = response.message.content

    messages.append({
        "role": "assistant",
        "content": answer
    })

    print("AI:", answer)
messages.append({
    "role": "system",
    "content": "Remember the user's name and previous conversation. Answer questions using the conversation history."
})