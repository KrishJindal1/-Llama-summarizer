from core.ollama_client import chat

# Added dictionary to store the temperature and instructions for each tone option
tone_config = {
    "Professional": {
        
        "instruction": "Use polished, professional, business-oriented language."
    },
    "Formal": {
        
        "instruction": "Use formal vocabulary, complete sentences, and a serious tone."
    },
    "Casual": {
        
        "instruction": "Use conversational, friendly, and approachable language."
    },
    "Executive": {
        
        "instruction": "Focus on key insights, decisions, outcomes, and business impact."
    },
    "Technical": {
        
        "instruction": "Use precise technical terminology and maintain technical accuracy."
    },
    "Academic": {
        
        "instruction": "Use objective, analytical, and scholarly language."
    },
    "Marketing": {
       
        "instruction": "Make the content engaging, persuasive, and audience-focused."
    },
    "Simple English": {
        
        "instruction": "Use simple words, short sentences, and explain concepts clearly."
    }
}

#summary config for different lengths
summary_config = {
        "Short": "100-120 words",
        "Medium": "120-400 words",
        "Long": "400-1000 words"}


def generate_summary(document_text, target_length, selected_model):
    summary_response = chat(
                model=selected_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert document analyst."
                    },
                    {
                        "role": "user",
                        #prompt for better summarized content.
                        "content": f"""
                            Generate a summary.

                                Target Lengths:
                                    {target_length} 

                                Requirements:
                                - Capture all key points.
                                - Preserve important facts.
                                - Do not omit critical information.
                                - Use clear headings where appropriate.
                                - Do not leave the summary unfinished.
                                
                                Document:
                                {document_text}
                                """
                    }
                ],
                options={
                    "temperature": 1,
                    "num_predict": 2000 # set a high token limit to avoid the summary being cut off due to token limits.
                }
            )
    return summary_response["message"]["content"]

def rewrite_content(document_text, summary, tone, temperature, rewrite_target, selected_model):
    config = tone_config[tone]
    instruction = config["instruction"]

    rewrite_response = chat(
                model=selected_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content rewriter."
                    },
                    {
                        "role": "user",
                        "content": f"""
                            You are an expert editor.

                            Task:
                                Rewrite the content using a {tone} tone.

                            Tone Guidelines:
                                {instruction}

                                Requirements:
                                - Preserve all important information.
                                - Do not change factual content.
                                - Improve readability and organization.
                                - Keep the rewritten version approximately the same length.
                                - Use headings or bullet points when appropriate.
                                - Do not leave the rewritten version unfinished.
                                

                            Content:
                            {summary if rewrite_target == "Summary" else document_text}
                            """
                    }
                ],
                options={
                    "temperature": temperature,
                }
            )
    return rewrite_response["message"]["content"]