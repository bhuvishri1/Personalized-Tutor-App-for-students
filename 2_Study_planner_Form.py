import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI

st.title(":white[Study Planner]")
st.header("Your Tailored Learning for Success",divider="rainbow")

st.markdown("""
    Welcome to the Study Planner, your personalized assistant for creating effective study plans. Whether you're preparing for exams, learning a new skill, or organizing your daily study routine, the Study Planner has got you covered.
    """)

st.subheader("How it works?")
st.markdown("""
    1. Upload your Syllabus pdf 
    2. Once Uploaded Select your Plan on How you want to Prepare for the Studies
    - **Goal-Oriented Planning**: Align your study sessions with your academic and personal goals.
    - **Flexibility**: Adapt your study plan to fit your changing schedule and priorities.
    """)

st.subheader("Benefits of Using the Study Planner")
st.markdown("""
    - **Efficiency Boost**: Optimize your study time and make the most out of each session.
    - **Reduced Stress**: A well-organized plan reduces stress and promotes a balanced approach to learning.
    - **Consistency**: Build a consistent study routine for better retention and understanding.
    """)

syllabus=""
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


if syllabus:
    plan = st.radio("Select your plan",["Daily","Weekly","Monthly"],index=None)
    if plan:
     with st.spinner('Wait for it...Generating your study plan'):
        st.markdown("----")
        res_box = st.empty() 
        client = OpenAI(api_key=" ")
        report=[]
        for resp in client.chat.completions.create(
          model="gpt-3.5-turbo",
        
          messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"""provide me a study plan for{plan}to prepare on the Document:

                    {syllabus}, """ },# Your prompt for generating text


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