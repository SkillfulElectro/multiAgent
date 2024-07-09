import os
from groq import Groq
from googlesearch import search
import requests
from bs4 import BeautifulSoup

def web_search(query, num_results=3):
    def get_search_results(query, num_results):
        return search(query, stop=num_results)

    def fetch_html(url):
        response = requests.get(url)
        return response.text

    def extract_text(html):
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        return text

    search_results = get_search_results(query, num_results)
    page_texts = []

    for i, url in enumerate(search_results, start=1):
        html_text = fetch_html(url)
        page_text = extract_text(html_text)
        page_texts.append(page_text)

    return page_texts





# Create the Groq client
client = Groq(api_key= os.environ['GROQ_API_KEY'], )



system_prompt = {
    "role": "system",
    "content":
    "You are a helpful assistant. You reply with very detailed answers."
}




# Initialize the chat history
chat_history = [system_prompt]


main_history = [system_prompt]

while True:
  # Get user input from the console
  user_input = input("You: ")

  search_prompt = {
    "role": "system",
    "content":
    "provide short query to search web for " + user_input + ". no explanation and answering just short query"
  }

  temp = [search_prompt]
    
  try:
      response = client.chat.completions.create(model="llama3-8b-8192",
                                                messages=temp,
                                                max_tokens=2048,
                                                temperature=0)
    
    
      print("Searching the web for :", response.choices[0].message.content)
      search_text = response.choices[0].message.content
  except:
      search_text = user_input



    
  chat_history.append({"role": "user", "content": user_input})

  main_history.append({"role": "user", "content": user_input})

  
  

  system_prompt = {
    "role": "system",
    "content":
    "searching the web for " + user_input
  }

  chat_history.append(system_prompt)
    
  page_texts = web_search(search_text)
  for text in page_texts:
    if len(text) >= 2048:
      for i in range(0, len(text), 2048):
        chunk = text[i:i + 2048]
        chat_history.append({"role": "system", "content": chunk})
    else:
      chat_history.append({"role": "system", "content": text})


  # Append the user input to the chat history


  


  try:
    system_prompt = {
    "role": "system",
    "content":
    "based on provided search results answer very detailed to : " + user_input
  }

    chat_history.append(system_prompt)

      
    response = client.chat.completions.create(model="llama3-8b-8192",
                                                messages=chat_history,
                                                max_tokens=2048,
                                                temperature=0)
    
    
      
  except:
    print("Manager : small err")


  system_prompt = {
    "role": "system",
    "content":
    "check previous assistant prompt if it does answer needs of \"" + user_input + "\" currently give exactly same" + "answer as it , if not correct it give the complete answer . Your answer must be independent"
}

  chat_history.append(system_prompt)

  


  try:    
      response = client.chat.completions.create(model="gemma-7b-it",
                                                messages=chat_history,
                                                max_tokens=2048,
                                                temperature=0)
    
      chat_history.append({
          "role": "assistant",
          "content": response.choices[0].message.content
      })
    
      chat_history.append(system_prompt)

  except:
      print("Manager : small err")



  try:
      response = client.chat.completions.create(model="gemma2-9b-it",
                                                messages=chat_history,
                                                max_tokens=2048,
                                                temperature=0)
    
      chat_history.append({
          "role": "assistant",
          "content": response.choices[0].message.content
      })
    
      chat_history.append(system_prompt)


  except:
      print("Manager : small err")


  try:
      response = client.chat.completions.create(model="mixtral-8x7b-32768",
                                                messages=chat_history,
                                                max_tokens=2048,
                                                temperature=0)
    
      chat_history.append({
          "role": "assistant",
          "content": response.choices[0].message.content
      })
    
    
      
        
      chat_history.append(system_prompt)


  except:
      print("Manager : small err")



    
  try: 
      response = client.chat.completions.create(model="llama3-70b-8192",
                                                messages=chat_history,
                                                max_tokens=2048,
                                                temperature=0)
      # Append the response to the chat history
      main_history.append({
          "role": "assistant",
          "content": response.choices[0].message.content
      })


  except:
      print("Manager : small err")
      main_history.append({
          "role": "assistant",
          "content": response.choices[0].message.content
      })

  chat_history = main_history
    
  # Print the response
  print("Assistant:", response.choices[0].message.content)



