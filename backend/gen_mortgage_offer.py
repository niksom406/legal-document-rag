"""
generate_mortgage_offer.py
Generates a synthetic Halifax mortgage offer letter PDF.
Run: python generate_mortgage_offer.py
"""
from fpdf import FPDF

OUTPUT = "../mortgage_offer.pdf"
NAVY = (13, 27, 46)
GOLD = (180, 140, 60)
GREY = (120, 130, 145)
LIGHT = (245, 246, 248)
RED = (200, 50, 50)
GREEN = (34, 120, 70)
AMBER = (190, 120, 20)


class OfferPDF(FPDF):
    def header(self):
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 12, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        self.set_xy(10, 2)
        self.cell(0, 8, "HALIFAX plc  |  MORTGAGE OFFER  |  PRIVATE & CONFIDENTIAL  |  SYNTHETIC SAMPLE")
        self.set_text_color(0, 0, 0)
        self.ln(12)

    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GREY)
        self.cell(0, 5, f"Halifax plc is authorised by the PRA and regulated by the FCA and PRA. Registered in England No. 00002367. Page {self.page_no()}/{{nb}}", align="C")

    def h1(self, text):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*NAVY)
        self.cell(0, 9, text, ln=True)
        self.set_text_color(0, 0, 0)

    def h2(self, text):
        self.set_fill_color(*NAVY)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 9)
        self.cell(190, 6, f"  {text}", fill=True, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 9)
        self.ln(1)

    def row(self, label, value, bold_val=False):
        self.set_font("Helvetica", "B", 8.5)
        self.set_x(12)
        self.cell(55, 5.5, label)
        self.set_font("Helvetica", "B" if bold_val else "", 8.5)
        self.multi_cell(133, 5.5, value)

    def para(self, text, indent=0):
        self.set_font("Helvetica", "", 9)
        self.set_x(10 + indent)
        self.multi_cell(190 - indent, 5, text)
        self.ln(1)

    def condition(self, num, status, text):
        colors = {"MET": GREEN, "OUTSTANDING": RED, "STANDARD": AMBER}
        col = colors.get(status, GREY)
        self.set_fill_color(*col)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 7)
        self.cell(10, 5.5, str(num), fill=True, align="C")
        self.cell(22, 5.5, status, fill=True, align="C")
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 8.5)
        self.set_x(self.get_x() + 2)
        self.multi_cell(156, 5.5, text)


def build():
    pdf = OfferPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    # Header block
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*GREY)
    pdf.cell(0, 5, "Halifax plc, PO Box 548, Leeds, LS1 1WU", ln=True)
    pdf.cell(0, 5, "Telephone: 0345 850 3705   |   www.halifax.co.uk", ln=True)
    pdf.ln(3)
    pdf.set_text_color(0, 0, 0)

    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, "3 June 2025", ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 5, "Mr James R. Hargreaves & Ms Claire L. Hargreaves", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, "42 Beechwood Avenue", ln=True)
    pdf.cell(0, 5, "Woking, Surrey, GU21 3PQ", ln=True)
    pdf.ln(4)

    pdf.h1("MORTGAGE OFFER")
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GREY)
    pdf.cell(0, 5, "This is a binding mortgage offer subject to the conditions set out below. Please read carefully.", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    pdf.h2("PART 1 - OFFER DETAILS")
    pdf.row("Offer reference:", "HAL-2025-0061847")
    pdf.row("Offer date:", "3 June 2025")
    pdf.row("Offer valid until:", "3 December 2025 (6 months from offer date)")
    pdf.row("Borrowers:", "Mr James Richard Hargreaves (DOB 14/03/1985)")
    pdf.row("", "Ms Claire Louise Hargreaves (DOB 22/07/1987)")
    pdf.row("Property:", "14 Elmwood Close, Guildford, Surrey, GU2 7RN")
    pdf.row("Title number:", "SY884432 (Freehold)")
    pdf.row("Purchase price:", "GBP 485,000")
    pdf.row("Loan amount:", "GBP 363,750")
    pdf.row("Loan to value (LTV):", "75.00%")
    pdf.row("Solicitors acting:", "ABC Conveyancing LLP, ref: AV-2025-04871")
    pdf.ln(2)

    pdf.h2("PART 2 - LOAN TERMS")
    pdf.row("Interest rate:", "4.89% fixed for 60 months (5 years)")
    pdf.row("After fixed period:", "Halifax Standard Variable Rate (SVR), currently 7.49% p.a.")
    pdf.row("Repayment type:", "Capital and interest (repayment mortgage)")
    pdf.row("Term:", "25 years (300 monthly payments)")
    pdf.row("Monthly payment (fixed):", "GBP 2,108.43 (months 1-60)")
    pdf.row("Monthly payment (SVR):", "GBP 2,604.17 (estimated, months 61-300)")
    pdf.row("Total amount payable:", "GBP 626,401.20 (estimated, based on current SVR)")
    pdf.row("APRC:", "5.8% APRC (Annual Percentage Rate of Charge)")
    pdf.row("Early repayment charge:", "3% of outstanding balance in years 1-3; 2% in years 4-5; none thereafter")
    pdf.row("Arrangement fee:", "GBP 999 (added to loan; increases total cost)")
    pdf.row("Valuation fee:", "GBP 350 (paid by borrower; non-refundable)")
    pdf.ln(2)

    pdf.h2("PART 3 - PROPERTY VALUATION")
    pdf.para("Halifax instructed Savills Residential Valuation (RICS registered) to inspect and value the property.")
    pdf.row("Valuation date:", "28 May 2025")
    pdf.row("Valuer:", "Ms Rachel Obi MRICS, Savills, Guildford")
    pdf.row("Valuation figure:", "GBP 490,000")
    pdf.row("Reinstatement value:", "GBP 850,000 (for buildings insurance purposes)")
    pdf.para("The property is a 3-bedroom semi-detached house of brick construction with a pitched tiled roof, circa 1985. The valuer noted the following observations: (1) minor displacement of roof tiles to the rear elevation, visible from ground level, which the borrower should monitor and repair as necessary; (2) a damp patch approximately 0.3m x 0.2m in the north-west corner of the master bedroom, which appears consistent with condensation rather than rising or penetrating damp but should be investigated. The valuer did not reduce the valuation on account of these observations but recommended that the borrower obtain a specialist opinion. These observations are the basis of Special Condition 6 below.")
    pdf.ln(2)

    pdf.h2("PART 4 - SPECIAL CONDITIONS")
    pdf.para("The following conditions must be satisfied before Halifax will authorise release of mortgage funds. Failure to satisfy these conditions by the offer expiry date will result in the offer lapsing.")
    pdf.ln(1)

    conditions = [
        (1, "STANDARD", "Solicitor's certificate of title. ABC Conveyancing LLP must provide Halifax with a certificate of title in the CML Lenders' Handbook form confirming title is good and marketable, the property is suitable for mortgage security, and no material matters have been discovered that would affect Halifax's decision to lend."),
        (2, "OUTSTANDING", "Buildings insurance. The borrower must arrange buildings insurance with a sum insured of not less than GBP 850,000 (the reinstatement value confirmed by Halifax's valuer) from the date of exchange of contracts. Evidence of the policy number, insurer name, and commencement date must be provided to ABC before exchange. Halifax requires the policy to be in joint names of all borrowers. As at the date of this letter, no insurance evidence has been received."),
        (3, "MET", "Right to reside in the UK. Both borrowers have provided satisfactory evidence of British citizenship. This condition is satisfied."),
        (4, "MET", "Life assurance. Halifax recommends but does not require life assurance cover. Both borrowers confirmed they hold existing life assurance policies (Aviva, confirmed by Mr Hargreaves 28 May 2025). No further action required."),
        (5, "MET", "Satisfactory valuation. The property has been valued at GBP 490,000, which exceeds the purchase price of GBP 485,000. Halifax's security is therefore satisfactory. This condition is met."),
        (6, "OUTSTANDING", "Structural survey acceptance. The Halifax valuation report identified two observations requiring further investigation: roof tile displacement and a damp patch in the master bedroom. Halifax requires written confirmation from the borrower(s) that they have received a satisfactory RICS Level 2 HomeBuyer Report or Level 3 Building Survey and accept its findings, or that they have obtained specialist reports on both matters and are satisfied with the outcome. This written confirmation must be provided to ABC who will countersign and return it to Halifax before draw-down. As at the date of this letter, no such confirmation has been received."),
        (7, "MET", "No material change to property. The borrower confirms no material change to the property condition has occurred since the valuation date. Standard condition. Satisfied by borrower declaration 3 June 2025."),
        (8, "MET", "Completion within offer period. The target completion date of 28 August 2025 falls within the offer validity period (before 3 December 2025). This condition is met subject to completion proceeding as planned."),
        (9, "MET", "No undisclosed borrowing. Both borrowers have confirmed there is no undisclosed second charge, unsecured credit, or additional borrowing to be secured against the property. AML and credit checks were satisfactory. This condition is met."),
        (10, "MET", "Income verification. Both borrowers provided 3 months' payslips and P60 for the 2024/25 tax year. Mr Hargreaves: employed, gross annual salary GBP 74,000 (Deloitte LLP). Ms Hargreaves: employed, gross annual salary GBP 58,000 (NHS Trust). Combined gross income: GBP 132,000. Affordability assessment passed. This condition is met."),
        (11, "OUTSTANDING", "EWS1 External Wall Survey. The property was constructed in 1985. Halifax's current policy requires an EWS1 (External Wall Survey) form for all properties constructed before 1993 where the external wall construction type has not been independently confirmed as non-cladding and non-combustible. ABC wrote to Halifax on 10 July 2025 querying whether an EWS1 is required for a property of this age and traditional brick construction. Halifax has not yet responded to that query as at the date of this document. If Halifax confirms the EWS1 requirement, the borrower must instruct a qualified EWS1 assessor (estimated cost GBP 300-600, timeline 4-6 weeks). Halifax will not authorise draw-down until a satisfactory EWS1 form is received. This is a potential blocker to the planned completion date of 28 August 2025."),
        (12, "OUTSTANDING", "Gifted deposit declaration. Halifax has been notified that GBP 18,500 of the deposit is a gift from the borrower's parents (Mr and Mrs Hargreaves Sr). Halifax requires: (a) a signed gift letter from the donors confirming the gift is non-repayable and non-returnable; (b) bank statements from the donors for the last 3 months evidencing the source of the gifted funds; and (c) certified ID for both donors. These documents must be provided to ABC who will complete the required AML checks and confirm to Halifax. As at the date of this document, none of these items have been received."),
    ]

    for num, status, text in conditions:
        pdf.condition(num, status, text)
        pdf.ln(1)

    pdf.h2("PART 5 - IMPORTANT NOTICES")
    pdf.para("Your home may be repossessed if you do not keep up repayments on your mortgage.")
    pdf.para("This offer is made on the basis that the information provided in your mortgage application was accurate and complete. If any information changes before completion, you must notify Halifax immediately.")
    pdf.para("Halifax reserves the right to withdraw this offer if: (a) any information provided in the application proves to be inaccurate; (b) the property is damaged or its value materially changes before completion; (c) the borrower's financial circumstances change materially; or (d) the special conditions are not satisfied before the offer expiry date.")
    pdf.para("The Mortgage Credit Directive requires Halifax to provide you with a European Standardised Information Sheet (ESIS). Please refer to the ESIS provided separately for a full breakdown of costs and your legal right to a 7-day reflection period.")

    pdf.h2("PART 6 - ACCEPTANCE")
    pdf.para("This offer lapses if not accepted within 7 days of the offer date. To accept, please sign the acceptance below and return to Halifax via ABC Conveyancing LLP. Your solicitor's receipt of this offer on your behalf does not constitute acceptance.")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(90, 5, "Borrower 1 signature: _______________________")
    pdf.cell(90, 5, "Date: _______________", ln=True)
    pdf.ln(2)
    pdf.cell(90, 5, "Borrower 2 signature: _______________________")
    pdf.cell(90, 5, "Date: _______________", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(*GREY)
    pdf.para("Halifax plc. Registered in England and Wales, No. 00002367. Registered office: Trinity Road, Halifax, West Yorkshire, HX1 2RG. Authorised by the Prudential Regulation Authority and regulated by the Financial Conduct Authority and the Prudential Regulation Authority under registration number 702718. This document is a synthetic sample for interview demonstration purposes only. All names, figures, and details are fictional.")

    pdf.output(OUTPUT)
    print(f"OK: {OUTPUT}")


if __name__ == "__main__":
    build()
