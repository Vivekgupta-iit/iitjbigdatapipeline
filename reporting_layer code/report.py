from nbconvert import PDFExporter
from nbformat import read
from google.cloud import storage

# Create a client object for the GCS bucket
client = storage.Client()

# Get a reference to the PySpark notebook file
bucket = client.get_bucket("iitj_bigdataproject_pgd_dev")
blob = bucket.blob("Script/report.ipynb")

# Download the PySpark notebook to a local file
blob.download_to_filename("/tmp/report.ipynb")

# Read the PySpark notebook
with open("/tmp/report.ipynb") as f:
    nb = read(f, as_version=4)

# Create a PDF exporter
pdf_exporter = PDFExporter()

# Define the export options
pdf_exporter.exclude_input_prompt = True
pdf_exporter.exclude_output_prompt = True
pdf_exporter.verbose = False


# Generate the PDF report
(body, resources) = pdf_exporter.from_notebook_node(nb)

# Upload the PDF report to the GCS bucket
blob = bucket.blob("Script/report.pdf")
blob.upload_from_string(body)

print("PDF report generated successfully")
