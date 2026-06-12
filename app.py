import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st
import json
import re

load_dotenv(".env.local")

client =Groq(api_key=os.getenv("GROQ_API_KEY"))

def clean_ai_output(text):
    # remove <think>...</think>
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return text.strip()

def get_hint(challenge,test,got,code):
    prompt = f"""
You are a coding tutor. Reply back to the user.

IMPORTANT:
Do NOT include <think>, reasoning tags, or explanations of your thinking.

Only give a short hint.

Problem:
{challenge['description']}

Student Code:
{code}

Failed Test:
Input: {test.get('input')}
Expected: {test.get('expected')}
Got: {got}

Give only a short hint.
"""
    response= client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[{"role":"user", "content": prompt}]
    )
    return clean_ai_output(response.choices[0].message.content)

st.set_page_config(page_title="PyCodeQuest", page_icon="🐍")
st.title("PyCodeQuest")
st.write("Solve the challenge by writing a Python function.")

with open("data/challenges.json","r") as f:
    challenges = json.load(f)

challenge = challenges[0]

st.subheader(challenge["title"])
st.write(challenge["description"])

st.markdown("---")
code = st.text_area("Your Solution", height=200, placeholder="Write your Python function here...")

if st.button("Submit"):
    try:
        namespace={} #create safe namespace    
        try:
            exec(code,namespace) #run user code
        except Exception as e:
            st.error(f"Code Error: {str(e)}")
            st.stop

        #get function name from challenge
        func = namespace.get(challenge["function_name"]) 

        #check if functions exists
        if func is None:
            st.error(f"Function '{challenge['function_name']}' not found!")
        else:
            #run tests
            st.markdown("---")
            st.subheader("Running Tests...")

            results= []
            all_passed= True

            hint_shown = False

            for i, test in enumerate(challenge["tests"], start=1):
                try:
                    result= func(*test["input"])
                    expected= test["expected"]

                    passed = result == expected
                    results.append({
                        "test": i,
                        "input": test["input"],
                        "expected": expected,
                        "got": result,
                        "passed": passed
                    })
                    if not passed:
                        all_passed= False
                        if not hint_shown:
                            hint_shown= True
                            st.info("AI HINT")

                            hint=get_hint(
                                challenge,
                                test,
                                result,
                                code
                            )
                            st.write(hint)

                except Exception as e:
                    results.append({
                        "test": i,
                        "input": test["input"],
                        "error": str(e),
                        "passed": False
                    })

                    all_passed= False

            #ui display
            st.subheader("Test Results")
            if all_passed:
                st.balloons()
                st.success("All tests passed")
            else:
                st.error("Some tests failed")

            with st.expander("View Test Details"):
                
                for r in results:
                    if r["passed"]:
                        st.success(f"Test {r['test']} passed!")
                        continue
                    st.error(f"Test {r['test']} failed")
                    st.write("Input", r["input"])

                    if "error" in r:
                        st.write("Error", r["error"])
                    else:
                        st.write("Expected:",r["expected"])
                        st.write("Got", r["got"])

            st.markdown("---")

            
                
    except Exception as e:
        st.error(f"Error: {str(e)}")
    

   

         
