import streamlit as st
import ollama

#side bar 
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
    summary_lengths = {
    "Short": 150,
    "Medium": 400,
    "Long": 800
}
    max_tokens = summary_lengths[summary_size] # Set max_tokens based on the selected summary size

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
        st.success("Document received!")
    # Call the Ollama API to get the summary or rewrite based on the user's choice
    response = ollama.chat(
        model=selected_model,
        
       messages=[
    {
        "role": "system",
        "content": "You are an expert document analyst."
    },
    {
        "role": "user",
        "content": f"Summarize:\n\n{document_text}"

    }
],
        options={
            "temperature": temperature,
            "num_predict": max_tokens
        }
 )

    st.write(response["message"]["content"])