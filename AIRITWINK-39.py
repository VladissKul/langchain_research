from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama

llm = Ollama(model="llama3.2:latest")

template = """
У тебя есть четкие черты характера. Твои черты:
1. Ты {trait_1}.
2. Ты {trait_2}.
3. Ты {trait_3}.

Твоя задача — ответить на вопросы, исходя из этих черт характера.
"""

prompt = PromptTemplate(
    input_variables=["trait_1", "trait_2", "trait_3"],
    template=template,
)

llm_chain = LLMChain(llm=llm, prompt=prompt)

response = llm_chain.run({
    "trait_1": "мужчина",
    "trait_2": "оптимистичный",
    "trait_3": "шутливый"
})

print(response)
