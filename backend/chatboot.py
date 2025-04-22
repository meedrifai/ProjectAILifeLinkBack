import os
from fastapi import APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import gdown
import pickle
import requests
import time

def load_model():
    # Check volume location first
    volume_model_path = "/app/model_data/model.pkl"
    model_path = "model.pkl"
    
    # Use model from volume if it exists
    if os.path.exists(volume_model_path):
        print("Loading model from volume...")
        with open(volume_model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    
    # Fallback to local path
    if os.path.exists(model_path):
        print("Loading model from local path...")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    
    # If model not found locally, download from Google Drive
    print("Model not found locally. Downloading from Google Drive...")
    try:
        # Extract file ID from the Google Drive link
        file_id = "12zlu_C1WA1SFTla4cUG3hDVRpvqoK0dP"
        
        # Download the file using gdown
        gdown.download(f"https://drive.google.com/uc?id={file_id}", model_path, quiet=False)
        
        # Check if download was successful
        if os.path.exists(model_path):
            print("Model downloaded successfully!")
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            return model
        else:
            raise FileNotFoundError("Failed to download model file")
    except Exception as e:
        raise Exception(f"Error downloading model: {str(e)}")

# Get the model when needed
try:
    model = load_model()
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {str(e)}")

intent_responses = {
    "StartConversation": "Welcome! I'm here to answer all your questions about blood donation. Feel free to ask me whatever you're interested in.",
    
    "EndConversation": "Thank you for chatting with me today. Please feel free to come back if you have any other questions about blood donation. Have a great day!",
    
    "DonationPain": "Blood donation generally causes a slight pinch, but it doesn't really hurt. Most donors only feel momentary discomfort when the needle is inserted. After donation, some people may experience a slight bruise or tenderness at the puncture site.",
    
    "AnnualDonationFrequency": "You can donate blood up to 4 times a year for men and 3 times for women. This difference is due to iron reserves, which are naturally higher in men.",
    
    "DonationRequirements": "You must be in good health, aged between 18 and 65, and weigh at least 110 pounds (50 kg). Some situations may require a temporary deferral: recent tattoo (4 months), travel to certain countries, surgical procedures, pregnancy, etc. A medical interview beforehand will determine your eligibility to donate.",
    
    "DrivingAfterDonation": "Yes, you can drive after donating blood, but it's recommended to rest for at least 15 minutes after donation and to hydrate properly. If you feel weak or dizzy, wait until these sensations disappear before getting behind the wheel.",
    
    "PrecautionsBeforeDonation": "Before donating blood, make sure you're well-hydrated, have eaten normally, and are well-rested. Avoid alcohol in the 24 hours preceding donation. Wear comfortable clothing with sleeves that are easy to roll up. Don't forget to bring identification.",
    
    "DonationHours": "Blood donation centers are generally open Monday to Friday from 8am to 7pm and Saturday from 8am to 1pm. Some centers may have extended hours. We recommend checking the exact hours of the center near you on our website or by calling the center directly.",
    
    "EatingBeforeDonation": "It's strongly recommended to eat before donating blood. Don't come on an empty stomach, as this could cause dizziness. Have a light meal and hydrate well (water, fruit juice) in the hours preceding your donation. Avoid overly fatty foods and alcohol.",
    
    "DonationFrequency": "For whole blood donation, you must respect a minimum delay of 8 weeks (56 days) between each donation. For plasma donation, the interval is 2 weeks, and for platelet donation, 4 weeks. These intervals allow your body to replenish its reserves.",
    
    "DonationDuration": "The blood extraction itself takes about 10 minutes. However, the complete process (reception, questionnaire, medical interview, extraction, and rest) takes about 45 minutes to 1 hour for a first visit, and about 30 minutes for regular donors.",
    
    "BloodTests": "After each donation, your blood is systematically analyzed to determine your blood type and Rhesus factor, as well as to detect possible infectious diseases such as Hepatitis B and C, HIV, syphilis, and other viruses. These tests ensure the safety of the recipient.",
    
    "DizzinessAfterDonation": "If you feel unwell after donating blood, lie down immediately with your legs elevated. Alert the medical staff present. Hydrate yourself and eat something sweet. Don't leave the center until you feel completely recovered. If you feel dizzy once you're home, contact the donation center.",
    
    "PregnancyBreastfeedingDonation": "Blood donation is contraindicated during pregnancy and for 6 months after childbirth. For women who are breastfeeding, it's recommended to wait until the end of breastfeeding before donating blood. These precautions aim to protect the health of the mother and child.",
    
    "MedicationsDonation": "Some medications can temporarily prevent blood donation, including recent antibiotics, anticoagulants, certain dermatological treatments like isotretinoin, or prostate medications. Contraceptives, treatments for stabilized hypertension, or antidepressants are generally compatible with donation.",
    
    "BloodDonationProcedure": "The donation process includes: reception and registration, filling out a health questionnaire, a confidential medical interview, blood collection (about 470 ml), and a mandatory snack break for 15-20 minutes. The entire procedure takes about 45 minutes for a first donation.",
    
    "BloodUsage": "The collected blood is used for transfusions during hemorrhages (accidents, surgeries, childbirths), to treat diseases like cancer or anemia, and to manufacture blood-derived medications. All blood types are needed, but O negative (universal donor) and A positive groups are particularly in demand.",
    
    "DonationLocation": "You can make an appointment for blood donation online on our website, via our mobile app, by phone, or directly at the donation center. Although appointments are recommended to reduce your waiting time, many centers also accept donors without appointments.",
    
    "ExerciseAfterDonation": "It's advised against practicing intense physical activity within 24 hours following a blood donation. Particularly avoid swimming, cycling, intensive running, or heavy weightlifting. These precautions allow your body to recover and avoid dizziness or discomfort related to the temporary decrease in blood volume."
}
# Définir l'app FastAPI
router = APIRouter()


# Modèle d'entrée
class MessageInput(BaseModel):
    message: str

@router.post("/chatboot")
async def chatboot(data: MessageInput):
    question = data.message
    intent = model.predict([question])[0]
    response = intent_responses.get(intent, "Je n'ai pas compris, réessayez.")
    return {
        "intent": intent,
        "response": response
    }
