import streamlit as st
from core.analyzer import ( generate_summary, rewrite_content)
from core.extractor import (extract_text)
from core.ollama_client import (get_models)
from core.analyzer import summary_config

# Function to analyze the document, generate summary and rewrite based on the selected tone and rewrite target
def analyze_document(document_text,selected_model,temperature,tone,rewrite_target,target_length):
    with st.status("📄 Processing Document...", expanded=True) as status:

        st.write("Generating summary...")
        
        # Generate summary
        try:
            summary = generate_summary(document_text,target_length,selected_model)

        except Exception as e:
            st.error(f"Summary Generation Failed: {e}")
            return
        st.success("Summary generated")

        st.write("Generating rewritten content...")
        # Generate rewritten content using helper
        try:
            rewritten_text = rewrite_content(document_text,summary, tone,temperature,rewrite_target,selected_model)

        except Exception as e:
            st.error(f"Rewriting Failed: {e}")
            return
        st.success("Rewritten text generated")

        status.update(
            label="✅ Analysis Complete",
            state="complete",
        )

    #Display the summary and rewritten text in separate tabs
    sum_tab1, rewrite_tab2 = st.tabs(["📄 Summary", "✍️ Rewritten"])
    with sum_tab1:
            st.subheader("📄 Summary")
            st.write(summary)
    with rewrite_tab2:
            st.subheader("✍️ Rewritten Text")
            st.write(rewritten_text)


# Function to show the preview of the extracted text from the uploaded document
def show_preview(document_text):
    try:
        st.text_area(
            "Preview",
            document_text[:2000],
            height=200,
        )
    except Exception as e:
        st.error(f"Preview Generation Failed: {e}")

# Function to process the extracted text, show the preview and analyze the document based on the extracted text
def process_extracted_text(document_text, file_type,selected_model, temperature, tone, rewrite_target, target_length):
    if document_text.strip():
        st.success(
            f"{file_type} extracted successfully ✅"
        )
        show_preview(document_text)
        analyze_document(document_text, selected_model, temperature, tone, rewrite_target, target_length)
    else:
        st.error(
            f"No text extracted from {file_type}"
        )

def app():
    # side bar 
    with st.sidebar:
        st.title('🦙💬 Llama summarizer')
        

        # Get the list of available models from Ollama and show it in the dropdown menu
        model_names = get_models()
        selected_model = st.selectbox("Choose Model",model_names)


        # To choose the temperature and show it in the slider
        temperature = st.slider("Temperature",0.0,1.0,0.7)


        # To choose the summary length and show it in the dropdown menu
        st.subheader("Summary Settings")

        summary_size = st.selectbox(
            "Summary Length",
            ["Short", "Medium", "Long"]
        )
        
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

    tab1, tab2 = st.tabs(
        ["📝 Text Document", "📂 Upload Document"]
    )

    with tab1:
        #Text Box to paste the document to be analyzed
        document_text = st.text_area(
            "Paste your text here:",
            height=300,
            placeholder="Enter the text you want to summarize or rewrite.",
        )


        # Button to trigger the analysis
        analyze_button = st.button("Analyze Document")
        #analyze_button Logic
        if analyze_button:
            if not document_text.strip():
                st.warning("Please enter a document.")
            
            else:
                analyze_document(document_text,selected_model,temperature,tone,rewrite_target,target_length)


    #File uploader to upload the document to be analyzed 
    with tab2:
        uploaded_file = st.file_uploader(
            "Upload a document",
            type=["pdf", "docx", "pptx", "txt"]
        )
        # Button to trigger the analysis of the uploaded document
        analyze_upload = st.button(
            "Analyze Uploaded Document"
        )
        #Analyze_Upload Button Logic
        if analyze_upload:

            if not uploaded_file:

                st.warning("Please upload a document.")

            else:

                try:
                    st.success("Document uploaded successfully ✅")
                    with st.expander("📄 Document Details"):
                        st.write(f"📄 File Name: {uploaded_file.name}")
                        st.write(f"📁 File Type: {uploaded_file.type}")
                        st.write(
                            f"📊 Size: {uploaded_file.size / 1024:.2f} KB"
                        )

                   
                    # For each file type, extract the text and then show the preview
                    # and analyze the document based on the extracted text.
                    document_text = extract_text(uploaded_file, uploaded_file.name)

                    process_extracted_text( document_text, uploaded_file.name, selected_model, temperature, tone, rewrite_target, target_length)

                except Exception as e:

                    st.error(
                        f"Error reading file: {e}"
                    )



if __name__ == "__main__":
    app()