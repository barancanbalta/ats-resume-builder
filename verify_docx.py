from cv_generator_docx import ATSResumeDocx
from user_data import user_profile
import os

print("Testing DOCX Generator...")
try:
    docx = ATSResumeDocx()
    docx.generate(user_profile)
    
    filename = "test_ats_resume.docx"
    docx.save(filename)
    
    size = os.path.getsize(filename)
    print(f"SUCCESS: DOCX generated. Size: {size} bytes")
    
    # Optional: Check if we can open it again (basic integrity check)
    from docx import Document
    doc = Document(filename)
    print(f"SUCCESS: DOCX is readable. Paragraphs: {len(doc.paragraphs)}")
    
    # Check for metadata
    core_props = doc.core_properties
    print(f"Metadata Title: {core_props.title}")
    print(f"Metadata Keywords: {core_props.keywords}")

except Exception as e:
    print(f"FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

# Debug Metadata directly on the object used for generation
print(f"Direct Check - Title: {docx.doc.core_properties.title}")
print(f"Direct Check - Keywords: {docx.doc.core_properties.keywords}")
