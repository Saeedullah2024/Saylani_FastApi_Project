import streamlit as st 
from datetime import date
import pandas as pd



st.title("Hello World!")
st.subheader("Streamlit")
st.text("Hello bachat")

llm = st.selectbox("Your option" , ["Gpt-4" , "Gpt-5" , "Gemini" , "Anthropic"])
st.write(f"Your choice {llm} best choice")
st.success("Sucessfully created")

option = st.radio("Chose Your Option" , ["Only Chai" , "Chai With Biscuit" , "Sugar+Chai+Biscuit" , "None"])
st.write(f"You have selected {option}")
if option == "Only Chai":
    st.write("You Bill is 10$")
elif option == "Chai With Biscuit":
    st.write("Your Bill is 12$")
elif option == "Sugar+Chai+Biscuit":
    st.write("Your Bill is 15$")
else :
    st.write("Selected None")

slider = st.slider("select your budget in $" , 0,120,70)
st.write(f"Your budget is around {slider}")
if slider >= 60 and slider<=100:
    st.write("That Normal No worry")
elif slider>=100 and slider <=120:
    st.write("The Big Issue!!!")
else:
    pass

number = st.number_input("Enter your age ", min_value=18 , max_value=65 , step=1)
st.write(f"Your age is {number}")

text = st.text_input("Enter your name : ")
st.write(f"Welcome , {text}")

dob = st.date_input(f"Enter your Date of birth: " , min_value=date(2000 , 1 , 1) ,  max_value=date.today())
if dob:
    today = date.today()
    
    age = today.year - dob.year - (
        (today.month, today.day) < (dob.month, dob.day)
    )
    
    st.write("Your age is:", age)

col1 , col2 = st.columns(2)

with col1:
    st.header("This is your car")
    st.image("https://www.nation.com.pk/07-Sep-2018/all-set-to-introduce-latest-cars-in-pakistan" , width=500)
    vote1 = st.button("Click to buy")
with col2: 
    st.header("This is your Bike")
    st.image("https://trims.pk/blogs/news/heavy-bike-price-in-pakistan" , width=500)
    vote2 = st.button("Click to Bike")

name = st.sidebar.text_input("Enter your name: ")
welcome_text = st.sidebar.text_input("Some Greetings: ")
st.write(f"Hello {name} may {welcome_text}")

#Used to show big messsage
with st.expander("How to Build FastApi"):
    st.write("""
             1. Run pip install fastapi
             2. Write the code
             3. use uvicorn __filename__:app --reloadl
             
""")

file = st.file_uploader("Upload your file:", ["json", "csv"])

if file is not None:
    st.header("File Preview")
    if file.name.endswith(".json"):
        df = pd.read_json(file)
        st.dataframe(df)
        stats = df.describe()
        st.dataframe(stats)
        
    elif file.name.endswith(".csv"):
        df = pd.read_csv(file)
        st.dataframe(df)
        stats = df.describe()
        st.dataframe(stats)
    else:
        st.error("Unsupported file type")