# This file will be responsible
# for creating a package on PyPI
# out of this ml project
from setuptools import setup,find_packages

HYPHEN_E_DOT="-e ."

def get_requirements(req_file_path:str)->list[str]:
    """
    this method returns a list of requirements
    """
    requirements=[]
    with open(req_file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
    if HYPHEN_E_DOT in requirements:
        requirements.remove(HYPHEN_E_DOT)
    return requirements

# metadata about the project
setup(
    name="e2e_mlproject_1",
    author="Ipsita",
    version="0.0.1",
    packages=find_packages(),#list of packages in this project
    install_requires=get_requirements("requirements.txt")
)