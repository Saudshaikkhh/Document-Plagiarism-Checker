import streamlit as st
import tempfile
import os
from plagiarism_backend import process_document, save_report_to_pdf

# Check for API token
if not os.environ.get("AZURE_TOKEN"):
    st.error("⚠️ Azure API token not found. Please add your AZURE_TOKEN in the environment variables.")
    st.info("Contact your administrator to set up the Azure AI token for plagiarism detection.")
    st.stop()

# Configure Streamlit page
st.set_page_config(
    page_title="Document Plagiarism Checker",
    page_icon="📄",
    layout="centered"
)

# Main title
st.title("📄 Document Plagiarism Checker")
st.markdown("Upload your DOCX or PDF document to check for plagiarism and generate an assessment report.")

# File upload section
st.header("📁 Upload Document")
uploaded_file = st.file_uploader(
    "Choose a file",
    type=["docx", "pdf"],
    help="Upload a DOCX or PDF file containing A.C. sections for plagiarism analysis"
)

if uploaded_file is not None:
    # Display file information
    st.success(f"File uploaded: {uploaded_file.name}")
    st.info(f"File size: {uploaded_file.size} bytes")
    
    # Get file extension
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    # Process button
    if st.button("🔍 Process Document", type="primary"):
        try:
            # Create progress bar and status container
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Prepare file
            status_text.text("📁 Preparing file for processing...")
            progress_bar.progress(10)
            
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_file_path = tmp_file.name
            
            # Step 2: Extract A.C. sections
            status_text.text("📖 Extracting A.C. sections from document...")
            progress_bar.progress(25)
            
            if file_extension == "docx":
                from plagiarism_backend import extract_ac_sections_from_docx
                ac_sections = extract_ac_sections_from_docx(temp_file_path)
            else:  # pdf
                from plagiarism_backend import extract_ac_sections_from_pdf
                ac_sections = extract_ac_sections_from_pdf(temp_file_path)
            
            if not ac_sections:
                raise ValueError("No A.C. sections found in the document")
            
            # Step 3: Detect document topic
            status_text.text("🎯 Analyzing document topic...")
            progress_bar.progress(35)
            
            from plagiarism_backend import detect_document_topic
            sample_content = next(iter(ac_sections.values()))
            document_topic = detect_document_topic(sample_content)
            
            # Step 4: Process each A.C. section with AI
            total_sections = len(ac_sections)
            ac_results = {}
            
            # Show found sections info with sorting
            sorted_sections = sorted(ac_sections.keys(), key=lambda x: float(x))
            st.info(f"Found {total_sections} A.C. sections: {', '.join(sorted_sections)}")
            
            # Show complete sequence that will be generated
            section_numbers = [float(k) for k in ac_sections.keys()]
            if section_numbers:
                # Calculate expected complete sequence
                major_numbers = {}
                for ac_num in ac_sections.keys():
                    parts = ac_num.split('.')
                    major = int(parts[0])
                    minor = int(parts[1])
                    if major not in major_numbers:
                        major_numbers[major] = []
                    major_numbers[major].append(minor)
                
                complete_sequence = []
                for major in sorted(major_numbers.keys()):
                    minors = major_numbers[major]
                    min_minor = min(minors)
                    max_minor = max(minors)
                    for minor in range(min_minor, max_minor + 1):
                        complete_sequence.append(f"{major}.{minor}")
                
                missing_sections = [ac for ac in complete_sequence if ac not in ac_sections]
                if missing_sections:
                    st.info(f"📋 Complete sequence will be: {', '.join(complete_sequence)}")
                    st.warning(f"⚠️ Missing sections to be added: {', '.join(missing_sections)}")
                else:
                    st.success(f"✅ Perfect sequence found: {', '.join(complete_sequence)}")
            
            for i, (ac_num, content) in enumerate(ac_sections.items()):
                section_progress = 40 + (i * 30 // total_sections)
                status_text.text(f"🤖 Analyzing A.C. {ac_num} with AI ({i+1}/{total_sections})...")
                progress_bar.progress(section_progress)
                
                from plagiarism_backend import gpt_plagiarism_check, parse_gpt_response
                
                try:
                    # Get AI response with timeout handling
                    with st.spinner(f"Processing A.C. {ac_num}..."):
                        gpt_response = gpt_plagiarism_check(ac_num, content, document_topic)
                    
                    # Debug: Show raw response (you can remove this later)
                    with st.expander(f"Debug: A.C. {ac_num} Raw AI Response", expanded=False):
                        st.text(gpt_response)
                    
                    # Parse the response
                    parsed_result = parse_gpt_response(gpt_response)
                    
                    # Debug: Show parsed result
                    with st.expander(f"Debug: A.C. {ac_num} Parsed Result", expanded=False):
                        st.json(parsed_result)
                    
                    ac_results[ac_num] = parsed_result
                    
                    # Show progress for this section
                    st.success(f"✅ A.C. {ac_num} completed - Score: {parsed_result['score']}, Status: {parsed_result['plagiarism']}")
                    
                except Exception as section_error:
                    st.warning(f"⚠️ A.C. {ac_num} processing failed: {str(section_error)}")
                    # Add fallback result for failed sections
                    ac_results[ac_num] = {
                        'plagiarism': 'No',
                        'score': '10%',
                        'level': 'Low',
                        'feedback': f'Processing failed for A.C. {ac_num} due to technical issues. Manual review recommended.'
                    }
            
            # Step 5: Generate report
            status_text.text("📊 Generating assessment report...")
            progress_bar.progress(75)
            
            from plagiarism_backend import generate_report
            report_text = generate_report(ac_results, document_topic)
            
            # Step 6: Create PDF
            status_text.text("📄 Creating PDF report...")
            progress_bar.progress(90)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
                pdf_file_path = pdf_file.name
            
            save_report_to_pdf(report_text, pdf_file_path, document_topic)
            
            # Step 7: Complete
            status_text.text("✅ Processing complete!")
            progress_bar.progress(100)
            
            # Store results in session state
            st.session_state.report_ready = True
            st.session_state.pdf_file_path = pdf_file_path
            st.session_state.document_topic = document_topic
            st.session_state.ac_count = len(ac_results)
            
            # Clean up temp input file
            os.unlink(temp_file_path)
                
            st.success("✅ Document processed successfully!")
            
            # Display summary
            st.header("📋 Processing Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Document Topic", st.session_state.document_topic)
            
            with col2:
                st.metric("A.C. Sections Found", st.session_state.ac_count)
                
            with col3:
                pass_count = sum(1 for data in ac_results.values() 
                               if data.get('plagiarism', '').lower() == 'no' or 
                               data.get('level', '').lower() in ['low', 'medium'])
                st.metric("Pass Rate", f"{pass_count}/{len(ac_results)}")
            
            # Show detailed results table
            st.subheader("📊 Detailed Results")
            results_data = []
            for ac_num, data in ac_results.items():
                plagiarism = data.get("plagiarism", "No")
                score = data.get("score", "0%")
                level = data.get("level", "Low")
                feedback_preview = data.get("feedback", "No feedback")[:100] + "..."
                decision = "Pass" if plagiarism.lower() == "no" or level.lower() in ["low", "medium"] else "Redo"
                
                results_data.append({
                    "A.C. No": ac_num,
                    "Decision": decision,
                    "Plagiarism Score": score,
                    "Level": level,
                    "Feedback Preview": feedback_preview
                })
            
            st.dataframe(results_data, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error processing document: {str(e)}")
            # Clean up temp file if it exists
            try:
                if 'temp_file_path' in locals():
                    os.unlink(temp_file_path)
            except:
                pass

# Download section
if hasattr(st.session_state, 'report_ready') and st.session_state.report_ready:
    st.header("📥 Download Report")
    
    # Read the PDF file
    try:
        with open(st.session_state.pdf_file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        
        # Create download button
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_data,
            file_name=f"plagiarism_report_{st.session_state.document_topic.replace(' ', '_')}.pdf",
            mime="application/pdf",
            type="primary"
        )
        
        st.success("Report generated successfully! Click the button above to download.")
        
        # Clean up PDF file after download
        if st.button("🗑️ Clear Report", help="Clear the current report and start over"):
            try:
                os.unlink(st.session_state.pdf_file_path)
            except:
                pass
            
            # Clear session state
            for key in ['report_ready', 'pdf_file_path', 'document_topic', 'ac_count']:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Error preparing download: {str(e)}")

# Instructions section
st.header("📝 Instructions")
with st.expander("How to use this tool"):
    st.markdown("""
    1. **Upload File**: Choose a DOCX or PDF document containing Assessment Criteria (A.C.) sections
    2. **Process**: Click the "Process Document" button to analyze the content
    3. **Download**: Once processing is complete, download the generated PDF report
    
    **Requirements**:
    - Document must contain sections starting with "A.C. X.X COVERED"
    - Supported formats: DOCX, PDF
    - Maximum file size: 200MB
    
    **Report Contains**:
    - Plagiarism assessment for each A.C. section
    - Pass/Redo recommendations
    - Professional tutor feedback
    - Detailed analysis and scoring
    """)

# Footer
st.markdown("---")
st.markdown("*Powered by Azure AI and advanced plagiarism detection algorithms*")
