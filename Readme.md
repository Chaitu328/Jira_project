# Workflow

+----------------------------+            +-------------------------+
|   1. Fetch Epic Details     |            |   2. Feed to Generative  |
|   (JIRA API)                |------------|   AI Model (ChatGroq)    |
|                            |            |                         |
| - Pull Epic Summary         |            | - Generate Test Cases    |
| - Pull Description          |            |                         |
| - Pull Acceptance Criteria  |            |                         |
+----------------------------+            +-------------------------+
               |                                  |
               v                                  v
+----------------------------+            +-------------------------+
|   3. Generate Test Cases    |            | 4. Save/Export to CSV    |
|   (Using Generative AI)     |            |                         |
| - AI generates test cases   |------------| - Save generated test    |
|   based on the inputs       |            |   cases to CSV or Excel  |
+----------------------------+            +-------------------------+
               |                                  |
               v                                  v
+----------------------------+            +-------------------------+
|   5. Create in JIRA         |            |   6. Review Test Cases   |
|   (JIRA API)                |------------|   (Optional)             |
| - Create Test Cases as      |            |                         |
|   Jira Issues               |            | - Review and Confirm     |
+----------------------------+            +-------------------------+
