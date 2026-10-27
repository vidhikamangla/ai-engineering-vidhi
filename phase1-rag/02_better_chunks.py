from pypdf import PdfReader

PDF_PATH = "data/vidhika_resume_2026.pdf"
CHUNK_SIZE = 500
OVERLAP = 100

# Step 1: load the PDF (same as 01)
reader = PdfReader(PDF_PATH)
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

# Step 2: split into lines, dropping empty ones
lines = [line.strip() for line in text.split("\n") if line.strip()]

# Step 3: pack whole lines into chunks of up to CHUNK_SIZE characters
chunks = []
current = []  # lines in the chunk being built

for line in lines:
    current_len = sum(len(l) + 1 for l in current)  # +1 for the newline between lines
    if current and current_len + len(line) > CHUNK_SIZE:
        chunks.append("\n".join(current))

        # Overlap: start the next chunk with the last few lines of this one
        overlap_lines = []
        overlap_len = 0
        for prev in reversed(current):
            if overlap_len + len(prev) > OVERLAP:
                break
            overlap_lines.insert(0, prev)
            overlap_len += len(prev) + 1
        current = overlap_lines

    current.append(line)

if current:
    chunks.append("\n".join(current))

# Step 4: check the result
print("Lines:", len(lines))
print("Chunks:", len(chunks))
for i, chunk in enumerate(chunks):
    print(f"\n===== chunk {i} ({len(chunk)} chars) =====")
    print(chunk)
