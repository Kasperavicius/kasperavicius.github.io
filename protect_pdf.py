from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
import io
import os

# ✏️ Change these two lines
password = "YourPasswordHere"
message = "Please contact me to obtain the password for access."

# Get the folder where this script is located
folder = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(folder, "unprotected.pdf")
output_path = os.path.join(folder, "resume.pdf")

# Create the message page
buffer = io.BytesIO()
c = canvas.Canvas(buffer, pagesize=letter)
width, height = letter
c.setFont("Helvetica-Bold", 14)
c.drawCentredString(width/2, height/2 + 20, "This document is password-protected.")
c.setFont("Helvetica", 12)
c.drawCentredString(width/2, height/2 - 10, message)
c.save()

# Combine message page + original PDF
buffer.seek(0)
message_page = PdfReader(buffer).pages[0]

writer = PdfWriter()
writer.add_page(message_page)  # message goes first

original = PdfReader(input_path)
for page in original.pages:
    writer.add_page(page)

# Encrypt and save
writer.encrypt(password)
with open(output_path, "wb") as f:
    writer.write(f)

print(f"Done! Saved as: {output_path}")