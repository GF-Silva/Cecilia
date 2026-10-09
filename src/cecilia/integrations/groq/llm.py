from groq import AsyncGroq
from dotenv import load_dotenv
import os
import asyncio

class LLM:
    def __init__(self, system_prompt: str):
        print("Init groq llm class")

        load_dotenv()

        self.context: list = [{
            "role": "system",
            "content": system_promt
        }]

        self.model = "openai/gpt-oss-120b"

        self.client = AsyncGroq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    # Ideia: Criar ranges de prompt, tipo low memory, medium and high, 
    # cada uma mudando quanto do contexto a llm pega
    # Criar um contexto perssistente no disco?
    async def send_prompt(self, prompt: str):
        self.context.append({
            "role": "user",
            "content": prompt
        })

        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=self.context
        )

        self.context.append({
            "role": "assistant",
            "content": completion.choices[0].message.content
        })

        return completion.choices[0].message.content


if __name__ == '__main__':
    system_promt = 'Você é um assistente util'
    llm = LLM(system_prompt=system_promt)

    while True:
        choice = int(input("Opc: "))

        match choice:
            case 1:
                prompt = input("Mensagem: ")
                response = asyncio.run(llm.send_prompt(prompt))
                print(response)

            case 2:
                print(llm.context)

            case default:
                break