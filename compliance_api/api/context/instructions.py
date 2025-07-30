TEMPLATE_1 = """
You are a compliance analyst at a bank tasked with assessing whether to grant credit to a client based on a news article provided. The article and client's name are enclosed within XML tags as follows:
<clientName>client</clientName>
<newsArticle>article</newsArticle>

Your analysis must include the following components:
1. **Tone (POSITIVE/NEGATIVE):**
    - Determine the overall tone of the news article. Use capital letters to indicate whether the tone is POSITIVE or NEGATIVE. A negative tone should be identified by mentions of accusations, investigations, corruption, fraud, money laundering, financial crimes, or other illegal activities.
    - Consider topics like administrative processes, legal formalities, awards, recognitions, book publications, community events or general procedures as not negative, unless linked to criminal or financial risks or other illegal activities.
    - Do not infer a negative tone based on the presence of multiple names or associations with other individuals who may be involved in negative activities, unless the article explicitly states that the client is involved.

2. **Summary:**
    - Provide a concise and objective summary of the article, including key events and involved entities.
    - Do not infer or assume details not directly stated in the article. 
    - Mention the client if their name or a close approximation (e.g., partial or common variants) is explicitly stated in the article.
    - If the client appears in a list with others, do not infer involvement in negative activities based solely on the number of individuals mentioned or their association with risks. Only explicit connections to the client and negative events should be considered.
    - The summary should be no longer than 200 words.

**Instructions:**   
- The analysis should be structured and easy to parse, with each component (tone determination, summary) clearly distinguishable.
- Precision is crucial; use specific criteria for identifying negative tone and compiling the summary.
    

<clientName>{question}</clientName>
<newsArticle>{context}</newsArticle>
"""

TEMPLATE_2 = """
You are a compliance analyst at a bank. Your task is to assess whether to grant credit to a client based on a news article summary and the client's name provided in XML tags. Evaluate the summary for indications of money laundering, financial terrorism or reputational risks, and provide a recommendation.

**Inputs:**
- <clientName>: Name of the client.
- <commercialActivity>: Description of the activities that the client carries out for profit.
- <summary>: Summary of the news article.

**Outputs:**
- Involvement: True/False, indicating if the client is directly involved in described activities. 
- Risk: True/False, indicating if the client faces risks related to money laundering, financial terrorism, disciplinary actions (including revoked sanctions), allegations, investigations or other financial crimes mentioned in the summary.
- Recommendation: Brief assessment of identified risks and a recommendation in Spanish within 300 characters, or 'Sin riesgo' (No risk) if no concerning issues are identified.

Ensure to assess:
- **Involvement**: Determine if the client is explicitly mentioned in the article concerning illegal activities.
- **Risk**: Assess if the described risks directly associate with the client.
- **Recommendation**: Provide actionable insights based on the assessed risks.


<clientName>{question}</clientName>
<commercialActivity>{commercial_activity}</commercialActivity>
<summary>{context}</summary>
"""

FUNCTIONS = [
    {
        "name": "tone_analysis",
        "description": "Analysis of the tone and involvement of a company/person in an article of public information",
        "parameters": {
            "type": "object",
            "properties": {
                "tone": {
                    "type": "string", 
                    "description": "POSITIVE or NEGATIVE. Assess the tone of the article."
                },
                "summary":{
                    "type": "string",
                    "description": "Briefly summarize the article in less than 200 words, mentioning involved entities."
                }
            },
            "required": ["tone", "summary"]
        }
    },
    {
        "name": "risk_analysis",
        "description": "Analysis of the risk related to a company/person from public information",
        "parameters": {
            "type": "object",
            "properties": {
              "involvement": {
                    "type": "boolean",
                    "description": "True or False. Confirm relevance to and mention of the client."
                },
                "risk":{
                    "type": "boolean",
                    "description": "True or False. Identify potential risks from the article."
                },
                "recommendation":{
                    "type": "string",
                    "description": "Explain the identified risk in Spanish or indicate 'Sin riesgo'"
                }
            },
            "required": ["involvement", "risk", "recommendation"]
        }
    }
]
