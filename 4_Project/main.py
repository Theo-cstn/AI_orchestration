from crew import PartnershipCrew
from dotenv import load_dotenv

load_dotenv()

def run():
    # Un exemple de mail à tester
    inputs = {
        'email_content': "Bonjour, je suis un bot qui veut vous vendre des chaussures pas chères."
    }
    PartnershipCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()