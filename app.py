import streamlit as st
import json

st.title("PyCodeQuest")

with open("data/challenges.json","r") as f:
    challenges = json.load(f)

challenge = challenges[0]

st.subheader(challenge["title"])
st.write(challenge["description"])

code = st.text_area("Write your Python code here", height=200)

if st.button("Submit"):
    try:
        namespace={} #create safe namespace    
        
        exec(code,namespace) #run user code

        #get function name from challenge
        func_name=challenge["function_name"]
        func = namespace.get(func_name) 

        #check if functions exists
        if func is None:
            st.error(f"Function '{func_name}' not found!")
        else:
            #run tests
            all_passed= True

            for test in challenge["tests"]:
                input_data= test["input"]
                expected = test["expected"]

                result = func(*input_data)

                if result != expected:
                    all_passed = False
                    st.error(
                        f"FAILED: input {input_data}"
                        f"expected {expected} got {result}"
                    )
                    break
            if all_passed:
                st.success("All tests passed!")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    

   

         
