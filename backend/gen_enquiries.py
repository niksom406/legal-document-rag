"""
gen_enquiries.py
Generates a synthetic Pre-Contract Enquiries and Replies PDF (formal CPSE-style).
"""
from fpdf import FPDF

OUTPUT = "../enquiries_replies.pdf"
NAVY = (13, 27, 46); GREY = (120, 130, 145); LIGHT = (245, 246, 248)
RED = (200, 50, 50); GREEN = (34, 120, 70); AMBER = (190, 120, 20)


class EnquiryPDF(FPDF):
    def header(self):
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 12, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        self.set_xy(10, 2)
        self.cell(0, 8, "PRE-CONTRACT ENQUIRIES AND REPLIES  |  MATTER AV-2025-04871  |  WITHOUT PREJUDICE  |  SYNTHETIC SAMPLE")
        self.set_text_color(0, 0, 0)
        self.ln(12)

    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GREY)
        self.cell(0, 5, f"Pre-Contract Enquiries - 14 Elmwood Close, Guildford, Surrey GU2 7RN  |  Page {self.page_no()}/{{nb}}", align="C")

    def h2(self, text):
        self.set_fill_color(*NAVY)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 9)
        self.cell(190, 6.5, f"  {text}", fill=True, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 9)
        self.ln(1)

    def enquiry_block(self, eid, status, q_date, q_text, r_date, r_text):
        colors = {"REPLIED": GREEN, "OUTSTANDING": RED, "PARTIAL REPLY": AMBER}
        col = colors.get(status, GREY)
        self.set_fill_color(*col)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        self.cell(14, 6, eid, fill=True, align="C")
        self.cell(28, 6, status, fill=True, align="C")
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "I", 7.5)
        self.set_x(self.get_x() + 2)
        self.cell(0, 6, f"Raised: {q_date}", ln=True)
        # Question
        self.set_x(14)
        self.set_font("Helvetica", "B", 8)
        self.cell(10, 5, "Q:")
        self.set_font("Helvetica", "", 8.5)
        self.multi_cell(176, 5, q_text)
        # Reply
        self.set_x(14)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*col)
        self.cell(10, 5, "A:")
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "" if status == "REPLIED" else "I", 8.5)
        if r_date:
            self.set_font("Helvetica", "I", 7.5)
            x = self.get_x()
            self.cell(0, 5, f"[Reply dated {r_date}]", ln=True)
            self.set_x(24)
            self.set_font("Helvetica", "" if status == "REPLIED" else "I", 8.5)
        self.set_x(24)
        self.multi_cell(176, 5, r_text)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)


def build():
    pdf = EnquiryPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 8, "Pre-Contract Enquiries and Replies", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, "Property: 14 Elmwood Close, Guildford, Surrey, GU2 7RN", ln=True)
    pdf.cell(0, 5, "Seller: Mrs Patricia Adaeze Okonkwo", ln=True)
    pdf.cell(0, 5, "Buyer: Mr James R. Hargreaves & Ms Claire L. Hargreaves", ln=True)
    pdf.cell(0, 5, "Seller's solicitors: Bright & Co, 18 High Street, Guildford, GU1 3AX (ref: BC/PO/2025/0187)", ln=True)
    pdf.cell(0, 5, "Buyer's solicitors: ABC Conveyancing LLP (ref: AV-2025-04871)", ln=True)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GREY)
    pdf.cell(0, 5, "These enquiries are raised without prejudice and are subject to contract.", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    pdf.h2("PART A - STANDARD ENQUIRIES (Replies by Bright & Co on behalf of seller)")

    enquiries = [
        ("E-01", "REPLIED", "20 May 2025", "Boundaries: Please identify which boundaries the seller owns, is responsible for maintaining, and confirm whether any boundary has been moved or altered during the seller's ownership.",
         "4 Jun 2025", "The seller owns and is responsible for maintaining the left-hand boundary (as viewed from the road) and the rear boundary. The right-hand boundary belongs to the owner of 16 Elmwood Close. The rear garden fence along the rear boundary was replaced by the seller in 2022 on the same line as the previous fence. No boundary has been altered in any other way during the seller's ownership."),

        ("E-02", "REPLIED", "20 May 2025", "Disputes: Are there any current or past disputes, complaints, or negotiations with neighbours or third parties relating to the property, its boundaries, access, or use?",
         "4 Jun 2025", "The seller confirms there are no current or past disputes with any neighbouring owner. No formal complaints have been made or received. There have been no boundary disputes or informal disagreements during the seller's ownership. The seller is on good terms with neighbours at Nos. 12 and 16 Elmwood Close."),

        ("E-03", "REPLIED", "20 May 2025", "Alterations and Improvements: Please provide full details of all structural alterations, extensions, or improvements made to the property since the seller's purchase, including dates and whether planning permission and building regulations consent were obtained.",
         "4 Jun 2025", "The seller confirms the following works were carried out: (1) Rear single-storey extension constructed in 2019. Planning permission was obtained under reference GU/2019/0447 (granted 14 November 2019). The seller states that building regulations approval was applied for and that inspections were carried out. A copy of the building regulations completion certificate has been requested from the local authority by the seller's solicitor and will be provided when received. (2) New gas boiler installed in March 2018 by Corgi-registered engineer (now Gas Safe). Gas Safe certificate provided in the disclosure bundle. (3) New bathroom fitted in 2020, cosmetic work only, no structural changes. No building regulations required."),

        ("E-04", "REPLIED", "20 May 2025", "Services: Please confirm all services connected to the property including gas, electricity, water, drainage, telecommunications and broadband.",
         "4 Jun 2025", "The property has the following services connected: Gas (British Gas, mains supply), Electricity (EDF Energy, mains supply), Mains water (Thames Water), Mains drainage - foul and surface water both drain to public sewer, Broadband (Virgin Media fibre, up to 500Mbps), Telephone landline (BT Openreach). No oil, no LPG, no septic tank, no private drainage."),

        ("E-05", "REPLIED", "20 May 2025", "Guarantees, Warranties, and Indemnities: Please provide details of any guarantees, warranties, or indemnity policies relating to the property or any works carried out, and confirm they will be assigned to the buyer.",
         "4 Jun 2025", "The following guarantees/warranties are available and will be assigned to the buyer: (1) Gas Safe certificate for boiler installation (March 2018) - copy provided. (2) Boiler manufacturer warranty: Worcester Bosch Greenstar 8000, 5-year warranty commencing March 2018 (expired March 2023 - no longer in force). (3) NHBC warranty for original construction (1985) - expired. No other guarantees or warranties are available. No indemnity insurance policies are in place."),

        ("E-06", "REPLIED", "20 May 2025", "Notices: Please confirm whether the seller has received any notices, orders, or proposals from any government body, local authority, utility, or third party affecting the property.",
         "4 Jun 2025", "The seller confirms no notices have been received from any authority, utility, or third party during the seller's ownership. No planning enforcement correspondence, no drainage notices, no compulsory purchase notices, no tree preservation order notifications."),

        ("E-07", "OUTSTANDING", "20 May 2025", "Thames Water Consent - Rear Extension: The water and drainage search reveals a public combined sewer within approximately 2.5 metres of the rear wall of the existing rear extension. Under the Water Industry Act 1991 and Building Regulations Part H, Thames Water consent (a 'build-over' or 'build-near' agreement) is required for any construction within 3 metres of a public sewer. Please provide: (a) evidence that Thames Water consent was obtained prior to or during construction of the rear extension; or (b) if consent was not required at the time of construction, confirmation of the basis on which it was not required; or (c) if consent was not obtained, a full explanation.",
         None, "OUTSTANDING AS AT 14 JULY 2025. First enquiry raised 20 May 2025. First chaser sent 19 June 2025. Second chaser sent 1 July 2025. Bright & Co stated on 8 July 2025 that they are awaiting a response from the seller and expected a reply within 10 working days (due 22 July 2025). No reply received as at date of this document. If Thames Water consent was not obtained, ABC will need to consider drainage indemnity insurance and advise the buyer of the risk."),

        ("E-08", "REPLIED", "20 May 2025", "Shared Access: The title plan shows a shared rear access track running behind Nos. 12-16 Elmwood Close. Please confirm the legal basis for this access, the arrangements for maintenance, and whether any disputes or claims have arisen.",
         "4 Jun 2025", "The seller confirms the rear access track is a shared private right of way appurtenant to Nos. 12, 14, and 16 Elmwood Close. The right of way is granted by a deed of easement dated 15 March 2009 (copy available on request). There is no formal maintenance agreement; the three owners maintain their respective sections informally. The seller has not been asked to contribute to any maintenance costs during their ownership and no disputes have arisen regarding the shared access."),

        ("E-09", "REPLIED", "20 May 2025", "Energy Performance Certificate: Please confirm whether the seller is aware of any enforcement action by the local authority regarding the EPC rating and whether the seller intends to carry out any energy improvements before completion.",
         "4 Jun 2025", "The property has an EPC rating of D (score 62). The seller is not aware of any enforcement action regarding the EPC. The property is owner-occupied and is therefore not subject to the Minimum Energy Efficiency Standards that apply to rented properties. The seller does not intend to carry out energy improvements before completion but has no objection to the buyer doing so after completion."),

        ("E-10", "REPLIED", "20 May 2025", "Restrictive Covenants: The title register contains a covenant dated 14 March 2009 restricting use to a single private dwellinghouse. Please confirm the property has been used exclusively as such and that no breach of covenant has occurred.",
         "4 Jun 2025", "The seller confirms the property has been used exclusively as a private dwellinghouse throughout their ownership. No commercial activity has been carried on from the property. No home business registration has been made. No letting or sub-letting has occurred. No planning permission for change of use has been sought or granted."),

        ("E-11", "PARTIAL REPLY", "20 May 2025", "Building Regulations Completion Certificate - Rear Extension: The local authority search reveals planning permission GU/2019/0447 was granted for the rear extension but no building regulations completion certificate is recorded on the local authority's records. Please provide: (a) a copy of the building regulations completion certificate; or (b) if no final inspection was obtained, a copy of all stage inspection certificates and an explanation of why a completion certificate was not obtained; or (c) if a regularisation certificate was subsequently obtained, a copy of that certificate.",
         "14 Jul 2025", "PARTIAL REPLY received 14 July 2025 from Bright & Co: The seller confirms planning permission GU/2019/0447 was granted and the extension was built in accordance with that permission. A copy of the planning decision notice is to follow (not yet received by ABC). The seller states that building regulations approval was applied for and that the local building control inspector attended on site during construction. The seller is unable to locate the completion certificate at present and is requesting a copy from the local authority. OUTSTANDING ELEMENT: No building regulations completion certificate or regularisation certificate has been provided. The enquiry in relation to building regulations is not yet fully answered. ABC should not exchange contracts without either: (a) receipt of the building regulations completion certificate; (b) receipt of a regularisation certificate; or (c) appropriate indemnity insurance in place and buyer advised."),

        ("E-12", "REPLIED", "20 May 2025", "Fixtures, Fittings, and Contents: Please confirm the TA10 form is accurate and complete and that all items listed as included will be left in the property on completion.",
         "4 Jun 2025", "The seller confirms the TA10 is accurate and complete. All items listed as included will be left at the property on completion. In particular: the garden shed is included; the integrated dishwasher (Bosch, kitchen) is included; the integrated washing machine (Siemens, kitchen) is included. The following items are excluded: curtains and curtain poles in the master bedroom (noted on TA10). All other items are as stated on the TA10."),

        ("E-13", "REPLIED", "20 May 2025", "Completion Date: Please confirm whether the proposed completion date of 28 August 2025 is acceptable to the seller and confirm the seller's position in the chain.",
         "4 Jun 2025", "The seller confirms 28 August 2025 is acceptable as the target completion date. The seller has exchanged contracts on their onward purchase (a 4-bedroom detached house in Woking, Surrey) with a completion date also agreed as 28 August 2025. The seller's solicitors will confirm chain details in due course. The chain is as follows (in summary): Buyer (Hargreaves) - 14 Elmwood Close - Seller (Okonkwo) - onward purchase (Woking)."),

        ("E-14", "OUTSTANDING", "20 May 2025", "Japanese Knotweed: Has the seller or any previous owner identified the presence of Japanese knotweed on or near the property at any time? Please confirm whether the seller is aware of any Japanese knotweed in the garden, on neighbouring land, or on the shared rear access track, and whether any treatment plan has ever been put in place.",
         None, "OUTSTANDING AS AT 14 JULY 2025. Raised 20 May 2025. The seller's TA6 form (Section 7.4) states 'Not aware of any Japanese knotweed.' However, ABC requires a formal reply to this enquiry for the file. First chaser sent 19 June 2025. Second chaser sent 1 July 2025. No formal reply received despite two chasers. NOTE: If Japanese knotweed is present, the Halifax mortgage lender may require a treatment and monitoring programme (typically GBP 2,000-5,000 over 3 years) and a specialist surveyor's confirmation before draw-down. This enquiry must be answered before exchange."),
    ]

    for data in enquiries:
        pdf.enquiry_block(*data)

    pdf.h2("PART B - ADDITIONAL ENQUIRIES (Supplemental - raised by ABC)")

    supp_enquiries = [
        ("E-15", "REPLIED", "4 Jun 2025", "Gas Safety: Please provide copies of all Gas Safe certificates for the boiler and any other gas appliances at the property, and confirm the date of the last annual service.",
         "8 Jun 2025", "Gas Safe certificate for boiler installation (March 2018) provided in the disclosure bundle. Annual service records: boiler serviced annually by British Gas HomeCare. Last service date: 15 April 2025. Annual service certificate for 2025 provided. Previous years' certificates available on request."),

        ("E-16", "REPLIED", "4 Jun 2025", "Electrical Installation Condition Report: Has an EICR (Electrical Installation Condition Report) been carried out at the property? If so, please provide a copy. If not, please confirm the last date electrical works were carried out.",
         "8 Jun 2025", "An EICR was not carried out during the seller's ownership as the property is owner-occupied and no rewiring has been undertaken. The seller is not legally required to obtain an EICR for a private sale. The existing wiring was inspected by an electrician in 2016 as part of the bathroom refurbishment. No issues were identified at that time. The buyer may wish to commission their own EICR after completion."),

        ("E-17", "REPLIED", "10 Jun 2025", "Parking: Please confirm the parking arrangements for the property including whether there is a garage, driveway, or allocated parking space.",
         "16 Jun 2025", "The property benefits from a single detached garage at the rear (accessible from the shared rear access track) and a dropped kerb driveway to the front providing off-street parking for two vehicles. The garage is in good repair. There is no parking permit scheme affecting the road. On-street parking in Elmwood Close is unrestricted."),

        ("E-18", "OUTSTANDING", "1 Jul 2025", "Loft Conversion: The local authority search reveals a prior approval notification (GU/2016/PD/0134) for a loft conversion. Please provide building regulations completion certificate or confirmation of the works carried out.",
         None, "OUTSTANDING AS AT 14 JULY 2025. Raised 1 July 2025. No reply received. Bright & Co have been chased. See local authority search notes."),
    ]

    for data in supp_enquiries:
        pdf.enquiry_block(*data)

    pdf.h2("OUTSTANDING ENQUIRY SUMMARY")
    pdf.set_fill_color(*RED)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(190, 6, "  3 enquiries outstanding as at 14 July 2025 - exchange cannot proceed until resolved", fill=True, ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.ln(1)
    outstanding = [
        ("E-07", "Thames Water consent for rear extension proximity to public sewer", "Due 22 Jul 2025 per Bright & Co"),
        ("E-14", "Japanese knotweed confirmation", "No response after 2 chasers"),
        ("E-18", "Loft conversion building regulations", "Raised 1 Jul 2025, no reply"),
    ]
    for eid, desc, note in outstanding:
        pdf.set_fill_color(*RED)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(12, 5.5, eid, fill=True, align="C")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.cell(0, 5.5, f"{desc} - {note}", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(*GREY)
    pdf.multi_cell(190, 5, "This document is a synthetic sample for interview demonstration purposes. All names, figures, addresses, and legal details are entirely fictional. ABC Conveyancing LLP - Synthetic demonstration, July 2025.")

    pdf.output(OUTPUT)
    print(f"OK: {OUTPUT}")


if __name__ == "__main__":
    build()
