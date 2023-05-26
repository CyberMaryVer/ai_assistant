prompt_template_question = """
You have a great expertise in SEC regulations. Please provide a concise answer to the question below.

Example format: 
ANSWER:
  [regulations that apply to the case, recommendations, etc.]
ANSWER_IN_RUSSIAN:
  [translation of the answer in Russian]

Question: {text}

Result:
ANSWER:"""

prompt_template_summary = """
Please provide a concise summary of the following text and translate it into Russian.

Example format: 
CONCISE SUMMARY:
  [summary in Russian]
MAIN IDEA FOR EACH PARAGRAPH:
  - [main idea for paragraph '...' in Russian]
  - [main idea for paragraph '...' in Russian]

Text: {text}

Result:
CONCISE SUMMARY:"""

PROMPT_REGULAR = """
system: You are a Russian business expert. Please provide a concise answer to the question below.
"""