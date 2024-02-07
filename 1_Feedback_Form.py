import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI


st.title(":white[Custom Feedback Generator]")
st.header(":black_nib: Your Personalized Tutor, Constructive Feedback Made Easy",divider="rainbow")

st.markdown("""
    Welcome to the Feedback Generator, your tool for effortlessly creating constructive and personalized feedback. Whether you're a teacher providing feedback to students or a manager guiding your team, this tool streamlines the feedback generation process.
    """)

st.subheader("How it works?")
st.markdown("""
               1. Upload you Pdf Documents for evaluation.
               2. Once uploaded It starts Generating your Personalized Feedback. 
               3. It Delivers clear, constructive, and actionable feedback. 
            
            """)

col1, col2 = st.columns(2)

with col1:
    report_card = ""
    uploaded_files = st.file_uploader("Choose a Pdf file of Your Report Card")
    if uploaded_files:
        
        def report_extractor():
                reader_report = PdfReader(uploaded_files)
                raw_text1 = ''
                for i, page in enumerate(reader_report.pages):
                    text = page.extract_text()
                    if text:
                        raw_text1 += text
                return raw_text1
            
        report_card = report_extractor()
    
        st.write("Your Report Card data is extracted")

with col2:
    syllabus = ""
    uploaded_files1 = st.file_uploader("Choose a Pdf file of Your Syllabus")
    if uploaded_files1:
        
        def syllabus_extractor():
            reader_report = PdfReader(uploaded_files1)
            raw_text = ''
            for i, page in enumerate(reader_report.pages):
                text = page.extract_text()
                if text:
                    raw_text += text 
            return raw_text
            
        syllabus = syllabus_extractor()
        st.write("Your Syllabus data is extracted")

# Initialize a session state to store cleaned data
if 'cleaned_data' not in st.session_state:
    st.session_state.cleaned_data = None
if 'cleaning_done' not in st.session_state:
    st.session_state.cleaning_done = False
    
      
def cleaning(): 
    cleaned_data = None
    if report_card and syllabus and not st.session_state.cleaning_done:
            with st.spinner('Wait for it...Cleaning your data'):
                client = OpenAI(api_key=" ")
                response_cleaning = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"""Generate a cleaned data from the document:{report_card} as
                                            'Mathematics':extract_grade('Mathematics' : ),
                                            'World History':extract_grade('World History':),
                                            'Geography': extract_grade('Geography':),
                                            'Computer': extract_grade('Computer':),
                                            'Science': extract_grade('Science':),
                                            'English':extract_grade('English':),
                                            also from this{syllabus}document provide me a clean and structured data like
                                            SYLLABUS – 2021 - 2022,
                                            STANDARD: 10,
                                            SUBJECT: MATHEMATICS, etc"""},  # Your prompt for generating text
                    ]
                )
                
                # Get the generated text
                cleaned_data = response_cleaning.choices[0].message.content
                st.success("Data is cleaned, ready to generate feedback")
                st.session_state.cleaning_done = True
                st.session_state.cleaned_data = cleaned_data
    else:
                st.warning("Please extract both Report Card and Syllabus before generating feedback.")

    return cleaned_data
    
cleaned_data = cleaning()
# Debug prints
# st.write(f"cleaning_done: {st.session_state.cleaning_done}")
# st.write(f"cleaned_data: {st.session_state.cleaned_data}")

# st.write(response_message)           
if st.button("Generate Feedback"):
    if st.session_state.cleaned_data:
     with st.spinner('Wait for it...generating your data'):
            st.markdown("----")
            res_box = st.empty()           
            client = OpenAI(api_key=" ")
            report=[]
        
            for resp in client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"""provide some ways and feedback to improve my marks on the subjects based on the Document:

                                {st.session_state.cleaned_data}, """ },# Your prompt for generating text


                    ],
                    stream=True
                    
                ):

                    # Get the generated text

                delta_content = resp.choices[0].delta.content
                if delta_content is not None:
                    report.append(delta_content)
                if report:
                    res="".join(report).strip()
                    res_box.markdown(f'*{res}*')
                    

st.markdown("----")



     
























































































































































                    
                


           
        


