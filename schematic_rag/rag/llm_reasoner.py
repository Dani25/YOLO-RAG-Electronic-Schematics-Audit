def build_prompt(components, connections, retrieved_context):
    return f"""
You are an expert electrical engineer.

Components:
{components}

Connections:
{connections}

Knowledge:
{retrieved_context}

Tasks:
1. Infer missing connections
2. Correct errors
3. Generate netlist
4. Generate BOM

Return structured output.
"""


def generate_reasoning(client, components, connections, retrieved_context):
    prompt = build_prompt(components, connections, retrieved_context)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
