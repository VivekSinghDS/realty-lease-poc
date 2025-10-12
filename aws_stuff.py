import boto3

def extract_paragraphs_from_pdf(pdf_path):
    textract = boto3.client("textract", region_name = "us-east-1")

    # Read file bytes
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # Analyze document with layout to get paragraph blocks
    response = textract.analyze_document(
        Document={"Bytes": pdf_bytes},
        FeatureTypes=["LAYOUT"]
    )

    # Extract paragraph blocks
    paragraphs = []
    for block in response["Blocks"]:
        if block["BlockType"] == "PARAGRAPH":
            paragraphs.append(block["Text"])

    # Number and print them
    for i, paragraph in enumerate(paragraphs, start=1):
        print(f"Paragraph {i}:\n{paragraph}\n{'-'*60}")

    return paragraphs


if __name__ == "__main__":
    pdf_file = "/Users/vivek.singh/realty-poc/data/Bayer 2015-10-05 Lease.pdf"  # <-- your PDF file
    extract_paragraphs_from_pdf(pdf_file)
