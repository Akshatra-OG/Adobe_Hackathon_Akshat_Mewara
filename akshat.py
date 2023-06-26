# due to the version control issue and so of the rest_api site maybe due to traffic or something i was not able to access the link so went out with a whole diff. approach of ReGEX

import os
import csv
import re
import pdfplumber

# Set the path to the folder containing the PDF invoices
invoices_folder = "/InvoicesData/TestDataSet"

# Set the path to save the extracted data in CSV format
output_csv_path = "/InvoicesData/sampleInvoicesAndData/file.csv"

# Define the regular expressions for pattern matching
invoice_number_regex = r"Invoice#\s*([\w\d]+)"
issue_date_regex = r"Issue date\s*([\d-]+)"
business_name_regex = r"([\w\s]+)\nWe are here"
business_address_regex = r"(\d+ [\w\s,.]+), ([\w\s]+), ([\w\s]+)"
customer_name_regex = r"BILL TO\n([\w\s]+)"
customer_email_regex = r"([\w.-]+@[\w.-]+)"
customer_phone_regex = r"(\d{3}-\d{3}-\d{4})"
customer_address_regex = r"([\d\s]+ [\w\s,.]+)"

def extract_invoice_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        invoice_number = re.search(invoice_number_regex, text)
        issue_date = re.search(issue_date_regex, text)
        business_name = re.search(business_name_regex, text)
        business_address = re.search(business_address_regex, text)
        customer_name = re.search(customer_name_regex, text)
        customer_email = re.search(customer_email_regex, text)
        customer_phone = re.search(customer_phone_regex, text)
        customer_address = re.search(customer_address_regex, text)

        extracted_data = [
            business_address.group(1).strip() if business_address else "",
            business_address.group(2).strip() if business_address else "",
            business_address.group(3).strip() if business_address else "",
            business_name.group(1).strip() if business_name else "",
            customer_address.group(1).strip() if customer_address else "",
            invoice_number.group(1).strip() if invoice_number else "",
            customer_address.group(1).strip() if customer_address else "",
            customer_address.group(1).strip() if customer_address else "",
            customer_email.group(1).strip() if customer_email else "",
            customer_name.group(1).strip() if customer_name else "",
            customer_phone.group(1).strip() if customer_phone else "",
            "",  # Placeholder for Invoice__BillDetails__Name
            "",  # Placeholder for Invoice__BillDetails__Quantity
            "",  # Placeholder for Invoice__BillDetails__Rate
            "",  # Placeholder for Invoice__Description
            "",  # Placeholder for Invoice__DueDate
            issue_date.group(1).strip() if issue_date else "",
            invoice_number.group(1).strip() if invoice_number else "",
            "",  # Placeholder for Invoice__Tax
        ]

        return extracted_data

def process_invoices():
    # Create the CSV file and write the header
    with open(output_csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "Bussiness__City",
            "Bussiness__Country",
            "Bussiness__Description",
            "Bussiness__Name",
            "Bussiness__StreetAddress",
            "Bussiness__Zipcode",
            "Customer__Address__line1",
            "Customer__Address__line2",
            "Customer__Email",
            "Customer__Name",
            "Customer__PhoneNumber",
            "Invoice__BillDetails__Name",
            "Invoice__BillDetails__Quantity",
            "Invoice__BillDetails__Rate",
            "Invoice__Description",
            "Invoice__DueDate",
            "Invoice__IssueDate",
            "Invoice__Number",
            "Invoice__Tax",
        ])

        # Iterate through the PDF invoices in the folder
        for filename in os.listdir(invoices_folder):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(invoices_folder, filename)
                extracted_data = extract_invoice_data(pdf_path)

                # Save the extracted data to the CSV file
                writer.writerow(extracted_data)

process_invoices()

