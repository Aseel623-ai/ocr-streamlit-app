import streamlit as st
import google.generativeai as genai
import pytesseract
from PIL import Image
import os



# عنوان التطبيق
st.title("LabResults AI")
st.markdown("---")



def load_model():
    genai.configure(api_key="AIzaSyBsA6ixodO7_ODrKGV6kRqiswdN_3n958A")
    return genai.GenerativeModel(model_name="gemini-2.0-flash")



model = load_model()


#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


st.header("تحميل صورة التحليل")
uploaded_file = st.file_uploader("قم بتحميل صورة التحليل الطبي", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة المحملة", width=400)


    if st.button("تحليل الصورة"):
        with st.spinner("جاري معالجة التحليل..."):

            extracted_text = pytesseract.image_to_string(image, lang='ara+eng')

            # عرض النص المستخرج في مربع نص قابل للطي
            with st.expander("النص المستخرج من الصورة"):
                st.text_area("النص المستخرج:", value=extracted_text, height=200)


            messages = [
                {
                    "role": "user",
                    "parts": [f"""أنت مساعد طبي ذكي.
مهمتك هي:
- قراءة نتائج التحاليل المرفقة.
- تلخيص النتائج بشكل تقرير طبي واضح.
- تقديم نصيحة طبية عامة حسب النتائج.
- اقتراح التخصص الطبي المناسب إن لزم.

نتائج التحاليل المستخرجة:
{extracted_text}"""]
                }
            ]


            try:
                response = model.generate_content(messages)

                # عرض النتائج في مربع بتصميم جميل
                st.success("تم تحليل الصورة بنجاح!")
                st.subheader("نتائج التحليل:")
                st.markdown(f"""
                <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border: 1px solid #ccc;">
                    {response.text}
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"حدث خطأ أثناء تحليل الصورة: {str(e)}")
                st.info("قد يكون السبب هو تجاوز حدود الاستخدام في واجهة برمجة Google Gemini API. يرجى المحاولة لاحقًا.")


st.sidebar.header("تعليمات الاستخدام")
st.sidebar.markdown("""
1. قم بتحميل صورة التحليل الطبي
2. انقر على زر "تحليل الصورة"
3. انتظر حتى تظهر النتائج
""")


st.sidebar.header("حول الخدمة")
st.sidebar.info("""
هذه الخدمة تستخدم:
- Google Gemini AI لتحليل النتائج
- Tesseract OCR لاستخراج النص من الصور
- Streamlit لواجهة المستخدم

يمكن قراءة النصوص العربية والإنجليزية من صور التحاليل الطبية وتقديم تحليل لها.
""")