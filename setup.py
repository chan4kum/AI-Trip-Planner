from pathlib import Path
from setuptools import find_packages, setup
from typing import List


def get_requirements() -> List[str]:
    """Load requirements.txt, skipping editable/local directives."""

    requirement_list: List[str] = []
    try:
       with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:

                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("The requirements.txt file was not found.")
    return requirement_list

print(get_requirements())

setup(
    name="AI-Travel-PLANNER",
    version="0.1.0",
    author="Chandan Kumar",
    author_email="ckumar13@deloitte.com",
    description="AI Travel Planner using LangChain and LLMs",
    packages=find_packages(),
    install_requires=get_requirements(),
)
