import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def teach_skill(skill, job_title):
    prompt = f"""
You are an AI tutor.

Teach the skill "{skill}" specifically for this job:
"{job_title}"

Explain:
1. What the skill is
2. Why this job requires it
3. Core concepts
4. Simple example
5. 30-day learning roadmap
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content
