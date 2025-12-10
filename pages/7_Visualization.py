import streamlit as st, os
st.set_page_config(page_title="Visualization", layout="wide")
st.title("Visualization & Export")
st.info("This page will show model/train curves and allow exporting the model and artifacts.")
if os.path.exists('models/intent_model/training_losses.png'):
    st.image('models/intent_model/training_losses.png', caption='Training Losses')
if os.path.exists('models/intent_model/confusion_matrix.png'):
    st.image('models/intent_model/confusion_matrix.png', caption='Confusion Matrix')
if st.button('Download Model (zip)'):
    import zipfile, shutil
    zip_path = 'models/intent_model.zip'
    shutil.make_archive('models/intent_model','zip','models/intent_model')
    with open(zip_path,'rb') as f:
        st.download_button('Download', f, file_name='intent_model.zip')
