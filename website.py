import tkinter as tk
from tkinter import messagebox
import requests
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

st.set_page_config(page_title = 'DR. MUMMY', page_icon = 'duffle-fill', layout = 'wide')

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = 'https://lottie.host/ae135ba7-a41d-49b2-8e7c-e1f8e600d372/O2iCm65aKU.json'
image_contact_form = Image.open("website/images/qrcode_localhost.png")

# with st.sidebar:
selected = option_menu(
    menu_title = None,
    options = ['Home', 'Remedies', 'Contact Us'],
    icons = ['house', 'book', 'envelope'],
    # menu_icon = 'cast',
    default_index = 0,
    orientation = 'horizontal',
    styles = {
        'nav-link': {
            'font-size' : '20px',
            'text-align' : 'center',
            'margin' : '0px',
            '--hover-color' : 'blue'}
    }
    )  

if selected == 'Home':
    with st.container():
        st.subheader('Discover wellness the natural way')
        st.title('Dr. MUMMY')
        st.write('Welcome to Dr. Mummy, your online health companion! Discover a holistic approach to wellness as we leverage the power of homemade remedies to treat various ailments. Our platform provides expert advice, curated home remedies, and a supportive community to guide you on your journey to better health. Embrace the natural path to healing with Dr. Mummy, where personalized care meets the comfort of home.')
        st.write('[Learn More](python/website/doctors)')

    with st.container():
        st.write('---')
        left_column,right_column = st.columns((2,1))
    with left_column:
        st.header('Why us?')
        st.write('If you don\'t believe in popping a pill every time you are down with mild fever or feeling a bit stick, then natural remedies can come to your rescue (but not always!). Right from getting soft, pink lips with homemade scrub to dealing with indigestion and pain, this section has everything you wish you knew about natural remedies or home remedies. BOOKMARK this page for every natural remedy under the roof right from quick-fixes for acidity and home remedies for bleeding gums to home cures for everyday hair care and skin care problems like dandruff, dry hair, split ends, acne, stretch marks and much more.')
    with right_column:
        st_lottie(lottie_coding, height = 300, key = 'coding')

    with st.container():
        st.write('---')
        st.header('You can also visit us here!!')
        st.write('##')
        image_column, text_column = st.columns((1,2))
    with image_column:
        st.image(image_contact_form)
    with text_column:
        st.subheader('Address')
        st.write('#314, Mall Road, adjoining clock tower building, Vancouver, Canada')
        st.write('Contact : 9372116902')
        st.write('Email : yuvkashi9779g@gmail.com')


if selected == 'Remedies':
    st.subheader('You will be redirected now...')
    
    remedies = {
    "Headache": ["Drink water", "Take a nap"],
    "Sore Throat": ["Gargle with warm salt water", "Honey and tea"],
    }

    def search_remedy():
        query = search_entry.get()
        if query in remedies:
            result_text.set("\n".join(remedies[query]))
        else:
            result_text.set("Remedy not found!")

    def add_remedy():
        disease = disease_entry.get()
        remedy = remedy_entry.get()
        
        if disease and remedy:
            if disease in remedies:
                remedies[disease].append(remedy)
            else:
                remedies[disease] = [remedy]
            messagebox.showinfo("Success", "Remedy added successfully!")
            disease_entry.delete(0, tk.END)
            remedy_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Both fields are required!")

    root = tk.Tk()
    root.title("Dr. Mummy")
    root.geometry('300x300')

    search_label = tk.Label(root, text="Search for a remedy:")
    search_label.pack()
    search_entry = tk.Entry(root)
    search_entry.pack()
    search_button = tk.Button(root, text="Search", command=search_remedy)
    search_button.pack()

    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text)
    result_label.pack()

    add_label = tk.Label(root, text="Add a remedy for a disease:")
    add_label.pack()
    disease_label = tk.Label(root, text="Disease:")
    disease_label.pack()
    disease_entry = tk.Entry(root)
    disease_entry.pack()
    remedy_label = tk.Label(root, text="Remedy:")
    remedy_label.pack()
    remedy_entry = tk.Entry(root)
    remedy_entry.pack()
    add_button = tk.Button(root, text="Add Remedy", command=add_remedy)
    add_button.pack()

    root.mainloop()

if selected == 'Contact Us':
    with st.container():
        st.write('---')
        st.header('Get in touch with us')
        st.write('##')
        contact_form = """
        <form action ="https://formsubmit.co/yuvakshi9779g@gmail.com" method="POST">
        <input type="hidden" name="_captcha" >
        <input type = "text" name = "name" placeholder = "Your name" required>
        <input type = "email" name = "email" placeholder = "Your email" required>
        <textarea name="message" placeholder="Your problem"></textarea>
        <button type = "submit">Send</button>
        </form>
        """

        st.markdown(contact_form, unsafe_allow_html = True)
    
        def local_css(file):
            with open(file) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

        local_css("website/style/style.css")


hide_st_style = """
            <style>
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
