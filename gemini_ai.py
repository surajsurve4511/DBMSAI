# gemini_ai.py
# Google Gemini AI Integration for Advanced Medical Insights

import google.generativeai as genai
from config import Config
import json
from database import Database

class GeminiAI:
    """Advanced AI features using Google Gemini"""
    
    def __init__(self):
        """Initialize Gemini AI"""
        try:
            if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != 'YOUR_GEMINI_API_KEY_HERE':
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
                self.enabled = True
            else:
                self.enabled = False
                print("⚠️  Gemini AI not configured. Using basic AI features only.")
        except Exception as e:
            self.enabled = False
            print(f"⚠️  Gemini AI initialization failed: {e}")
    
    def generate_patient_insights(self, patient_data, medical_history):
        """Generate comprehensive patient insights using Gemini"""
        if not self.enabled:
            return self._basic_insights(patient_data, medical_history)
        
        try:
            # Prepare context
            context = f"""
            You are a medical AI assistant. Analyze this patient data and provide insights.
            
            Patient Information:
            - Name: {patient_data.get('name')}
            - Age: {patient_data.get('age')}
            - Gender: {patient_data.get('gender')}
            
            Medical History:
            {self._format_history(medical_history)}
            
            Provide a brief analysis including:
            1. Health risk factors
            2. Preventive care recommendations
            3. Lifestyle suggestions
            
            Keep response concise (3-4 sentences).
            """
            
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            print(f"Gemini AI error: {e}")
            return self._basic_insights(patient_data, medical_history)
    
    def generate_treatment_plan(self, diagnosis, patient_age, medical_history):
        """Generate detailed treatment plan using Gemini"""
        if not self.enabled:
            return self._basic_treatment(diagnosis)
        
        try:
            context = f"""
            As a medical AI, suggest a treatment plan for:
            
            Diagnosis: {diagnosis}
            Patient Age: {patient_age}
            Previous Conditions: {', '.join([h.get('disease', '') for h in medical_history[:3]])}
            
            Provide:
            1. Primary treatment approach
            2. Medications (generic names)
            3. Lifestyle modifications
            4. Follow-up schedule
            
            Format as numbered list. Keep concise.
            """
            
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            print(f"Gemini AI error: {e}")
            return self._basic_treatment(diagnosis)
    
    def analyze_symptoms(self, symptoms):
        """Analyze symptoms and suggest possible conditions"""
        if not self.enabled:
            return "Please consult a healthcare professional for accurate diagnosis."
        
        try:
            context = f"""
            As a medical AI assistant, analyze these symptoms and suggest possible conditions:
            
            Symptoms: {symptoms}
            
            Provide:
            1. Most likely conditions (3-4)
            2. Urgency level (Low/Medium/High)
            3. Recommended next steps
            
            Note: This is for informational purposes only. Always consult a doctor.
            Keep response brief and clear.
            """
            
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            return "Error analyzing symptoms. Please consult a healthcare professional."
    
    def predict_complications(self, current_diagnosis, age, history):
        """Predict potential complications"""
        if not self.enabled:
            return ["Monitor vital signs regularly", "Follow prescribed treatment", "Regular check-ups recommended"]
        
        try:
            context = f"""
            Medical AI: Predict potential complications for:
            
            Current Diagnosis: {current_diagnosis}
            Patient Age: {age}
            Medical History: {', '.join([h.get('disease', '') for h in history[:3]])}
            
            List 3-5 potential complications to watch for.
            Format as bullet points. Be specific but concise.
            """
            
            response = self.model.generate_content(context)
            # Parse response into list
            complications = [line.strip('- •').strip() for line in response.text.split('\n') if line.strip()]
            return complications[:5]  # Limit to 5
        except Exception as e:
            return ["Monitor for any unusual symptoms", "Maintain prescribed medication schedule", "Regular vital sign checks"]
    
    def generate_discharge_summary(self, patient_data, admission_data):
        """Generate discharge summary"""
        if not self.enabled:
            return self._basic_discharge_summary(admission_data)
        
        try:
            context = f"""
            Generate a discharge summary for:
            
            Patient: {patient_data.get('name')}, {patient_data.get('age')} years
            Diagnosis: {admission_data.get('diagnosis')}
            Treatment Given: {admission_data.get('treatment')}
            Admission Date: {admission_data.get('in_date_time')}
            
            Include:
            1. Brief hospitalization summary
            2. Discharge instructions
            3. Medications to continue
            4. Follow-up schedule
            
            Professional medical format. Concise.
            """
            
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            return self._basic_discharge_summary(admission_data)
    
    def analyze_hospital_trends(self, disease_data):
        """Analyze hospital disease trends"""
        if not self.enabled:
            return "Disease trend analysis requires AI configuration."
        
        try:
            diseases_str = ', '.join([f"{d['disease']} ({d['frequency']})" for d in disease_data[:5]])
            
            context = f"""
            Analyze these hospital disease trends:
            
            {diseases_str}
            
            Provide:
            1. Pattern insights
            2. Seasonal considerations
            3. Resource planning suggestions
            
            Keep response brief (3-4 sentences).
            """
            
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            return "Unable to analyze trends at this time."
    
    def generate_health_tips(self, age, gender, conditions):
        """Generate personalized health tips"""
        if not self.enabled:
            return ["Maintain a balanced diet", "Exercise regularly", "Get adequate sleep", "Stay hydrated"]
        
        try:
            context = f"""
            Provide 5 personalized health tips for:
            
            Age: {age}
            Gender: {gender}
            Conditions: {', '.join(conditions[:3])}
            
            Format as bullet points. Practical and specific advice.
            """
            
            response = self.model.generate_content(context)
            tips = [line.strip('- •').strip() for line in response.text.split('\n') if line.strip()]
            return tips[:5]
        except Exception as e:
            return ["Maintain healthy lifestyle", "Regular medical check-ups", "Balanced diet", "Adequate rest"]
    
    # Helper methods for fallback
    def _format_history(self, history):
        """Format medical history for context"""
        if not history:
            return "No previous medical history"
        return '\n'.join([f"- {h.get('disease')}: {h.get('treatment')}" for h in history[:5]])
    
    def _basic_insights(self, patient_data, medical_history):
        """Basic insights without AI"""
        age = patient_data.get('age', 0)
        history_count = len(medical_history)
        
        if age > 60 and history_count > 3:
            return "Patient requires regular monitoring due to age and medical history. Focus on preventive care and lifestyle management."
        elif history_count > 5:
            return "Multiple medical conditions require coordinated care approach. Regular follow-ups recommended."
        else:
            return "Maintain healthy lifestyle and regular check-ups. Follow prescribed treatment plans."
    
    def _basic_treatment(self, diagnosis):
        """Basic treatment suggestion"""
        return f"Recommended treatment for {diagnosis}:\n1. Appropriate medication as prescribed\n2. Rest and proper nutrition\n3. Follow-up in 7-10 days\n4. Monitor for any complications"
    
    def _basic_discharge_summary(self, admission_data):
        """Basic discharge summary"""
        return f"""Discharge Summary:
        
Patient was treated for {admission_data.get('diagnosis')}.
Treatment provided: {admission_data.get('treatment')}

Discharge Instructions:
1. Continue prescribed medications
2. Follow-up appointment in 1 week
3. Rest and proper nutrition
4. Contact hospital if symptoms worsen
"""

# Initialize global instance
gemini_ai = GeminiAI()
