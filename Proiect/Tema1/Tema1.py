from openai import OpenAI

# Inițializați obiectul OpenAI cu cheia API
client = OpenAI(api_key='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')

# Definiți datele de antrenare (textul explicativ al regulilor jocului de șah)
training_data = """
Regulile jocului de șah

1. Scopul jocului:
   Scopul jocului de șah este să pună regele advers în șah și mat, adică să-l pună într-o poziție în care nu poate evita capturarea.

2. Mișcările pieselor:
   a. Pionul: Se poate deplasa înainte cu o singură casetă, dar poate captura pe diagonală. La prima mutare, are opțiunea de a avansa cu două casete.
   b. Turul: Se deplasează orizontal sau vertical oricâte căsuțe.
   c. Calul: Are o mișcare specială în formă de L. Este singura piesă care poate sări peste alte piese.
   d. Nebunul: Se deplasează pe diagonale oricâte căsuțe.
   e. Regina: Se deplasează orizontal, vertical sau pe diagonale oricâte căsuțe.
   f. Regele: Se deplasează orizontal, vertical sau pe diagonale cu o singură căsuță.

3. Șah și mat:
   a. Șahul apare atunci când regele este amenințat. Jucătorul trebuie să îl protejeze.
   b. Matul este atunci când regele nu poate fi salvat. Jocul se termină și adversarul câștigă.

4. Castling:
   Este o mișcare specială în care regele și unul dintre turnuri se deplasează simultan. Nu poate fi folosit dacă regele a fost în șah sau dacă oricare dintre piese a fost mutată anterior.

5. En passant:
   O mișcare specială a pionului în care un pion poate captura alt pion care a avansat cu două casete.

6. Promovarea pionului:
   Dacă un pion ajunge la linia de sfârșit a adversarului, este promovat la o altă piesă (de obicei, regina).

"""

# Definiți instrucțiunile pentru finetuning
instructions = """
You are a chatbot designed to explain the rules of chess. Please provide clear and concise explanations for questions related to chess rules. You can use information from the provided training data.

### Examples of questions:
1. What is castling in chess?
2. Explain en passant rule.
3. What does pawn promotion mean?

### Instructions for the model:
- Read and understand the question.
- Provide accurate and relevant information from the training data.
- Keep the response concise and easy to understand.
- If the question is not clear, ask for clarification or provide a general response.

### Important:
- Do not generate inappropriate or biased content.
- Focus on accuracy and clarity in responses.
"""

# Încărcați datele în platforma OpenAI pentru finetuning
response = client.completions.create(
    model="text-davinci-003",
    prompt=training_data,
    temperature=0.7,
    max_tokens=150,
    n=1,
    stop=None,
)

# Antrenați sistemul
finetuned_model_id = response['id']

# Demonstrarea capabilităților noului sistem
def get_chess_explanation(question):
    prompt = f"Chess rule: {question}\n{instructions}"

    response = client.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
        n=1,
        stop=None,
    )

    return response['choices'][0]['text']


# Testarea sistemului
def main():
    question = "What does pawn promotion mean?"
    answer = get_chess_explanation(question)
    print(answer)
