from django.shortcuts import render
from django.http import JsonResponse
import PyPDF2
import re
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key='AIzaSyDirsa-ppbHV5eDkAysC9JVExlvmFHD534')
model = genai.GenerativeModel(model_name='gemini-pro')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to clean text
def clean_text(text):
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
    cleaned_text = cleaned_text.lower()
    cleaned_text = ' '.join(cleaned_text.split())
    return cleaned_text

# Extract and clean text from PDF files (example paths)
pdf_files = [
    "D:/try3 - Copy/chatbot_project/chat/templates/chat/Employee Manuals.pdf",
    "D:/try3 - Copy/chatbot_project/chat/templates/chat/FAQ.pdf",
    "D:/try3 - Copy/chatbot_project/chat/templates/chat/HRPolicy.pdf"
]
all_cleaned_text = ""

for pdf_file in pdf_files:
    raw_text = extract_text_from_pdf(pdf_file)
    cleaned_text = clean_text(raw_text)
    all_cleaned_text += cleaned_text + " "

all_cleaned_text = all_cleaned_text.strip()

# Function to get response from Generative AI
def get_response(question):
    response = model.generate_content(f"{all_cleaned_text}\n\n{question}")
    return response.text.strip()

# HR policies dictionary
HR_Policies = {
    "Employee Code of Conduct": {
        "Introduction": [
            "1. Purpose: This Employee Code of Conduct outlines the standards of behavior expected of employees at MarkAtlas Inkjet Technologies. It guides interactions within the workplace, with clients, and in the broader community.",
            "2. Scope: This code applies to all employees, contractors, and volunteers. Compliance is a condition of employment."
        ],
        "Professional Behavior": [
            "1. Respect and Courtesy: Employees must treat each other, clients, and stakeholders with respect and courtesy. Discriminatory, harassing, or bullying behavior is prohibited.",
            "2. Integrity: Employees must act honestly and ethically in all business dealings and professional relationships.",
            "3. Confidentiality: Employees must safeguard company confidential information and not disclose it to unauthorized persons. This includes protecting personal data of clients and colleagues.",
        ],
        "Work Performance": [
            "1. Accountability: Employees are responsible for their actions and must perform their duties to the best of their ability, following company policies.",
            "2. Punctuality: Employees must arrive at work on time. Absenteeism and tardiness without valid reasons may result in disciplinary action.",
            "3. Professional Development: Employees are encouraged to pursue professional development to enhance skills. The company provides training programs and resources."
        ],
        "Conflict of Interest": [
            "1. Definition: A conflict of interest arises when personal interests interfere with professional duties.",
            "2. Disclosure: Employees must disclose conflicts of interest to supervisors or HR. Failure to disclose may result in disciplinary action.",
            "3. Management: The company will manage conflicts of interest to prevent negative impacts."
        ],
        "Use of Company Resources": [
            "1. Proper Use: Employees must use company resources responsibly and for work-related purposes only.",
            "2. Intellectual Property: Respect the company's and others' intellectual property rights. Unauthorized use is prohibited.",
            "3. IT Security: Follow IT policies, use strong passwords, secure devices, and report security incidents promptly."
        ],
        "Health and Safety": [
            "1. Workplace Safety: Maintain a safe environment, follow safety protocols, report hazards, and participate in safety training.",
            "2. Substance Abuse: Prohibit illegal drugs or misuse of alcohol/prescriptions. Employees must be fit for duty.",
            "3. Wellness Programs: Access wellness programs to support physical and mental health."
        ],
        "Reporting Violations": [
            "1. Procedure: Report violations to supervisors, HR, or through the anonymous reporting system.",
            "2. Non-Retaliation: The company prohibits retaliation against good-faith reporters.",
            "3. Investigation: Prompt investigation of violations, followed by appropriate action."
        ],
        "Disciplinary Actions": [
            "1. Grounds: Disciplinary action for code violations or conduct detrimental to the company.",
            "2. Process: Actions may include warnings, suspension, or termination, depending on severity.",
            "3. Appeal: Employees may appeal disciplinary actions in writing to HR."
        ],
        "Review and Amendments": [
            "1. Review: Periodic review to ensure relevance and effectiveness, with updates communicated to employees.",
            "2. Amendments: The company reserves the right to amend the code; compliance with current versions is expected."
        ],
        "Acknowledgment": [
            "Acknowledgment: Employees acknowledge receipt and understanding of the code by signing an acknowledgment form."
        ]
    },
    "HR Policy on Remote Work": {
        "Introduction": [
            "1. Purpose: This policy provides guidelines for approved remote work arrangements to benefit employees and the company.",
            "2. Scope: Applies to employees granted remote work privileges, full-time or part-time."
        ],
        "Eligibility and Approval": [
            "1. Eligibility: Based on performance and job responsibilities.",
            "2. Approval: Submit request for review by supervisor and HR. New arrangements may have a trial period."
        ],
        "Remote Work Environment": [
            "1. Home Office: Set up a productive, safe workspace with reliable internet and necessary equipment.",
            "2. Equipment and Supplies: Company-provided resources are for work purposes.",
            "3. IT Support: Access company IT support for technical issues and follow security protocols."
        ],
        "Work Hours and Availability": [
            "1. Work Schedule: Adhere to agreed-upon hours and be available during core business times.",
            "2.  Communication: Maintain regular contact with team via company tools, attend meetings, and update progress.",
            "3. Time Tracking: Use company systems for accurate hours, with overtime approved in advance."
        ],
        "Performance and Accountability": [
            "1. Expectations: Meet standards for quality, deadlines, and goals.",
            "2. Accountability: Demonstrate responsiveness, timely completion of tasks, and productivity.",
            "3. Feedback: Regular supervisor feedback supports remote success."
        ],
        "Security and Confidentiality": [
            "1. Data Security: Follow company policies for data protection, including secure networks and reporting breaches.",
            "2. Confidentiality: Safeguard company information, physical or digital."
        ],
        "Health and Well-Being": [
            "1. Ergonomics: Set up ergonomic workspace to prevent injury.",
            "2. Balance: Maintain work-life balance, manage stress.",
            "3. Wellness Programs: Access company wellness resources."
        ],
        "Termination of Remote Work Arrangement": [
            "1. By Employee: Request to return to office reviewed based on needs.",
            "2. By Company: Termination based on performance, job changes, or operational needs.",
            "3. Transition: Plan provided for office return or adjustments."
        ],
        "Review and Amendments": [
            "1. Review: Regular policy review for relevance.",
            "2. Amendments: Updates communicated to employees."
        ],
        "Acknowledgment": [
            "Acknowledgment: Employees acknowledge receipt and understanding by signing."
        ]
    }
}

def index(request):
    return render(request, 'chat/index.html')

def chatbot_response(request):
    if request.method == "POST":
        user_input = request.POST.get('message')
        response = {}

        if not user_input:
            response = {
                'response': 'Welcome! What would you like to choose?',
                'options': [
                    {'text': 'HR Policies', 'value': 'View HR Policies'},
                    {'text': 'HR Queries', 'value': 'HR Queries'},
                ]
            }
        elif user_input.lower() == "view hr policies":
            response = {
                'response': 'Please select a policy:',
                'options': [
                    {'text': 'Code of Conduct', 'value': 'Code of Conduct'},
                    {'text': 'Remote Work', 'value': 'Remote Work'},
                    {'text': 'Main Menu', 'value': 'Main Menu'},
                ]
            }
        elif user_input.lower() == "main menu":
            response = {
                'response': 'What would you like to choose?',
                'options': [
                    {'text': 'HR Policies', 'value': 'View HR Policies'},
                    {'text': 'HR Queries', 'value': 'HR Queries'},
                ]
            }
        elif user_input.lower() == "code of conduct":
            response = {
                'response': 'Please select a section of the Code of Conduct:',
                'options': [
                    {'text': 'Introduction', 'value': 'Introduction'},
                    {'text': 'Professional Behavior', 'value': 'Professional Behavior'},
                    {'text': 'Work Performance', 'value': 'Work Performance'},
                    {'text': 'Conflict of Interest', 'value': 'Conflict of Interest'},
                    {'text': 'Use of Company Resources', 'value': 'Use of Company Resources'},
                    {'text': 'Health and Safety', 'value': 'Health and Safety'},
                    {'text': 'Reporting Violations', 'value': 'Reporting Violations'},
                    {'text': 'Disciplinary Actions', 'value': 'Disciplinary Actions'},
                    {'text': 'Review and Amendments', 'value': 'Review and Amendments'},
                    {'text': 'Acknowledgment', 'value': 'Acknowledgment'},
                ]
            }
        elif user_input.lower() == "remote work":
            response = {
                'response': 'Please select a section of the Remote Work policy:',
                'options': [
                    {'text': 'Introduction', 'value': 'Introduction'},
                    {'text': 'Eligibility and Approval', 'value': 'Eligibility and Approval'},
                    {'text': 'Remote Work Environment', 'value': 'Remote Work Environment'},
                    {'text': 'Work Hours and Availability', 'value': 'Work Hours and Availability'},
                    {'text': 'Performance and Accountability', 'value': 'Performance and Accountability'},
                    {'text': 'Security and Confidentiality', 'value': 'Security and Confidentiality'},
                    {'text': 'Health and Well-Being', 'value': 'Health and Well-Being'},
                    {'text': 'Termination of Remote Work Arrangement', 'value': 'Termination of Remote Work Arrangement'},
                    {'text': 'Review and Amendments', 'value': 'Review and Amendments'},
                    {'text': 'Acknowledgment', 'value': 'Acknowledgment'},
                ]
            }
        elif user_input.lower() == "hr queries":
            response = {
                'response': 'Please type your query:',
                'options': []
            }
        elif any(user_input.lower() in sub_section.lower() for sub_section in HR_Policies["Employee Code of Conduct"]):
            policy_section = HR_Policies["Employee Code of Conduct"][user_input]
            response = {
                'response': "\n".join(policy_section),
                'options': [
                    {'text': 'Code of Conduct', 'value': 'Code of Conduct'},
                    {'text': 'Remote Work', 'value': 'Remote Work'},
                    {'text': 'Main Menu', 'value': 'Main Menu'},
                ]
            }
        elif any(user_input.lower() in sub_section.lower() for sub_section in HR_Policies["HR Policy on Remote Work"]):
            policy_section = HR_Policies["HR Policy on Remote Work"][user_input]
            response = {
                'response': "\n".join(policy_section),
                'options': [
                    {'text': 'Code of Conduct', 'value': 'Code of Conduct'},
                    {'text': 'Remote Work', 'value': 'Remote Work'},
                    {'text': 'Main Menu', 'value': 'Main Menu'},
                ]
            }
        else:
            response_text = get_response(user_input)
            response = {
                'response': response_text,
                'options': [
                    {'text': 'HR Policies', 'value': 'View HR Policies'},
                    {'text': 'HR Queries', 'value': 'HR Queries'},
                ]
            }

        return JsonResponse(response)
    return JsonResponse({'response': 'Invalid request method.'})