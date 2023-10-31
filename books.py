import time
import openai
import pandas as pd

def get_chatgpt_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        #model="gpt-3.5-turbo-0301", ## ateh 1 junho 2023
        messages=messages,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

# Initialize the API key
openai.api_key = "YOUR-KEY"

# read the Excel of the books
books_df = pd.DataFrame(pd.read_excel("books.xlsx"))

# Create a new 'Country' column with initial values as None
books_df['Country'] = None

print(f'We have {len(books_df)} books in the list.')
print('Conecting with ChatGPT...')

# Iterate through the DataFrame and update the 'Country' column
for index, row in books_df.iterrows():
    title = row['Title']

    print('Book: ' + title)

    message = 'What is the country where the book' + str(title) + ' was written? ' \
              ' I want a single word response, only providing the name of the country.'

    messages = []
    messages.append({"role": "user", "content": str(message)})
    answer = get_chatgpt_response(messages)[0]
    messages.append({"role": "assistant", "content": answer})

    books_df.at[index, 'Country'] = answer

    # Wait for 20 seconds before making the next request
    time.sleep(20)

print(books_df)

# Save the DataFrame back to the same Excel file
books_df.to_excel("books.xlsx", index=False)

print("Book list saved to 'books.xlsx'")
