import streamlit as st
import os
from dotenv import load_dotenv
import time

final_arr=[]
load_dotenv()


if "info" not in st.session_state:
    st.session_state.info = None
#################################################################################
# App elements

st.set_page_config(layout="wide")
st.title("Video Analytics Dashboard")

# variables
MAIN_VIDEO = "./One_Mans_Mission_to_Revive_the_Last_Redwood_Forests_short.mp4"
MAIN_ACTIONS = "./actionSummary.json"
MAIN_CHAPTERS = "./chapterBreakdown.json"

# read actionSummary-sample-nch-01-10min-mma.json into a JSON object
import json
with open(MAIN_ACTIONS) as f:
    data = json.load(f)

# Assuming 'data' is a list of dictionaries and you want to use the 'name' key
# actions = [{item["Start_Timestamp"]:item["actions"]} for item in data]  # Replace "name" with the actual key you want to use

actions = {}
for item in data:
    # actions[item["Start_Timestamp"]] = item["actions"]
    actions[f"{item['Start_Timestamp']} - {item['actions']}"] = item["actions"]


# Create a selectbox with the dictionary items
selected_option = st.selectbox(
    'Select a detected scene:',
    list(actions.keys())
)

# Get the value of the selected option
selected_value = actions[selected_option]

# st.write(f"Selected option: {selected_option}")
st.write(f"## Selected scene: {selected_value}")

selected_timestamp = selected_option.split("-")[0].strip()

# Find the element in the data that matches the selected timestamp
matching_element = None
for element in data:
    if element.get("Start_Timestamp") == selected_timestamp:
        matching_element = element
        break

start_time = int(float(matching_element.get("Start_Timestamp").replace('s', '')))
end_time = int(float(matching_element.get("End_Timestamp").replace('s', '')))      

with st.container(border=True):

    # dashboard with key metrics
    col1, col2, col3= st.columns([2, 1, 3])

    with col1:
        container = st.container(border=True)
        container.caption("Scene summary")
        container.write(f"{matching_element.get('summary')}")

        container = st.container(border=True)
        container.caption("Characters")
        container.write(f"{matching_element.get('characters')}")

        container = st.container(border=True)
        container.caption("Actions")
        container.write(f"{matching_element.get('actions')}")

    with col2:
        container = st.container(border=True)
        container.caption("Key object")
        container.write(f"{matching_element.get('key_objects')}")




        container = st.container(border=True)
        container.caption("Scene theme")
        container.write(f"{matching_element.get('scene_theme')}")

        container = st.container(border=True)
        container.caption("Scene sentiment")
        container.write(f"{matching_element.get('sentiment')}")

        container = st.container(border=True)
        container.caption("Scene length")
        container.write(f"{end_time - start_time} s")
    with col3:
        st.video(MAIN_VIDEO, start_time=start_time, end_time=end_time, autoplay=True)

    with st.expander("Scene details", expanded=False):
        st.write(matching_element)

# Ask a question to a video
qna_container = st.container(border=True)
with qna_container:
    with st.expander("Ask a question"):
        # display the JSON object
        question = st.text_input("Ask a question")
        if st.button("Submit"):
            st.session_state.info = question
            
            #Note: The openai-python library support for Azure OpenAI is in preview.
            #Note: This code sample requires OpenAI Python library version 1.0.0 or higher.
            import os
            from openai import AzureOpenAI

            client = AzureOpenAI(
            azure_endpoint = "https://openaimmaswe.openai.azure.com/", 
            api_key=os.getenv("AZURE_OPENAI_KEY"),  
            api_version="2024-02-15-preview"
            )


            system_prompt_template = """You are a movie analyst assistant which helps analyze video content from transcriptions, frame descriptiojns, scenes summary etc. 
            
            ### RULES
            - You are given a movie file described by AI in a format of list of JSON entries.
            - Your answers **MUST** be allways based on Movie Description below. 
            - Do NOT create any other infromation. Do not make up information.
            - Allways format your answer as a JSON from the orginal file.
            
            Format Example:\n[\n{\n        \"Start_Timestamp\": \"0.0s\",\n        \"End_Timestamp\": \"3.0s\",\n        \"scene_theme\": \"Calm\",\n        \"characters\": \"None visible\",\n        \"summary\": \"The scene opens to a tranquil setting with instrumental music playing in the background, creating a serene atmosphere amidst the backdrop of an open helicopter landing zone.\",\n        \"actions\": \"Helicopter stationed, no movement observed\",\n        \"key_objects\": \"A white and red helicopter with NEMSYS written on the side, situated in the center of a marked helipad\"\n    }\n]
            
            Movie Description:
            ### Start of description ###
            
            ###DESCRIPTION### 
            
            ### End of description ###
            """

            system_prompt_template = system_prompt_template.replace("###DESCRIPTION###", json.dumps(data))

            message_text = [{"role":"system","content":system_prompt_template}]



            # "give me a scene with an animal, output as timestamp"
            message_text.append({"role":"user","content":question})
            completion = client.chat.completions.create(
            model="gpt-4-turbo", # model = "deployment_name"
            messages = message_text,
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
            )

            st.write("Answer")
            try:
                st.write(json.loads(completion.choices[0].message.content))
            except:
                st.write("Probably the question was not clear enough: ", completion.choices[0].message.content)



with st.expander("Video details"):
    # display the JSON object
    st.write(data)