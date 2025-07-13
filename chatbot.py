import streamlit as st
import ollama
import time

def main():
    if st.button("🔙 Back to App"):
        st.session_state["page"] = "home"
        st.rerun()


    st.markdown("## 🤖 Get Help - AI Credit Agent")
    st.info("Ask me about banking terms, your loan application, or anything in this project.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask a question...")
    if prompt:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""

            stream = ollama.chat(
                model="gemma3",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant in a DeFi credit loan app. . Detect the user's language "
            "and always reply in the same language Keep answers short, clear, and in bullet points or under 5 lines."},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )

            for chunk in stream:
                word = chunk["message"]["content"]
                full_response += word
                placeholder.markdown(full_response + "▌")
                time.sleep(0.02)

            placeholder.markdown(full_response)
            st.session_state["messages"].append({"role": "assistant", "content": full_response})

# Only run standalone if needed
if __name__ == "__main__":
    main()