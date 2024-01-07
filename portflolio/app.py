from PIL import Image
import requests
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(page_title="My Webpage",page_icon="😇",layout="wide")

def load_lottieurl(url):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

local_css("portfoliostyle/style.css")

# -------- LOAD ASSETS --------------
lottie_coding=load_lottieurl("https://lottie.host/5f41d41d-b353-4eb4-b52a-fb8c3b7912da/He1aobP7P3.json")
img_header=Image.open("portfolio_images/header.png")
img_sections=Image.open("portfolio_images/sections.png")
img_ci=Image.open("portfolio_images/connectindia.png")

# -------- HEADER SECTION ------------
with st.container():
    st.subheader("Hi, I am Himanshi 🙋🏻‍♀️ ")
    st.title("A Student From India")
    st.write("I am passionate about the use of AI and ML to change the world of development and revolutionalize the world of computer science.")
    st.write("[Github: >](https://github.com/taemochi12)")


# ------ WHAT I DO -----------
with st.container():
    st.write("---")     #to create a divider
    left_column,right_column=st.columns(2)
    with left_column:
        st.header("What I do")
        st.write("##")      #to insert some space
        st.write(
            """
            I'm interested in doing:
            - Full Stack Development
            - AI, ML
            - Data Science
            - Cybersecurity
            - AR/VR
            - Jobs like: Github Campus Expert to showcase my public speaking and confidence
            """
        )
        st.write("[LinkedIn >](https://www.linkedin.com/in/himanshibhardwaj12/)")

    with right_column:
        st_lottie(lottie_coding,height=420,key="coding")


# ------- PROJECTS ----------
with st.container():
    st.write("---")
    st.header("My Projects")
    st.write("##")
    image_column,text_column=st.columns((1,2))      #text column will be twice as bigger as image column
    with image_column:
        st.image(img_header)
    
    with text_column:
        st.subheader("A Birthday Website")
        st.write(
            """
            It is a website to wish your loved ones a happy birthday !
            It has a beautiful ui with some pictures and has a birthday letter, a birthday video and a virtual cake with which one can play be again and again blowing candles by clicking on them and getting a birthday wish! 
            """
        )
        st.markdown("[Visit Website...](https://birthdaywebsite.vercel.app/home.html)")
with st.container():
    st.write("##")
    image_column,text_column=st.columns((1,2))      #text column will be twice as bigger as image column
    with image_column:
        st.image(img_ci)
    
    with text_column:
        st.subheader("A Website to connect Travellers")
        st.write(
            """
             It is an all-in-one website which offers three major options collectively based on the city the user is searching for- Explore, Accomodation Booking and Guide Booking.
            """
        )
        st.markdown("[Visit Website...](https://connect-india.vercel.app/)")


# ---- CONTACT ------
with st.container():
    st.write("---")
    st.header("Get In Touch With Me!")
    st.write("##")
    contact_form= """
    <form action="https://formsubmit.co/bhrdwj1218@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your Name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here" required></textarea>
     <button type="submit">Send</button>
    </form>
    """

    left_column,right_column=st.columns(2)
    with left_column:
        st.markdown(contact_form,unsafe_allow_html=True)
    with right_column:
        st.empty()
