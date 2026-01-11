import streamlit as st

def main():
    st.title("AI Powered Chatbot")
    st.write("Your Streamlit App is Running Successfully!")

    user_input = st.text_input("Enter your message:")

    if st.button("Send"):
        st.write("You said:", user_input)

if __name__ == "__main__":
    main()
     