import streamlit as st
import ollama


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
   

# side bar 
with st.sidebar:
    st.title('🦙💬 Llama summarizer')
    
    models = ollama.list()
# To choose all the models present in the ollama list and show them in the dropdown menu
    model_names = [
        model.model
        for model in models.models
]
    selected_model = st.selectbox("Choose Model",model_names)


    # To choose the temperature and show it in the slider
    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.7
    )


    # To choose the summary length and show it in the dropdown menu
    st.subheader("Summary Settings")

    summary_size = st.selectbox(
        "Summary Length",
        ["Short", "Medium", "Long"]
    )
    summary_config = {
    "Short": "100-200 words",
    "Medium": "300-500 words",
    "Long": "700-1000 words"
}
    target_length = summary_config[summary_size] # select max lenght based on words count  to avoid the summary being cut off due to token limits.



    # To choose the rewrite tone and show it in the dropdown menu
    tone = st.selectbox(
        "Rewrite Tone",
        [
            "Professional",
            "Formal",
            "Casual",
            "Executive",
            "Technical",
            "Academic",
            "Marketing",
            "Simple English"
        ]
    )


    
    rewrite_target = st.selectbox(
    "Rewrite",
    [
        "Summary",
        "Full Document"
    ]
)
    


# Main app
st.title("📄 AI Document Analyzer")
#Text Box to paste the document to be analyzed
document_text = st.text_area(
    "Paste your text here:",
    height=300,
    placeholder="Enter the text you want to summarize or rewrite."
)


# Button to trigger the analysis
if st.button("Analyze Document"):
    
    if not document_text.strip():
        st.warning("Please enter a document.")
    
    else:
        with st.status("📄 Processing Document...", expanded=True) as status:

            st.write("Generating summary...")
    

    # Call the Ollama API to get the summary or rewrite based on the user's choice
            summary_response = ollama.chat(
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
                    Generate a {summary_size} summary. 

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
                    "temperature": 0.2,
                    "num_predict": 2000, # set a high token limit to avoid the summary being cut off due to token limits.
                }
        )

            summary = summary_response["message"]["content"]
            st.write("Summary generated ✅")

            
            
            st.write("Generating rewritten content...")
            config = tone_config[tone]
            instruction = config["instruction"]


            #Api call to rewrite the content based on the selected tone and rewrite target 
            rewrite_response = ollama.chat(
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

            rewritten_text = rewrite_response["message"]["content"]
            st.write("Rewrite completed ✅")

            status.update(
                        label="✅ Analysis Complete",
                        state="complete",
                        
                    )



    # Display the summary and rewritten text in separate tabs
    tab1, tab2 = st.tabs(["📄 Summary", "✍️ Rewritten"])
    with tab1:
        st.subheader("📄 Summary")
        st.write(summary)
    with tab2:
        st.subheader("✍️ Rewritten Text")
        st.write(rewritten_text)