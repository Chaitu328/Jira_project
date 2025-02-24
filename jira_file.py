import os
import json
from dotenv import load_dotenv
from jira import JIRA
from langchain_groq.chat_models import ChatGroq
import pandas as pd

load_dotenv()

class JiraTestCaseGenerator:
    def __init__(self):
        # Connect to JIRA
        self.jira = self._connect_jira()
        
        # Set up the ChatGroq model
        groq_api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            model_name="mixtral-8x7b-32768",
            temperature=0.7,
            groq_api_key=groq_api_key
        )

    def _connect_jira(self):
        """Connect to the JIRA instance."""
        return JIRA(
            server=os.getenv("JIRA_URL"),
            basic_auth=(os.getenv("JIRA_USER"), os.getenv("JIRA_TOKEN"))
        )

    def get_epic_details(self, epic_key):
        """Fetch the Epic details using its key (e.g., SCRUM-3)."""
        try:
            epic = self.jira.issue(epic_key)
            epic_data = {
                'summary': epic.fields.summary,
                'description': epic.fields.description,
                'acceptance_criteria': getattr(epic.fields, 'customfield_10014', 'None provided')
            }
            return epic_data
        except Exception as e:
            print(f"Error fetching Epic details: {e}")
            return None

    def generate_test_cases(self, epic_data):
        """Generate test cases using the ChatGroq model."""
        prompt = f"""
        Generate test cases for the following Epic in JSON array format:
        Title: {epic_data['summary']}
        Description: {epic_data['description']}
        Acceptance Criteria: {epic_data['acceptance_criteria']}

        Each test case should have:
        - test_case_id (format: TC-001)
        - test_summary
        - test_steps (as numbered list)
        - expected_result

        Return only the JSON array without any additional text or markdown.
        Example:
        [
            {{
                "test_case_id": "TC-001",
                "test_summary": "Verify login functionality",
                "test_steps": "1. Navigate to login page\n2. Enter valid credentials\n3. Click login",
                "expected_result": "User should be logged in successfully"
            }}
        ]
        """

        try:
            response = self.llm.invoke(prompt)
            generated_text = response.content
            
            # Clean the response
            json_str = generated_text.strip().replace('```json', '').replace('```', '')
            
            # Parse JSON
            test_cases = json.loads(json_str)
            return test_cases
            
        except Exception as e:
            print(f"Error generating test cases: {e}")
            print(f"Raw response: {generated_text}")
            return []

    def save_test_cases_to_csv(self, test_cases, filename="test_cases.csv"):
        """Save generated test cases to a CSV file."""
        try:
            # Ensure the test cases have the required fields
            required_fields = ['test_case_id', 'test_summary', 'test_steps', 'expected_result']
            valid_test_cases = []
            
            for tc in test_cases:
                if all(field in tc for field in required_fields):
                    valid_test_cases.append(tc)
                else:
                    print(f"Skipping invalid test case: {tc}")

            if valid_test_cases:
                df = pd.DataFrame(valid_test_cases)
                df.to_csv(filename, index=False)
                print(f"Successfully saved {len(valid_test_cases)} test cases to {filename}")
            else:
                print("No valid test cases to save")
        except Exception as e:
            print(f"Error saving test cases: {e}")

    def create_jira_test_cases(self, test_cases, project_key="SCRUM"):
        """Create test cases in JIRA from generated test cases."""
        created_count = 0
        for tc in test_cases:
            try:
                issue = self.jira.create_issue(
                    project=project_key,
                    summary=f"Test: {tc['test_summary']}",
                    description=f"Steps:\n{tc['test_steps']}\n\nExpected Result:\n{tc['expected_result']}",
                    issuetype={'name': 'Test'}
                )
                print(f"Created Test: {issue.key}")
                created_count += 1
            except Exception as e:
                print(f"Error creating test case: {e}")
        return created_count

if __name__ == "__main__":
    # Initialize the generator
    generator = JiraTestCaseGenerator()
    
    # Specify your Epic key (e.g., "SCRUM-3")
    epic_key = "SCRUM-3"
    
    # Step 1: Fetch Epic details
    epic_data = generator.get_epic_details(epic_key)
    if epic_data:
        print("Epic Details:")
        print(json.dumps(epic_data, indent=2))
        
        # Step 2: Generate test cases using ChatGroq
        test_cases = generator.generate_test_cases(epic_data)
        if test_cases:
            print(f"Generated {len(test_cases)} test cases.")
            
            # Step 3: Save the generated test cases to a CSV file
            generator.save_test_cases_to_csv(test_cases)
            
            # Step 4: Optionally, create the test cases in JIRA
            if input("Do you want to create the test cases in JIRA? (y/n) ").lower() == 'y':
                created_count = generator.create_jira_test_cases(test_cases)
                print(f"Successfully created {created_count}/{len(test_cases)} test cases in JIRA.")
        else:
            print("No test cases generated.")
    else:
        print("Failed to fetch Epic details.")