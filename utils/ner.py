import re
import spacy
from utils.keyword import sector_keywords,general_skills,degrees
import os
import csv


nlp = spacy.load("en_core_web_sm")

def extract_name(text):
    try :
        doc = nlp(text)
        for entity in doc.ents:
            if entity.label_ == "PERSON":
                return entity.text.strip()
        return "Name not found"
    except Exception as e:
        return f"error occured in extract name function {e}"
def extract_email(text):
    try:
        match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        return match.group(0) if match else "Email not found"
    except Exception as e:
        return f"error occured in extract_email function {e}"  
def extract_phone(text):
    try:
        match = re.search(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}", text)
        return match.group(0) if match else "Phone number not found"
    except Exception as e:
        return f"error occured in extract_phone function {e}"
def extract_skills(text, sector):
    try:
        
        sector_skills = sector_keywords.get(sector.upper(), [])
        all_skills = general_skills + sector_skills
        found_skills = [skill for skill in all_skills if skill.lower() in text.lower()]
        return found_skills if found_skills else ["No skills found"]
    except Exception as e:
        return f"error occured in extract_skill function {e}"
def extract_experience(text):
    try:
        match = re.search(r"(\d+)\+?\s*years? of experience", text, re.IGNORECASE)
        return match.group(0) if match else "Experience not found"
    except  Exception as e:
        return f"error occured in extract experience function {e}"
def extract_education(text, degrees):
    try:
        # Convert text to lowercase for matching
        text = text.lower()
        # Convert all degrees to lowercase for consistency
        lower_degrees = [degree.lower() for degree in degrees]
        
        # Extract all words (including multi-word degrees like B. Tech, M. Sc)
        words = re.findall(r'\b\w+(?:\.\w+|\w+)*\b', text)
        
        found_degrees = []
        for word in set(words):
            if word in lower_degrees:
                # Preserve the original case for the extracted degree
                original_degree = degrees[lower_degrees.index(word)]
                found_degrees.append(original_degree)

        return found_degrees if found_degrees else ["No education found"]

    except Exception as e:
        return f"Error occurred in extract_education function: {e}"
def extract_links(text):
    try:
        # Normalize text to lowercase for better matching
        text = text.lower()

        # Pattern for LinkedIn links
        linkedin_pattern = r"(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9-]+"
        # Pattern for GitHub links
        github_pattern = r"(https?://)?(www\.)?github\.com/[a-zA-Z0-9-]+"
        
        # Extract LinkedIn and GitHub links
        linkedin_link = re.search(linkedin_pattern, text)
        github_link = re.search(github_pattern, text)
        
        # Extract links or return "not found" message
        linkedin = linkedin_link.group(0) if linkedin_link else "LinkedIn not found"
        github = github_link.group(0) if github_link else "GitHub not found"
        
        # Ensure the links have a complete URL format
        if linkedin != "LinkedIn not found" and not linkedin.startswith("http"):
            linkedin = "https://" + linkedin
        if github != "GitHub not found" and not github.startswith("http"):
            github = "https://" + github
        
        return {"LinkedIn": linkedin, "GitHub": github}

    except Exception as e:
        return f"Error occurred in extract_links function: {e}"
def extract_resume_info(text, sector):
    try:
        
        links = extract_links(text)
        return {
            "Name": extract_name(text),
            "Email": extract_email(text),
            "Phone": extract_phone(text),
            "Skills": extract_skills(text, sector),
            "Experience": extract_experience(text),
            "Education": extract_education(text,degrees),
            "Sector": sector,
            "LinkedIn": links["LinkedIn"],
            "GitHub": links["GitHub"]
        }
    except Exception as e:
        return f"error occured in extract_resume_info function in ner.py file {e}"


OUTPUT_CSV = "extracted_resume_details.csv"
headers = ["Name", "Education", "Experience", "Phone Number", "Email", "Skills", "Sector", "LinkedIn", "GitHub"]

def save_to_csv(text, sector):
    data_dict = extract_resume_info(text, sector)  # returns dict

    # Check if file exists to decide write mode and header
    file_exists = os.path.isfile(OUTPUT_CSV)

    with open(OUTPUT_CSV, mode="a" if file_exists else "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header only if file is new
        if not file_exists:
            writer.writerow(headers)

        # Prepare row in same order as headers
        row = [data_dict.get(header, "") for header in headers]
        writer.writerow(row)

    print(f"Resume details saved to {OUTPUT_CSV}")