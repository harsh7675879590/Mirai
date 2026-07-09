import streamlit as st

def main():
    # Task 1: The UI Shell
    st.set_page_config(page_title="Echo Chamber 9000", page_icon="📡")
    st.title("Echo Chamber 9000")
    st.write("Welcome to the Echo Chamber. Please enter your name and the message you wish to transmit to the Void.")

    # Task 2: Multi-Data Collection
    user_name = st.text_input("Name", placeholder="Enter your name here...")
    user_message = st.text_input("Message", placeholder="Enter your message here...")

    # Task 3: The Action Gate
    if st.button("Transmit", type="primary"):
        # Task 4: Conditional Routing (Edge Cases)
        # Using .strip() to ensure a string of only spaces is also considered empty
        if not user_name.strip():
            st.error("Please provide your name.")
        elif not user_message.strip():
            st.warning("Please type a message to transmit.")
        else:
            # Task 5: The Formatted Output
            st.success(f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}")
            
            # Advanced Challenge: Token Cost Estimator
            char_length = len(user_message)
            token_count = char_length / 4
            
            st.info(f"System Check: Your message will consume approximately {token_count:g} tokens from our context window.")

if __name__ == "__main__":
    main()
