# Jira Test Case Generator Workflow

## 1. User Input Section:
- **Epic Key Input**: 
  - A field where the user enters the Epic key (e.g., `SCRUM-3`).
- **Fetch Epic Details**: 
  - A button to fetch details from the Epic, which will return:
    - **Epic Title**: The name of the Epic.
    - **Epic Description**: The detailed description of the Epic.
    - **Acceptance Criteria**: The criteria for acceptance (fetched or displayed).

---

## 2. Generate Test Cases Section:
- **Generate Button**:
  - Once the Epic details are fetched, the user clicks a button to generate test cases.
  - The system calls the `generate_test_cases()` method to process and generate the test cases.
  - A **progress bar** or **spinner** indicates the generation process.
  - Display a summary of the generated test cases in a **table**:
    - **Test Case ID** (e.g., `TC-001`)
    - **Test Summary**
    - **Test Steps**
    - **Expected Result**
  - Optionally, the user can review and modify the test cases.

---

## 3. Save Test Cases Section:
- **Save to CSV Button**:
  - Allow the user to save the generated test cases as a CSV file.
  - A file picker or an automatic download link is provided after saving.

---

## 4. Create JIRA Test Cases Section:
- **Create in JIRA Button**:
  - After reviewing the generated test cases, the user clicks to create the test cases directly in JIRA.
  - Display a confirmation prompt: "Do you want to create the test cases in JIRA?"
  - If confirmed, the backend uses the `create_jira_test_cases()` method to push the test cases to JIRA.
  - Display a **success message** like: "Successfully created X test cases in JIRA."
  - In case of an error, display an **error message** such as: "Error creating test cases in JIRA."

---

## 5. Dashboard UI/UX Considerations:
- **Progress Feedback**:
  - Show feedback during operations like fetching Epic details, generating test cases, and creating test cases in JIRA (e.g., loading indicators).
- **Filter & Search**:
  - Add functionality to search or filter generated test cases or Jira tickets.
- **Export Options**:
  - Besides saving to CSV, allow exporting to **Excel** or **JSON** formats.
- **Dynamic Updates**:
  - Display the test case generation status in real-time, allowing users to interact with generated cases (edit, delete, mark as complete).

---

## 6. Dashboard Workflow Overview:

1. **Epic Selection (User Input)**:
   - User inputs the Epic key and clicks **Fetch Epic Details**.
   
2. **Fetch Epic Details (System Operation)**:
   - Backend fetches data from Jira.
   - Display Epic data like **Title**, **Description**, and **Acceptance Criteria**.

3. **Test Case Generation (User Action)**:
   - User clicks **Generate Test Cases**.
   - The system calls the `generate_test_cases()` method to process and return a list of test cases.

4. **Test Case Review (System/UX)**:
   - Generated test cases are displayed in a table.
   - User can review and edit test cases if needed.

5. **Saving/Exporting (User Action)**:
   - User clicks **Save to CSV** or **Export to Excel/JSON** to download the test cases.

6. **Create Test Cases in JIRA (User Action)**:
   - User clicks **Create in JIRA** to push the test cases to Jira.
   - System handles the creation and provides feedback (success or failure).
