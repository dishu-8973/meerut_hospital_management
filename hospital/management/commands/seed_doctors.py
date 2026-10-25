from django.core.management.base import BaseCommand

from hospital.models import Doctor

# Sample (kaalpanik) doctors -- demo ke liye. Asli doctors admin panel se add karo.
SAMPLE_DOCTORS = [
    {
        "name": "Dr. Anil Verma",
        "specialization": "Cardiology",
        "experience": 18,
        "description": "Heart ke rogon, BP aur preventive cardiac care mein visheshagya.",
    },
    {
        "name": "Dr. Sunita Sharma",
        "specialization": "Gynaecology",
        "experience": 14,
        "description": "Pregnancy care, women's health aur safe delivery mein anubhavi.",
    },
    {
        "name": "Dr. Rajesh Tyagi",
        "specialization": "Orthopedics",
        "experience": 12,
        "description": "Joint pain, fracture care aur sports injuries ka upchar.",
    },
    {
        "name": "Dr. Neha Gupta",
        "specialization": "Pediatrics",
        "experience": 9,
        "description": "Bachchon ki sehat, vaccination aur growth monitoring.",
    },
    {
        "name": "Dr. Vikas Malik",
        "specialization": "Neurology",
        "experience": 16,
        "description": "Migraine, epilepsy aur nervous system ke vikaron ka ilaaj.",
    },
    {
        "name": "Dr. Pooja Singh",
        "specialization": "Dermatology",
        "experience": 8,
        "description": "Skin, hair aur allergy se judi samasyaon ka upchar.",
    },
]


class Command(BaseCommand):
    help = "Demo ke liye kuch sample doctors database mein add karta hai."

    def handle(self, *args, **options):
        created = 0
        for data in SAMPLE_DOCTORS:
            _, was_created = Doctor.objects.get_or_create(
                name=data["name"],
                defaults={
                    "specialization": data["specialization"],
                    "experience": data["experience"],
                    "description": data["description"],
                    "available": True,
                },
            )
            created += int(was_created)
        self.stdout.write(
            self.style.SUCCESS(
                f"{created} naye doctors add hue ({len(SAMPLE_DOCTORS) - created} pehle se the)."
            )
        )
