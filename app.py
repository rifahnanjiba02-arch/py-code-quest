from services.groq_service import get_hint
import streamlit as st
import json

#setup
st.set_page_config(page_title="PyCodeQuest", page_icon="🐍")
st.title("PyCodeQuest")
st.write("Solve the challenge by writing a Python function.")

#load data
with open("data/challenges.json","r") as f:
    challenges = json.load(f)

#state
if "current_level" not in st.session_state:
    st.session_state.current_level=1

if "level_passed" not in st.session_state:
    st.session_state.level_passed =False

if "results" not in st.session_state:
    st.session_state.results = []

#get current challenge
challenge = challenges[
    st.session_state.current_level - 1
]

#header
st.markdown(f"Level {challenge['id']}")
st.subheader(challenge["title"])
st.caption(f"{challenge['topic']}|{challenge['difficulty']}")

progress = min(
    st.session_state.current_level,
    len(challenges)
)/ len(challenges)
st.progress(progress)

st.write(challenge["description"])

st.markdown("---")

#code input
code = st.text_area(
     "Your Solution",
     height=200,
     placeholder="Write your Python function here...",
     key= f"code_level_{st.session_state.current_level}"
     )

#submit logic
def run_tests(user_code, challenge):
    namespace= {}
    try:
        exec(code,namespace) #run user code
    except Exception as e:
        return False, [{"error": str(e)}]

    #get function name from challenge
    func = namespace.get(challenge["function_name"]) 
    if func is None:
            return False, [{"error": "Function not found"}]
    
    results=[]
    all_passed= True

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

                except Exception as e:
                    results.append({
                        "test": i,
                        "input": test["input"],
                        "error": str(e),
                        "passed": False
                    })

                    all_passed= False
    
    return all_passed, results

#submit button
if st.button("Submit"):
    all_passed, results= run_tests(code, challenge)
    st.session_state.results= results

    if all_passed:
        st.session_state.level_passed= True
        st.balloons()
        st.success("Level Complete!")
    else:
        st.session_state.level_passed= False
        st.error("Some tests failed!")

        #show hint only once
        failed_test = next((r for r in results if not r.get("passed", True)), None)

        if failed_test and "error" not in failed_test:
            hint= get_hint(challenge,
                           {
                               "input": failed_test["input"],
                               "expected": failed_test["expected"]
                           },
                           failed_test["got"],
                           code
                           )
            st.info("AI Hint")
            st.write(hint)

#next level 
if st.session_state.level_passed:
        if challenge["id"] < len(challenges):
            if st.button("Next Level"):
                st.session_state.current_level += 1
                st.session_state.level_passed = False
                st.session_state.results= []
                st.rerun()

        else:
             st.success("You completed all levels!")

#test results
if st.session_state.results:
        st.markdown("---")
        st.subheader("Test Results")

        for r in st.session_state.results:
            if r.get("passed"):
                st.success(f"Test {r['test']} passed!")

            elif "error" in r:
                 st.error(f"Error: {r['error']}")
            else:
                 st.error(f"Test {r['test']} failed")
                 st.write("Expected:",r["expected"])
                 st.write("Got:",r["got"])
                  

       