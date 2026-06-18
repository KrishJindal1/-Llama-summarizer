import argparse
from core.analyzer import(generate_summary, rewrite_content)
from core.extractor import(extract_text)


def main():
    parser = argparse.ArgumentParser(description="Document Analysis and Rewriting CLI")
    parser.add_argument("action", choices=["summarize", "rewrite"], help="Action to perform")
    parser.add_argument("--file-path", help="Path to the document file")
    parser.add_argument("--text",help="Direct text input for analysis or rewriting (optional, overrides file input)")
    parser.add_argument("--model", default="llama3.2:3b", help="Model to use for analysis and rewriting default is llama3.2:3b")
    parser.add_argument("--length", default="medium", choices=["short", "medium", "long"], help="Target length for the summary")
    parser.add_argument("--tone", default="Professional",choices=["Professional", "Formal", "Casual", "Executive", "Technical", "Academic", "Marketing", "Simple English"], help="Tone for rewriting")
    parser.add_argument("--temperature", type= float, default=0.5,help="Temperature for controlling creativity in rewriting (0.0 to 1.0)")
    args = parser.parse_args()

    try:
        if args.text:
            document_text = args.text
        else:
            with open(args.file_path, "rb") as uploaded_file:
                document_text = extract_text(uploaded_file, args.file_path)
        
        if args.action == "summarize":
            summary = generate_summary(document_text, args.length, args.model)
            print("Summary:")
            print(summary)

        elif args.action == "rewrite":
            
            rewritten_content = rewrite_content(document_text, args.tone, args.temperature, args.action, args.model)
            
            print("\nRewritten Content:")
            print(rewritten_content)
    except Exception as e:        
       
        print(f"Error processing the document: {e}")

if __name__ == "__main__":
    main()