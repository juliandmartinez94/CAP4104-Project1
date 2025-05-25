import streamlit as st
import pandas as pd
import time
import os

# Create a folder called data in the main project folder
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define CSV file paths for each part of the usability testing
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASK_CSV = os.path.join(DATA_FOLDER, "task_data.csv")
EXIT_CSV = os.path.join(DATA_FOLDER, "exit_data.csv")


def save_to_csv(data_dict, csv_file):
    """Append a new row to a CSV file, creating it if necessary."""
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        df_new.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        df_new.to_csv(csv_file, mode='a', header=False, index=False)


def load_from_csv(csv_file):
    """Load a CSV file into a DataFrame, or return empty DataFrame if it doesn't exist."""
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()


def main():
    st.title("Usability Testing Tool")

    home, consent, demographics, tasks, exit_q, report = st.tabs([
        "Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"
    ])

    with home:
        st.header("Introduction")
        st.write(
            """
            Welcome to the Usability Testing Tool for HCI.

            In this app, you will:
            1. Provide consent for data collection.
            2. Fill out a short demographic questionnaire.
            3. Perform a specific task (or tasks).
            4. Answer an exit questionnaire about your experience.
            5. View a summary report (for demonstration purposes).
            """
        )

    with consent:
        st.header("Consent Form")
        st.write(
            """
            Please read the following terms and consent to participate in this usability test.

            I give consent to the use of the information collected during this Project for the use of the programmers' written report. I understand that my name and personal information will not be released or distributed for commercial use. 
            It will only be for the purposes of this project.
            """
        )
        consent_given = st.checkbox(
            "I have read and agree to the terms of this usability test."
        )
        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("You must agree to the consent terms before proceeding.")
            else:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "consent_given": consent_given
                }
                save_to_csv(data_dict, CONSENT_CSV)
                st.success("Consent submitted. Thank you!")

    with demographics:
        st.header("Demographic Questionnaire")
        with st.form("demographic_form"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            occupation = st.text_input("Occupation")
            familiarity = st.radio(
                "How familiar are you with similar tools?",
                options=[
                    "I've never used these tools",
                    "I'm slightly familiar",
                    "I'm very familiar",
                    "I'm extremely familiar"
                ]
            )
            submitted = st.form_submit_button("Submit Demographics")
            if submitted:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "age": age,
                    "occupation": occupation,
                    "familiarity": familiarity
                }
                save_to_csv(data_dict, DEMOGRAPHIC_CSV)
                st.success("Demographics submitted. Thank you!")

    with tasks:
        st.header("Task Page")
        st.write("Please select a task and record your experience completing it.")

        selected_task = st.selectbox("Select Task", ["Task 1: Example Task"])
        st.write("Task Description: Perform the example task in our system...")

        if st.button("Start Task Timer"):
            st.session_state["start_time"] = time.time()
        if st.button("Stop Task Timer") and "start_time" in st.session_state:
            duration = time.time() - st.session_state["start_time"]
            st.session_state["task_duration"] = duration

        success = st.radio(
            "Was the task completed successfully?", ["Yes", "No", "Partial"]
        )
        notes = st.text_area("Observer Notes")

        if st.button("Save Task Results"):
            duration_val = st.session_state.get("task_duration", None)
            data_dict = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "task_name": selected_task,
                "success": success,
                "duration_seconds": duration_val if duration_val else "",
                "notes": notes
            }
            save_to_csv(data_dict, TASK_CSV)
            st.success("Task data saved.")
            # Clean up session state
            for key in ["start_time", "task_duration"]:
                if key in st.session_state:
                    del st.session_state[key]

    with exit_q:
        st.header("Exit Questionnaire")
        with st.form("exit_form"):
            st.write(
                "Please rate your experience on a scale of 1 to 5:\n"
                "1 = Very unsatisfied\n"
                "2 = Unsatisfied\n"
                "3 = Neutral\n"
                "4 = Satisfied\n"
                "5 = Very satisfied"
            )
            satisfaction = st.slider(
                "Overall, how satisfied were you with the experience?",
                min_value=1, max_value=5, value=3
            )
            st.write(
                "Please rate the task difficulty on a scale of 1 to 5:\n"
                "1 = Very difficult\n"
                "2 = Difficult\n"
                "3 = Neutral\n"
                "4 = Easy\n"
                "5 = Very easy"
            )
            difficulty = st.slider(
                "How difficult was it to complete the task?",
                min_value=1, max_value=5, value=3
            )
            open_feedback = st.text_area("Any additional feedback?")
            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
            if submitted_exit:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "satisfaction": satisfaction,
                    "difficulty": difficulty,
                    "open_feedback": open_feedback
                }
                save_to_csv(data_dict, EXIT_CSV)
                st.success("Exit questionnaire data saved.")

    with report:
        st.header("Usability Report - Aggregated Results")

        st.write("**Consent Data**")
        consent_df = load_from_csv(CONSENT_CSV)
        if not consent_df.empty:
            st.dataframe(consent_df)
        else:
            st.info("No consent data available yet.")

        st.write("**Demographic Data**")
        demographic_df = load_from_csv(DEMOGRAPHIC_CSV)
        if not demographic_df.empty:
            st.dataframe(demographic_df)
        else:
            st.info("No demographic data available yet.")

        st.write("**Task Performance Data**")
        task_df = load_from_csv(TASK_CSV)
        if not task_df.empty:
            st.dataframe(task_df)
        else:
            st.info("No task data available yet.")

        st.write("**Exit Questionnaire Data**")
        exit_df = load_from_csv(EXIT_CSV)
        if not exit_df.empty:
            st.dataframe(exit_df)
        else:
            st.info("No exit questionnaire data available yet.")

        # Example of aggregated stats
        if not exit_df.empty:
            avg_satisfaction = exit_df["satisfaction"].mean()
            avg_difficulty = exit_df["difficulty"].mean()
            st.write(f"**Average Satisfaction (1–5)**: {avg_satisfaction:.2f}")
            st.write(f"**Average Difficulty (1–5)**: {avg_difficulty:.2f}")

if __name__ == "__main__":
    main()