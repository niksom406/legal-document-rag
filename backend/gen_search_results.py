"""
gen_search_results.py
Generates a synthetic Local Authority + Environmental + Water Search Report PDF.
"""
from fpdf import FPDF

OUTPUT = "../search_results.pdf"
NAVY = (13, 27, 46); GOLD = (180, 140, 60); GREY = (120, 130, 145)
LIGHT = (245, 246, 248); RED = (200, 50, 50); GREEN = (34, 120, 70); AMBER = (190, 120, 20)


class SearchPDF(FPDF):
    def header(self):
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 12, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        self.set_xy(10, 2)
        self.cell(0, 8, "PROPERTY SEARCH REPORT  |  MATTER AV-2025-04871  |  CONFIDENTIAL  |  SYNTHETIC SAMPLE")
        self.set_text_color(0, 0, 0)
        self.ln(12)

    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GREY)
        self.cell(0, 5, f"Property Search Report - 14 Elmwood Close, Guildford, Surrey GU2 7RN  |  Page {self.page_no()}/{{nb}}", align="C")

    def h2(self, text):
        self.set_fill_color(*NAVY)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 10)
        self.cell(190, 7, f"  {text}", fill=True, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 9)
        self.ln(1)

    def h3(self, text, color=None):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*(color or NAVY))
        self.cell(0, 6, text, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 9)

    def row(self, label, value):
        self.set_font("Helvetica", "B", 8.5)
        self.set_x(12)
        self.cell(50, 5.5, label)
        self.set_font("Helvetica", "", 8.5)
        self.multi_cell(138, 5.5, value)

    def result_banner(self, text, ok=True):
        col = GREEN if ok else RED
        self.set_fill_color(*col)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 9)
        self.cell(190, 6, f"  RESULT: {text}", fill=True, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 9)
        self.ln(1)

    def entry(self, title, detail, flag=None):
        colors = {"advisory": AMBER, "alert": RED, "clear": GREEN}
        col = colors.get(flag, NAVY)
        self.set_fill_color(*col)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 7.5)
        label = flag.upper() if flag else "ENTRY"
        self.cell(18, 5, label, fill=True, align="C")
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "B", 8.5)
        self.set_x(self.get_x() + 2)
        self.cell(0, 5, title, ln=True)
        self.set_font("Helvetica", "", 8.5)
        self.set_x(22)
        self.multi_cell(178, 5, detail)
        self.ln(1)

    def para(self, text, indent=0):
        self.set_font("Helvetica", "", 9)
        self.set_x(10 + indent)
        self.multi_cell(190 - indent, 5, text)
        self.ln(1)


def build():
    pdf = SearchPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    # Cover
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 9, "Property Search Report", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "14 Elmwood Close, Guildford, Surrey, GU2 7RN", ln=True)
    pdf.ln(2)

    pdf.row("Instructed by:", "ABC Conveyancing LLP (Matter AV-2025-04871)")
    pdf.row("On behalf of:", "Mr James R. Hargreaves & Ms Claire L. Hargreaves (Buyers)")
    pdf.row("Search date:", "6 June 2025")
    pdf.row("Report date:", "12 June 2025")
    pdf.row("Search provider:", "Groundsure Ltd & Surrey County Council")
    pdf.row("Property:", "14 Elmwood Close, Guildford, Surrey, GU2 7RN (Title No. SY884432)")
    pdf.ln(3)

    # Summary table
    pdf.h2("SUMMARY OF RESULTS")
    summaries = [
        ("Local Authority Search", "ENTRIES REVEALED", False),
        ("Environmental Search (Groundsure)", "NO ADVERSE ENTRIES", True),
        ("Water and Drainage Search", "ENTRIES REVEALED - REQUIRES REVIEW", False),
        ("Chancel Repair Search", "NO LIABILITY IDENTIFIED", True),
        ("Land Charges Search", "NO ENTRIES", True),
    ]
    pdf.set_fill_color(*LIGHT)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(90, 6, "Search Type", fill=True, border="B")
    pdf.cell(100, 6, "Result", fill=True, border="B", ln=True)
    for stype, result, ok in summaries:
        col = GREEN if ok else RED
        pdf.set_font("Helvetica", "", 8.5)
        pdf.cell(90, 5.5, stype, border="B")
        pdf.set_fill_color(*col)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.cell(100, 5.5, result, fill=True, border="B", ln=True)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(4)

    # ── SECTION 1: Local Authority ─────────────────────────────────────────
    pdf.h2("SECTION 1 - LOCAL AUTHORITY SEARCH (Surrey County Council)")
    pdf.result_banner("SOME ENTRIES REVEALED - See entries below", ok=False)
    pdf.row("Search authority:", "Surrey County Council, Planning Department")
    pdf.row("Search reference:", "GU/CON/2025/04471")
    pdf.row("Search date:", "6 June 2025 (date of official search)")
    pdf.row("Search valid until:", "6 months from date (6 December 2025)")
    pdf.ln(2)

    pdf.h3("1.1 Planning History")
    pdf.entry("Householder Application",
              "Application reference GU/2019/0447. Proposal: Single-storey rear extension to existing dwellinghouse. Decision: GRANTED 14 November 2019 under delegated officer authority. Conditions: None attached. Note: The local authority search reveals this planning permission but no corresponding building regulations completion certificate on the council's records. See Section 1.3 below.",
              "advisory")
    pdf.entry("Prior Approval Notification",
              "Application reference GU/2016/PD/0134. Class A permitted development - loft conversion. Decision: Prior approval not required, 3 October 2016. Note: No building regulations completion certificate located for loft conversion. Recommend raising enquiry with seller.",
              "advisory")
    pdf.entry("No other planning applications found", "No further planning applications, refusals, or enforcement notices were found relating to this property address.", "clear")

    pdf.h3("1.2 Road and Footpath Adoption")
    pdf.entry("Highway Adoption",
              "Elmwood Close is recorded as a publicly maintainable highway adopted under Section 38 of the Highways Act 1980. Surrey County Council is the highway authority. There are no outstanding adoption disputes or unadopted sections affecting access to the property.",
              "clear")

    pdf.h3("1.3 Building Regulations")
    pdf.entry("Building Regulations - Rear Extension (2019)",
              "Surrey Borough Council building control records have been searched. No building regulations completion certificate is recorded for the rear single-storey extension constructed under planning permission GU/2019/0447. This is a notable entry. The absence of a completion certificate means there is no formal confirmation that the extension was constructed in accordance with building regulations. This may affect the buyer's mortgage offer and may require: (a) the seller to obtain a retrospective regularisation certificate; or (b) defective title/building regulations indemnity insurance; or (c) further investigation. This matter is addressed in Enquiry E-11.",
              "alert")
    pdf.entry("Building Regulations - Loft Conversion (2016)",
              "No building regulations completion certificate is recorded for the loft conversion (prior approval GU/2016/PD/0134). It is unclear whether building regulations were submitted and inspected. Recommend raising enquiry with seller.",
              "advisory")

    pdf.h3("1.4 Tree Preservation Orders")
    pdf.entry("No TPOs", "No Tree Preservation Orders affect the property or any trees within the property boundary.", "clear")

    pdf.h3("1.5 Conservation Area")
    pdf.entry("Not in a Conservation Area", "The property is not situated within a designated conservation area. No additional planning controls apply.", "clear")

    pdf.h3("1.6 Listed Building")
    pdf.entry("Not Listed", "The property is not a listed building. It is not within the curtilage of a listed building.", "clear")

    pdf.h3("1.7 Enforcement Notices")
    pdf.entry("No Enforcement Notices", "No enforcement notices, breach of condition notices, stop notices, or listed building enforcement notices are recorded against this property address.", "clear")

    pdf.h3("1.8 Contaminated Land")
    pdf.entry("Not Designated Contaminated Land", "This property has not been designated as contaminated land under Part IIA of the Environmental Protection Act 1990. No remediation notices are recorded.", "clear")

    # ── SECTION 2: Environmental ───────────────────────────────────────────
    pdf.h2("SECTION 2 - ENVIRONMENTAL SEARCH (Groundsure Homebuyers)")
    pdf.result_banner("NO ADVERSE ENTRIES", ok=True)
    pdf.row("Search provider:", "Groundsure Ltd")
    pdf.row("Search reference:", "GS-2025-0889234")
    pdf.row("Report date:", "8 June 2025")
    pdf.ln(2)

    pdf.h3("2.1 Flood Risk")
    pdf.entry("Flood Zone Assessment",
              "The property falls within Environment Agency Flood Zone 1 (low probability). Flood Zone 1 is defined as having a less than 1 in 1,000 annual probability of flooding from rivers or the sea. There is no floodplain mapping affecting this address. Surface water flood risk is assessed as low. Groundwater flood risk is not significant for this location. No flood insurance concerns are anticipated on this basis alone.",
              "clear")

    pdf.h3("2.2 Ground Stability")
    pdf.entry("Mining and Subsidence",
              "No active or historic mining activity has been recorded within the search area. No coal mining legacy, chalk mining, or brine subsidence risk is identified. The property is not within a subsidence-prone area on available mapping.",
              "clear")
    pdf.entry("Landfill and Made Ground",
              "No current or former landfill sites are recorded within 250 metres of the property. No made ground or significant fill material is recorded on available geological mapping.",
              "clear")

    pdf.h3("2.3 Contaminated Land (Environmental)")
    pdf.entry("Contamination Assessment",
              "No current or historical industrial sites, filling stations, dry cleaners, chemical works, or other potentially contaminating land uses are recorded within 250 metres of the property. The site and surrounding area is recorded as predominantly residential use. Contamination risk is low.",
              "clear")

    pdf.h3("2.4 Radon")
    pdf.entry("Radon Risk",
              "The property falls within an area where the Public Health England radon affected area designation is less than 1% of properties above the action level. Radon protection is not required for this property under current guidance.",
              "clear")

    pdf.h3("2.5 Air Quality")
    pdf.entry("Air Quality Management",
              "The property is not within an Air Quality Management Area (AQMA). No significant point sources of air pollution are recorded within 500 metres. Nitrogen dioxide levels in this location are within national air quality objectives.",
              "clear")

    # ── SECTION 3: Water ───────────────────────────────────────────────────
    pdf.h2("SECTION 3 - WATER AND DRAINAGE SEARCH (Thames Water)")
    pdf.result_banner("ENTRIES REVEALED - REQUIRES FURTHER REVIEW", ok=False)
    pdf.row("Search authority:", "Thames Water Utilities Ltd")
    pdf.row("Search reference:", "TW-DG-2025-81447")
    pdf.row("Search date:", "6 June 2025")
    pdf.ln(2)

    pdf.h3("3.1 Water Supply")
    pdf.entry("Mains Water Connection",
              "The property is connected to the mains water supply. The connection is via a supply pipe running from the public water main in Elmwood Close. There are no recorded supply interruptions, quality notices, or billing disputes for this address.",
              "clear")
    pdf.entry("Water Meter",
              "A water meter is installed at the property. Thames Water records indicate the meter is operational and last read on 15 April 2025.",
              "clear")

    pdf.h3("3.2 Foul and Surface Water Drainage")
    pdf.entry("Public Sewer Connection",
              "The property is connected to the public combined sewer network. Both foul water and surface water drain to the public combined sewer.",
              "clear")
    pdf.entry("PUBLIC SEWER WITHIN 3 METRES OF PROPERTY - IMPORTANT",
              "Thames Water records show a public combined sewer (pipe reference TW-S-14EMW-02, diameter 225mm, constructed circa 1974) running parallel to the rear boundary of 14 Elmwood Close. The recorded centreline of the sewer is approximately 2.5 metres from the rear wall of the property (including the existing rear extension). Under the Water Industry Act 1991, Section 159, and the Building Regulations 2010 (Part H), any building or extension constructed within 3 metres of a public sewer requires prior consent from Thames Water. Thames Water records do not show any consent-to-build notice (also known as a building-over or building-near agreement) having been issued for this property address. This is a significant advisory entry. If the existing rear extension was constructed within 3 metres of the public sewer without Thames Water consent, this may constitute an unauthorised build-over or build-near. The consequences may include: (a) Thames Water requiring removal or modification of the extension; (b) difficulty obtaining mortgage finance; (c) difficulty with future sale. This matter is addressed in Enquiry E-07. ABC should obtain satisfactory evidence of Thames Water consent or, if consent was not obtained, consider the need for indemnity insurance and advise the buyer accordingly.",
              "alert")

    pdf.h3("3.3 Thames Water Infrastructure")
    pdf.entry("No Water Main within 3m",
              "Thames Water records confirm no water main is recorded within 3 metres of the property. The nearest water main is approximately 5.2 metres from the property boundary.",
              "clear")

    # ── SECTION 4: Chancel ─────────────────────────────────────────────────
    pdf.h2("SECTION 4 - CHANCEL REPAIR SEARCH")
    pdf.result_banner("NO LIABILITY IDENTIFIED", ok=True)
    pdf.para("A chancel repair search has been carried out. The property does not appear to be within a parish where potential chancel repair liability has been registered or is known to exist. Chancel repair liability, where it exists, can require property owners to contribute to the cost of repairs to the chancel of the local parish church. The Land Registration Act 2002 generally protects registered land owners from overriding interest chancel repair claims where the land was registered after October 2013. Title SY884432 was registered in 2009; however, no chancel repair entry is recorded on the register or in available chancel repair databases.")

    # ── SECTION 5: Land Charges ────────────────────────────────────────────
    pdf.h2("SECTION 5 - LAND CHARGES SEARCH (HM Land Registry)")
    pdf.result_banner("NO ENTRIES", ok=True)
    pdf.row("Search reference:", "HMLR-LC-2025-0047821")
    pdf.para("A search of the Land Charges Register has been carried out against the seller (Mrs Patricia Adaeze Okonkwo). No entries were found. In particular, no bankruptcy orders, voluntary arrangements, or pending actions were discovered.")

    pdf.h2("SOLICITOR'S NOTES")
    pdf.set_fill_color(*AMBER)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(190, 6, "  Points requiring resolution before exchange - for fee earner review", fill=True, ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.ln(1)
    notes = [
        "1. Building regulations completion certificate absent for rear extension (2019) and loft conversion (2016). See enquiries E-11 and follow-up with Bright & Co.",
        "2. Public sewer within 2.5m of rear wall of extension. Thames Water consent not on record. See enquiry E-07. If consent was not obtained, consider drainage indemnity insurance. Buyer to be advised.",
        "3. No other adverse search entries. Environmental, chancel, and land charges searches are clear.",
    ]
    for note in notes:
        self_x = 12
        pdf.set_x(self_x)
        pdf.multi_cell(188, 5, note)
        pdf.ln(1)

    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(*GREY)
    pdf.para("This document is a synthetic sample generated for interview demonstration purposes only. All references, data, and addresses are fictional. Prepared for ABC interview task, July 2025.")

    pdf.output(OUTPUT)
    print(f"OK: {OUTPUT}")


if __name__ == "__main__":
    build()
