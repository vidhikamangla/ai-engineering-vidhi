from pypdf import PdfReader

PDF_PATH = "data/vidhika_resume_2026.pdf"
CHUNK_SIZE = 500

# reader = PdfReader(PDF_PATH)
# count=0
# for page in reader.pages:
#     count+=1
#     print(page.extract_text() + "\n\n")
# print("Pages:", len(reader.pages), count)
# print(page.extract_text())
# print(page.extract_text(0))

# Step 1: load the PDF and join every page's text into one string
reader = PdfReader(PDF_PATH)
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

print("Pages:", len(reader.pages))
print("Total characters:", len(text))

# Step 2: split into fixed-size chunks
chunks = [text[i : i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]

# Step 3: check the result
print("Chunks:", len(chunks))
print(chunks[0])
print("\n\n")
print(len(chunks[0]))
print("-" * 40)
print(chunks[7])
print("\n\n")
print(len(chunks[7]))
