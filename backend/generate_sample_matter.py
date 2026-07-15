"""
generate_sample_matter.py

Generates a realistic synthetic conveyancing matter PDF for ABC demo purposes.
All data is entirely fictional. No confidential information from any employer is used.

Run: python generate_sample_matter.py
Output: ../sample_matter.pdf
"""

from fpdf import FPDF
from datetime import date

OUTPUT_PATH = "../sample_matter.pdf"


class MatterPDF(FPDF):
    NAVY = (13, 27, 46)
    GOLD = (180, 140, 60)
    LIGHT_GREY = (245, 246, 248)
    MID_GREY = (120, 130, 145)
    RED = (200, 50, 50)
    AMBER = (190, 120, 20)
    GREEN = (34, 120, 70)

    def header(self):
        # Top bar
        self.set_fill_color(*self.NAVY)
        self.rect(0, 0, 210, 14, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 9)
        self.set_xy(10, 3)
        self.cell(0, 8, "ABC CONVEYANCING  |  MATTER DOCUMENT  |  INTERNAL USE ONLY  |  SYNTHETIC SAMPLE", align="L")
        self.set_text_color(0, 0, 0)
        self.ln(14)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.MID_GREY)
        self.cell(0, 6, f"ABC - Synthetic Matter - Page {self.page_no()} of {{nb}}  |  Generated for interview demo only", align="C")

    def matter_title_block(self, matter_id, address, buyer, seller, price, completion_target):
        self.set_fill_color(*self.NAVY)
        self.rect(10, self.get_y(), 190, 38, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 14)
        self.set_xy(15, self.get_y() + 4)
        self.cell(0, 8, address)
        self.set_font("Helvetica", "", 8)
        self.set_xy(15, self.get_y() + 9)
        self.cell(60, 5, f"Matter ID: {matter_id}")
        self.set_xy(80, self.get_y())
        self.cell(60, 5, f"Buyer: {buyer}")
        self.set_xy(15, self.get_y() + 6)
        self.cell(60, 5, f"Seller: {seller}")
        self.set_xy(80, self.get_y())
        self.cell(60, 5, f"Purchase Price: {price}")
        self.set_xy(145, self.get_y())
        self.cell(60, 5, f"Target Completion: {completion_target}")
        self.set_text_color(0, 0, 0)
        self.set_xy(10, self.get_y() + 10)

    def section_heading(self, title):
        self.ln(4)
        self.set_fill_color(*self.NAVY)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 9)
        self.cell(190, 7, f"  {title}", fill=True, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 9)
        self.ln(2)

    def sub_heading(self, title):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.NAVY)
        self.cell(0, 6, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 9)

    def status_pill(self, label, status):
        """status: 'ok' | 'warning' | 'blocked'"""
        colors = {
            "ok": self.GREEN,
            "warning": self.AMBER,
            "blocked": self.RED,
        }
        col = colors.get(status, self.MID_GREY)
        self.set_fill_color(*col)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 7)
        x, y = self.get_x(), self.get_y()
        self.set_xy(x, y)
        self.cell(26, 4.5, label.upper(), fill=True, align="C")
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 9)
        self.set_xy(x + 28, y)

    def table_row(self, cols, widths, bold=False, shaded=False):
        if shaded:
            self.set_fill_color(*self.LIGHT_GREY)
        self.set_font("Helvetica", "B" if bold else "", 8)
        for i, (col, w) in enumerate(zip(cols, widths)):
            self.cell(w, 5.5, str(col), border="B" if not shaded else 0,
                      fill=shaded, ln=(1 if i == len(cols) - 1 else 0))

    def para(self, text, indent=0):
        self.set_font("Helvetica", "", 9)
        self.set_x(10 + indent)
        self.multi_cell(190 - indent, 5, text)
        self.ln(1)

    def bullet(self, text, indent=4):
        self.set_font("Helvetica", "", 9)
        x = self.get_x()
        self.set_x(10 + indent)
        self.cell(4, 5, chr(149))
        self.multi_cell(186 - indent, 5, text)

    def divider(self):
        self.set_draw_color(*self.NAVY)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)


def build():
    pdf = MatterPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ── Title block ───────────────────────────────────────────────────────────
    pdf.matter_title_block(
        matter_id="AV-2025-04871",
        address="14 Elmwood Close, Guildford, Surrey, GU2 7RN",
        buyer="Mr James R. Hargreaves & Ms Claire L. Hargreaves",
        seller="Mrs Patricia Okonkwo",
        price="£485,000",
        completion_target="28 August 2025",
    )

    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*pdf.MID_GREY)
    pdf.cell(0, 5, "Assigned fee earner: Sarah Chen  |  Supervising partner: David Patel  |  Last updated: 14 July 2025", ln=True)
    pdf.set_text_color(0, 0, 0)

    # ── Status Summary ────────────────────────────────────────────────────────
    pdf.section_heading("A. MATTER STATUS SUMMARY")

    statuses = [
        ("Local Authority Search", "RECEIVED", "warning", "Received 12 Jun 2025 - expires 3 months from date (11 Sep 2025). One drainage matter flagged - see Section D."),
        ("Environmental Search", "RECEIVED", "ok", "Received 8 Jun 2025. No adverse entries. Low flood risk confirmed."),
        ("Water & Drainage Search", "RECEIVED", "warning", "Public sewer within 3m of boundary. Building Regs consent for rear extension query raised - awaiting seller reply. See Enquiry E-07."),
        ("Land Registry Title", "RECEIVED", "ok", "Title absolute. Title number SY884432. Registered 14 March 2009."),
        ("Mortgage Offer", "RECEIVED", "warning", "Halifax offer dated 3 Jun 2025. Condition 6 (structural survey) and Condition 11 (EWS1 cladding form) remain outstanding. See Section F."),
        ("Draft Contract", "RECEIVED", "ok", "Seller's solicitors (Bright & Co) issued draft contract 20 May 2025. Approved with amendments 4 Jun 2025."),
        ("Enquiries Raised", "PARTIAL", "warning", "14 enquiries raised. 11 replies received. 3 outstanding - E-07, E-11, E-14 - see Section E."),
        ("TA6 Property Info Form", "RECEIVED", "ok", "Received 19 May 2025. Seller declares no disputes, no notices. Reviewed."),
        ("TA10 Fixtures & Fittings", "RECEIVED", "ok", "Received 19 May 2025. Items listed confirmed with buyer."),
        ("Buildings Insurance", "NOT RECEIVED", "blocked", "Buyer to arrange from exchange. Reminder sent 10 Jul 2025. No confirmation received."),
        ("Client ID Verification", "COMPLETE", "ok", "Both buyers verified via Thirdfort 2 Jun 2025. AML check passed."),
        ("Deposit Funds Confirmed", "PARTIAL", "warning", "£48,500 (10%) required. Buyer confirmed £30,000 available. Gifted deposit of £18,500 from buyer's parents - gift letter outstanding. See Section G."),
        ("Search Indemnity Insurance", "NOT APPLICABLE", "ok", "Full searches obtained. No indemnity insurance required."),
        ("Completion Statement", "NOT ISSUED", "warning", "Target: issue by 21 July 2025. Awaiting confirmation of deposit funds before finalising."),
    ]

    pdf.table_row(["Item", "Status", "Notes"], [55, 28, 107], bold=True, shaded=True)
    for item, status_label, status_type, note in statuses:
        x, y = pdf.get_x(), pdf.get_y()
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(55, 5.5, item, border="B")
        # status pill inline
        col_map = {"ok": pdf.GREEN, "warning": pdf.AMBER, "blocked": pdf.RED, "partial": pdf.AMBER}
        pdf.set_fill_color(*(col_map.get(status_type, pdf.MID_GREY)))
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 6.5)
        pdf.cell(28, 5.5, status_label, fill=True, border="B", align="C")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 8)
        pdf.multi_cell(107, 5.5, note, border="B")

    # ── Correspondence Log ────────────────────────────────────────────────────
    pdf.section_heading("B. CORRESPONDENCE LOG (most recent first)")

    correspondence = [
        ("14 Jul 2025", "Email IN", "Bright & Co", "Re: Enquiry E-11. Seller states planning permission for rear extension was granted under householder application GU/2019/0447. Copy of decision notice to follow."),
        ("10 Jul 2025", "Email OUT", "Mr & Ms Hargreaves", "Reminder: buildings insurance must be arranged before exchange. Please confirm insurer and policy number."),
        ("10 Jul 2025", "Email OUT", "Halifax Mortgages", "Chaser re Condition 11 (EWS1 form). Original request dated 3 Jun 2025. No response received."),
        ("08 Jul 2025", "Email IN", "Bright & Co", "Partial reply to enquiries. E-07 and E-14 remain outstanding. Seller's solicitor states E-07 response expected within 10 working days."),
        ("03 Jul 2025", "Letter IN", "Halifax Mortgages", "Mortgage offer valid confirmation. Offer stands. No amendments. Conditions 6 and 11 must be satisfied before draw-down."),
        ("01 Jul 2025", "Email OUT", "Bright & Co", "Second chaser for outstanding enquiries E-07, E-11, E-14. First chaser sent 19 June."),
        ("25 Jun 2025", "Email IN", "Mr Hargreaves", "Gift letter from parents (Mr & Mrs Hargreaves Sr) will be provided by 15 July. Parents are gifting £18,500 towards deposit. No repayment expected."),
        ("19 Jun 2025", "Email OUT", "Bright & Co", "First chaser for outstanding enquiries E-07, E-11, E-14."),
        ("12 Jun 2025", "Search Result", "Surrey CC / Groundsure", "Local authority search received. One drainage notation - public combined sewer within 3 metres of property boundary. Water authority consent may be required for any future extension."),
        ("04 Jun 2025", "Email OUT", "Bright & Co", "Contract approved with amendments: clause 6.3 (completion date) amended to 28 Aug 2025; clause 9.1 (title guarantee) confirmed full."),
        ("03 Jun 2025", "Mortgage Offer IN", "Halifax Mortgages", "Mortgage offer received. Loan amount £363,750 (75% LTV). Conditions: (1) satisfactory structural survey; (2-5) standard; (6) written confirmation of structural survey outcome; (11) EWS1 external wall survey form for property built 1985."),
        ("20 May 2025", "Draft Contract IN", "Bright & Co", "Draft contract pack received including: draft contract, TA6, TA10, title register (official copy), lease (not applicable - freehold), energy performance certificate (D rated)."),
        ("15 May 2025", "Email OUT", "Bright & Co", "Instruction letter and request for draft contract."),
    ]

    pdf.table_row(["Date", "Type", "From/To", "Summary"], [25, 22, 30, 113], bold=True, shaded=True)
    for i, (d, t, ft, summary) in enumerate(correspondence):
        pdf.set_fill_color(*pdf.LIGHT_GREY) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Helvetica", "", 7.5)
        h = max(5.5, len(summary) // 60 * 5 + 5)
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        pdf.cell(25, 5.5, d, border="B", fill=(i % 2 == 0))
        pdf.cell(22, 5.5, t, border="B", fill=(i % 2 == 0))
        pdf.cell(30, 5.5, ft, border="B", fill=(i % 2 == 0))
        pdf.multi_cell(113, 5.5, summary, border="B")

    # ── Title & Property ──────────────────────────────────────────────────────
    pdf.section_heading("C. TITLE & PROPERTY DETAILS")

    pdf.sub_heading("Land Registry Official Copy - Title Number SY884432")
    details = [
        ("Tenure:", "Freehold"),
        ("Property:", "14 Elmwood Close, Guildford, Surrey, GU2 7RN"),
        ("Registered proprietor:", "Patricia Adaeze Okonkwo"),
        ("Price paid (at registration):", "£310,000 (registered 14 March 2009)"),
        ("Lender charge:", "None (mortgage discharged 2021, DS1 noted on register)"),
        ("Restrictive covenants:", "Yes - covenant dated 14 March 2009 (on transfer). Restricts use to single private dwellinghouse. No commercial use. No further subdivision without consent."),
        ("Easements:", "Right of way over shared rear access track (see plan). Right of drainage through neighbouring land."),
        ("Third party rights:", "None noted on register."),
        ("Overriding interests:", "None declared by seller. Buyer's solicitor to advise buyer to inspect property for evidence of adverse occupation."),
    ]
    for label, val in details:
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_x(14)
        pdf.cell(52, 5, label)
        pdf.set_font("Helvetica", "", 8)
        pdf.multi_cell(138, 5, val)

    pdf.ln(2)
    pdf.sub_heading("Property Description (from TA6)")
    pdf.para("3-bedroom semi-detached house, circa 1985. Gas central heating installed 2018 (boiler serviced annually - last service April 2025). Rear single-storey extension built approximately 2019. Seller states planning permission was obtained. Seller has not provided copy of planning consent or building regulations completion certificate for extension - this is the subject of Enquiry E-11.")

    # ── Search Results ────────────────────────────────────────────────────────
    pdf.section_heading("D. SEARCH RESULTS")

    pdf.sub_heading("D1. Local Authority Search - Surrey County Council (received 12 June 2025)")
    pdf.para("Result: SOME ENTRIES REVEALED")
    items_la = [
        ("Planning decisions:", "Householder application GU/2019/0447 - rear single-storey extension - GRANTED 14 November 2019. No conditions attached to decision."),
        ("Building regulations:", "No completion certificate on record for GU/2019/0447. Seller's solicitor has been asked to explain - see Enquiry E-11."),
        ("Road adoption:", "Elmwood Close is a publicly adopted highway (s.38 adoption confirmed)."),
        ("Drainage:", "Public combined sewer recorded within 3 metres of the property boundary. Any extension or development within 3 metres of a public sewer requires prior consent from Thames Water under the Water Industry Act 1991. Staff note: the existing rear extension appears to be within this zone - see Enquiry E-07."),
        ("Tree preservation:", "No TPO affecting the property."),
        ("Conservation area:", "Not within a conservation area."),
        ("Listed building:", "Not listed."),
        ("Enforcement notices:", "None."),
    ]
    for label, val in items_la:
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_x(14)
        pdf.cell(42, 5, label)
        pdf.set_font("Helvetica", "", 8)
        pdf.multi_cell(148, 5, val)

    pdf.ln(2)
    pdf.sub_heading("D2. Environmental Search - Groundsure Homebuyers (received 8 June 2025)")
    pdf.para("Result: NO ADVERSE ENTRIES")
    env_items = [
        "Flood risk: LOW. Property not within Environment Agency flood zone 2 or 3.",
        "Ground stability: No mining, landfill, or subsidence risk recorded within search area.",
        "Contaminated land: No current or historical contamination entries within 250m.",
        "Radon: Radon affected area risk: less than 1% of properties. No radon protection required.",
        "Air quality: Within national air quality targets. No significant sources of industrial pollution within 500m.",
    ]
    for item in env_items:
        pdf.bullet(item)
    pdf.ln(2)

    pdf.sub_heading("D3. Water & Drainage Search - Thames Water (received 8 June 2025)")
    pdf.para("Result: ENTRIES REVEALED - REQUIRES FURTHER REVIEW")
    water_items = [
        "Mains water supply: Connected to mains. No outstanding queries.",
        "Foul water: Connected to public combined sewer.",
        "Surface water: Connected to public combined sewer.",
        "Public sewer within 3m of property: YES. Public combined sewer runs along the rear boundary, approximately 2.5 metres from the rear wall of the existing extension.",
        "Building over/near sewer: Thames Water records indicate a building or structure exists within 3 metres of the recorded sewer. No consent-to-build notice on record. This requires investigation - see Enquiry E-07.",
    ]
    for item in water_items:
        pdf.bullet(item)

    # ── Enquiries ─────────────────────────────────────────────────────────────
    pdf.section_heading("E. ENQUIRIES & REPLIES")

    enquiries = [
        ("E-01", "REPLIED", "ok",
         "Boundaries: Please confirm which boundaries the seller owns and maintains.",
         "Seller confirms: left boundary (as viewed from front) and rear boundary are seller's responsibility. Right boundary belongs to No. 16. Garden fence replaced by seller 2022."),
        ("E-02", "REPLIED", "ok",
         "Disputes and complaints: Are there any current or historic disputes with neighbouring properties?",
         "Seller states no disputes. No formal complaints received or made. No boundary disputes. No noise complaints."),
        ("E-03", "REPLIED", "ok",
         "Alterations: Please provide details of all structural alterations made since the seller purchased the property.",
         "Seller confirms: (1) rear single-storey extension built 2019 - see E-11; (2) new boiler installed 2018 - Gas Safe certificate available; (3) new bathroom fitted 2020 - no structural alterations, cosmetic only."),
        ("E-04", "REPLIED", "ok",
         "Services: Please confirm all utility services connected to the property.",
         "Gas, electricity, mains water, mains drainage. Broadband: Virgin Media fibre. No oil, no septic tank, no private drainage."),
        ("E-05", "REPLIED", "ok",
         "Guarantees and warranties: Are there any guarantees or warranties relating to the property?",
         "NHBC warranty expired (property built 1985). Boiler: manufacturer 5-year warranty, expires March 2023 (now expired). No damp-proof course guarantee. No timber treatment guarantee."),
        ("E-06", "REPLIED", "ok",
         "Notices: Has the seller received any notices, orders, or proposals from any authority relating to the property?",
         "Seller states no notices received. No enforcement notices. No planning enforcement correspondence."),
        ("E-07", "OUTSTANDING", "blocked",
         "Drainage - extension proximity to public sewer: The water and drainage search reveals a public combined sewer within 2.5 metres of the rear wall of the existing extension. Under the Water Industry Act 1991, Thames Water consent is required to build within 3 metres of a public sewer. Please provide: (a) evidence that Thames Water consent was obtained prior to construction; or (b) confirmation of the date construction was completed and confirmation that no consent was required at that time; or (c) an explanation if no consent was obtained.",
         "AWAITING REPLY. First chaser sent 19 June 2025. Second chaser sent 1 July 2025. Seller's solicitor indicated reply expected within 10 working days of 8 July 2025 - due by 22 July 2025. If consent was not obtained, indemnity insurance may be required."),
        ("E-08", "REPLIED", "ok",
         "Shared access: The title plan shows a shared rear access track. Please confirm the arrangements for use and maintenance.",
         "Seller confirms the access track is shared between Nos. 12, 14, and 16 Elmwood Close. No formal maintenance agreement exists. Informal arrangement: each owner maintains their section. No contributions requested in the last 10 years. No disputes."),
        ("E-09", "REPLIED", "ok",
         "Energy Performance Certificate: The EPC shows a D rating. Please confirm no enforcement action has been taken by the local authority.",
         "Seller confirms no enforcement action. Property is not a rental. EPC for information only. No minimum EPC requirement applies to owner-occupied properties."),
        ("E-10", "REPLIED", "ok",
         "Restrictive covenant - dwellinghouse use: The title register contains a covenant restricting use to a single private dwellinghouse. Please confirm the property has been used exclusively as such.",
         "Seller confirms property used solely as private residence throughout ownership. No commercial activity conducted from property. No home business registration. No planning permission sought for change of use."),
        ("E-11", "OUTSTANDING", "blocked",
         "Planning and building regulations - rear extension: The local authority search reveals planning permission GU/2019/0447 was granted for the rear extension but no building regulations completion certificate is recorded. Please provide: (a) the building regulations completion certificate; or (b) if no final inspection was carried out, confirmation of this and copies of any stage inspection certificates; or (c) if a regularisation certificate was obtained, a copy of same.",
         "PARTIAL REPLY received 14 July 2025: Seller states planning permission GU/2019/0447 was granted. Seller's solicitor states copy of decision notice to follow. Building regulations completion certificate not yet addressed in reply. STILL OUTSTANDING. Note: absence of building regulations sign-off may require indemnity insurance or seller to regularise before exchange."),
        ("E-12", "REPLIED", "ok",
         "Fixtures and fittings: Please confirm the items in the TA10 are correct and complete.",
         "Seller confirms TA10 is correct. Garden shed included in sale. Integrated dishwasher and washing machine included. Curtains and curtain poles in master bedroom excluded (buyer agreed)."),
        ("E-13", "REPLIED", "ok",
         "Completion arrangements: Please confirm the seller's expected position on the proposed completion date of 28 August 2025.",
         "Seller confirms 28 August 2025 is acceptable. Seller has already exchanged on onward purchase. Seller's solicitors to confirm chain status in due course."),
        ("E-14", "OUTSTANDING", "blocked",
         "Japanese knotweed: The environmental search did not identify Japanese knotweed but this question is raised separately. Has the seller ever identified or received notification of Japanese knotweed on or near the property?",
         "AWAITING REPLY. Raised 20 May 2025. No response received despite two chasers. Note: seller's TA6 section 7.4 states 'not aware of any' but formal enquiry reply required for file. If knotweed is present, mortgage lender Halifax may require treatment plan."),
    ]

    for eid, status_label, status_type, question, reply in enquiries:
        col_map = {"ok": pdf.GREEN, "warning": pdf.AMBER, "blocked": pdf.RED}
        pdf.set_fill_color(*col_map.get(status_type, pdf.MID_GREY))
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(12, 6, eid, fill=True, align="C")
        pdf.set_fill_color(*col_map.get(status_type, pdf.MID_GREY))
        pdf.cell(26, 6, status_label, fill=True, align="C")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_x(pdf.get_x() + 2)
        pdf.multi_cell(150, 6, f"Q: {question}")
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_x(14)
        pdf.set_text_color(*pdf.MID_GREY if status_type == "ok" else (0, 0, 0))
        pdf.multi_cell(186, 5, f"A: {reply}")
        pdf.set_text_color(0, 0, 0)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

    # ── Mortgage ──────────────────────────────────────────────────────────────
    pdf.section_heading("F. MORTGAGE OFFER - HALIFAX MORTGAGES (dated 3 June 2025)")

    pdf.sub_heading("Offer terms")
    mortgage_details = [
        ("Lender:", "Halifax plc (Bank of Scotland)"),
        ("Borrowers:", "Mr James R. Hargreaves & Ms Claire L. Hargreaves (joint)"),
        ("Loan amount:", "£363,750"),
        ("LTV:", "75%"),
        ("Rate:", "4.89% fixed for 5 years, reverting to SVR"),
        ("Repayment:", "Capital and interest, 25-year term"),
        ("Offer expiry:", "3 December 2025"),
    ]
    for label, val in mortgage_details:
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_x(14)
        pdf.cell(35, 5, label)
        pdf.set_font("Helvetica", "", 8)
        pdf.multi_cell(155, 5, val)

    pdf.ln(2)
    pdf.sub_heading("Special conditions requiring action before draw-down")
    conditions = [
        ("Condition 1", "ok", "Receipt of satisfactory solicitor's certificate of title. To be provided on exchange of contracts. STANDARD - no action required beyond normal exchange process."),
        ("Condition 2", "ok", "Buildings insurance: minimum sum insured £850,000. Buyer to arrange. Reminder sent 10 July 2025. NOT YET CONFIRMED."),
        ("Condition 3", "ok", "Evidence of buyer's right to reside in the UK. Provided - both buyers are British citizens."),
        ("Condition 4", "ok", "Life assurance: Halifax recommends but does not require. Buyer has confirmed existing policy. No action required."),
        ("Condition 5", "ok", "Valuation: Halifax panel valuer confirmed property value of £490,000 (above purchase price of £485,000). SATISFIED."),
        ("Condition 6", "warning", "Structural survey: Halifax requires written confirmation that the buyer has received a satisfactory structural survey report or RICS HomeBuyer Report and accepts its findings. Buyer commissioned RICS Level 2 HomeBuyer Report. Report received by buyer 1 June 2025. Report flagged minor roof tile displacement and damp in one corner of the master bedroom. BUYER HAS NOT YET CONFIRMED ACCEPTANCE. Solicitor chased buyer on 10 July 2025. No response. This condition must be satisfied before draw-down."),
        ("Condition 7", "ok", "No material change to property condition between offer and draw-down. Standard condition. Confirmed by buyer 3 June 2025."),
        ("Condition 8", "ok", "Completion to occur within 6 months of offer date (by 3 December 2025). Target completion 28 August 2025 is within this window. SATISFIED."),
        ("Condition 9", "ok", "No undisclosed second charge or additional borrowing secured on the property. Confirmed by buyer. SATISFIED."),
        ("Condition 10", "ok", "Buyer to provide payslips from last 3 months. Provided to Halifax directly by buyer. SATISFIED."),
        ("Condition 11", "blocked", "EWS1 External Wall Survey: Halifax requires a valid EWS1 form for this property as it was constructed in 1985 and the external wall construction has not been confirmed as non-cladding. Halifax wrote to the solicitor on 3 June 2025. Solicitor wrote to Halifax 10 July 2025 querying whether this is required for a property of this age and construction. NO RESPONSE RECEIVED FROM HALIFAX. If Halifax insists on this condition, a qualified EWS1 assessor must inspect the property. Cost to buyer estimated £300-£600. Timeline: 4-6 weeks from instruction. This is a POTENTIAL BLOCKER to completion by 28 August 2025."),
    ]
    for cid, status_type, desc in conditions:
        col_map = {"ok": pdf.GREEN, "warning": pdf.AMBER, "blocked": pdf.RED}
        pdf.set_fill_color(*col_map.get(status_type, pdf.MID_GREY))
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.cell(22, 5.5, cid, fill=True, align="C")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_x(pdf.get_x() + 2)
        pdf.multi_cell(166, 5, desc)

    # ── Deposit & Gifted Funds ────────────────────────────────────────────────
    pdf.section_heading("G. DEPOSIT & GIFTED FUNDS")

    pdf.sub_heading("Deposit breakdown")
    pdf.para("Total deposit required on exchange: £48,500 (10% of purchase price).")
    deposit_items = [
        ("Buyer's own funds:", "£30,000 - held in joint savings account. Evidence of source provided (bank statements, 3 months). CONFIRMED."),
        ("Gifted deposit:", "£18,500 - gift from Mr and Mrs Hargreaves Sr (buyer's parents). Mr Hargreaves confirmed by email 25 June 2025 that a gift letter will be provided by 15 July 2025. LETTER NOT YET RECEIVED (today is 14 July 2025 - due tomorrow)."),
    ]
    for label, val in deposit_items:
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_x(14)
        pdf.cell(40, 5, label)
        pdf.set_font("Helvetica", "", 8)
        pdf.multi_cell(150, 5, val)

    pdf.ln(2)
    pdf.sub_heading("AML requirements for gifted deposit")
    pdf.para("Halifax has been notified of the gifted deposit (standard requirement for 75% LTV mortgage). Halifax requires: (1) signed gift letter from donors confirming non-repayable gift; (2) evidence of source of gifted funds (donor bank statements, 3 months); (3) ID verification for donors. Items (2) and (3) not yet received. Gift letter (item 1) due 15 July 2025.")

    # ── Suggested Next Actions ────────────────────────────────────────────────
    pdf.section_heading("H. SUGGESTED NEXT ACTIONS (fee earner review required)")

    pdf.set_fill_color(*pdf.AMBER)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(190, 6, "  The following are suggested actions for review by the assigned fee earner. Not legal advice.", fill=True, ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    actions = [
        ("URGENT", "Enquiry E-07 (Thames Water / sewer proximity)", "Response due 22 July 2025 from Bright & Co. If no response by 23 July, escalate to senior partner. If Thames Water consent was not obtained, obtain quotes for drainage indemnity insurance. Advise buyer of risk."),
        ("URGENT", "Enquiry E-11 (Building regulations - extension)", "Chase Bright & Co for building regulations completion certificate or regularisation certificate. If neither is available, obtain indemnity insurance quote. Do not exchange without resolution or insurance in place."),
        ("URGENT", "Mortgage Condition 11 (EWS1 form)", "Chase Halifax for response to 10 July letter. If Halifax confirms requirement, instruct EWS1 assessor immediately. With 6-week timeline, 28 August completion may be at risk. Advise buyer and agree position."),
        ("THIS WEEK", "Gifted deposit - gift letter and AML docs", "Gift letter due tomorrow (15 July). Chase buyer and donors if not received. Obtain donor bank statements and ID. Halifax AML requirements must be met before exchange."),
        ("THIS WEEK", "Mortgage Condition 6 (structural survey acceptance)", "Chase buyer for written confirmation that they accept the HomeBuyer Report findings. Flag that condition must be satisfied before mortgage draw-down."),
        ("THIS WEEK", "Enquiry E-14 (Japanese knotweed)", "Chase Bright & Co for formal reply. If knotweed is present or historically treated, obtain specialist report and advise Halifax. Do not exchange without clarity."),
        ("BEFORE EXCHANGE", "Buildings insurance", "Buyer must confirm insurance policy and sum insured (minimum £850,000 per Halifax condition 2) before exchange. Chase buyer."),
        ("BEFORE EXCHANGE", "Completion statement", "Issue completion statement once deposit funds and gifted deposit documentation are confirmed. Target: 21 July 2025."),
        ("FOR INFORMATION", "Chain status", "Seller has exchanged on onward purchase. Confirm chain position with Bright & Co. Ensure all parties in chain are aligned on 28 August 2025 completion."),
    ]

    for priority, action, detail in actions:
        col = pdf.RED if priority == "URGENT" else (pdf.AMBER if priority == "THIS WEEK" else pdf.GREEN if priority == "BEFORE EXCHANGE" else pdf.MID_GREY)
        pdf.set_fill_color(*col)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 7)
        pdf.cell(22, 5.5, priority, fill=True, align="C")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_x(pdf.get_x() + 2)
        pdf.cell(0, 5.5, action, ln=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_x(26)
        pdf.multi_cell(174, 5, detail)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)

    # ── Footer note ───────────────────────────────────────────────────────────
    pdf.ln(4)
    pdf.set_fill_color(*pdf.NAVY)
    pdf.rect(10, pdf.get_y(), 190, 14, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_xy(15, pdf.get_y() + 3)
    pdf.multi_cell(180, 5, "This document is a synthetic sample generated for interview demonstration purposes only. All names, addresses, figures, and matter details are entirely fictional. No confidential information from any employer has been used. ABC - Internal use only.")
    pdf.set_text_color(0, 0, 0)

    pdf.output(OUTPUT_PATH)
    print(f"✅ Sample matter PDF written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
