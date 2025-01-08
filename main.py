from src.resume_analyzer import ResumeAnalysisSystem
from src.llm.llm_config import get_llm


def main():
    llm = get_llm()
    analyzer = ResumeAnalysisSystem(llm)


if __name__ == "__main__":
    print("Henlo")
