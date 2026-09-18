import os
from openai import OpenAI


def build_prompt(query, evidence):
    evidence_text = "\n\n".join(
        f"Source: {item['document_id']} | "
        f"Title: {item['title']} | "
        f"Version: {item['version']}\n"
        f"Content: {item['content']}"
        for item in evidence
    )

    return f"""
You are a secure enterprise research assistant.

Answer the user's question using ONLY the authorized evidence below.

User question:
{query}

Authorized evidence:
{evidence_text}

Rules:
1. Never invent information.
2. Never use information outside the authorized evidence.
3. If the evidence is insufficient, say so.
4. Cite the source document in your answer.
"""


def prepare_llm_request(query, evidence):
    if not evidence:
        return None

    return {
        "prompt": build_prompt(query, evidence),
        "evidence": evidence
    }


def generate_answer(query, evidence):
    if not evidence:
        return "No accessible information was found for this question."

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return evidence[0]["content"]

    client = OpenAI(api_key=api_key)

    request = prepare_llm_request(query, evidence)

    response = client.responses.create(
        model="gpt-5-mini",
        input=request["prompt"]
    )

    return response.output_text