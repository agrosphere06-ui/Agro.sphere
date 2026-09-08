from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR

prs = Presentation("SIH2026-IDEA-Presentation-Format.pptx")

# Delete slide 7 (instructions slide)
rId = prs.slides._sldIdLst[6].rId
prs.part.drop_rel(rId)
del prs.slides._sldIdLst[6]

# Helper to update team name oval on slides
team_name = "Agro-Sphere Innovators"
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame and "Your Team Name" in shape.text_frame.text:
            shape.text_frame.text = team_name
            for p in shape.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.font.bold = True

# ==========================================
# SLIDE 1: TITLE PAGE
# ==========================================
slide1 = prs.slides[0]
for shape in slide1.shapes:
    if shape.has_text_frame and "Problem Statement ID" in shape.text_frame.text:
        tf = shape.text_frame
        tf.clear()
        
        items = [
            ("Problem Statement ID: ", "SIH1645 (Smart Agriculture & Farm Connect)"),
            ("Problem Statement Title: ", "AI Mandi Price Intelligence, Quality Grading & Farm Logistics"),
            ("Theme: ", "Agriculture, FoodTech & Rural Development"),
            ("PS Category: ", "Software"),
            ("Team ID: ", "SIH2026-TEAM-AGRO"),
            ("Team Name: ", "Agro-Sphere Innovators"),
            ("Project / Idea: ", "Agro-Sphere (Multilingual Farmer Intelligence Platform)"),
            ("GitHub Repo: ", "https://github.com/agrosphere06-ui/Agro.sphere.git"),
            ("Live Web App: ", "https://agrosphere06-ui.github.io/Agro.sphere/")
        ]
        
        for label, val in items:
            p = tf.add_paragraph()
            r1 = p.add_run()
            r1.text = label
            r1.font.bold = True
            r1.font.size = Pt(12)
            r1.font.color.rgb = RGBColor(23, 58, 37)
            
            r2 = p.add_run()
            r2.text = val
            r2.font.bold = False
            r2.font.size = Pt(12)
            r2.font.color.rgb = RGBColor(45, 45, 45)
            p.space_after = Pt(4)

# Add Logo to Slide 1
slide1.shapes.add_picture("assets/logo.png", Inches(8.3), Inches(4.3), width=Inches(1.6))

# ==========================================
# SLIDE 2: PROPOSED SOLUTION
# ==========================================
slide2 = prs.slides[1]
for shape in slide2.shapes:
    if shape.has_text_frame and "Proposed Solution" in shape.text_frame.text:
        tf = shape.text_frame
        tf.clear()
        
        lines = [
            ("Agro-Sphere: Unified Farm Intelligence & Direct Market Ecosystem", True, 13, RGBColor(23, 58, 37)),
            ("• Transparent Mandi Discovery: Live modal rates across APMC mandis (Lasalgaon, Nashik, Pune) with predictive 7-day selling recommendations.", False, 10.5, RGBColor(40, 40, 40)),
            ("• Verified Quality Grading & Inspection: Standardized lot specs (moisture %, size 45-55mm, zero residue test, defect <2%) for Grade A, B & Premium produce.", False, 10.5, RGBColor(40, 40, 40)),
            ("• Zero-Waste Fast Clearance: Emergency fast-sale channel for perishable surplus fruits/vegetables to eliminate post-harvest crop rotting.", False, 10.5, RGBColor(40, 40, 40)),
            ("• FPO Collective Pooling: Aggregates small farmer harvests into 100q+ bulk lots to secure institutional buyer pricing & reduce freight.", False, 10.5, RGBColor(40, 40, 40)),
            ("• End-to-End Live Logistics: Real-time truck tracking (MH-15), driver contact dispatch, weighbridge slot booking, and digital calendar milestones.", False, 10.5, RGBColor(40, 40, 40)),
            ("• Multilingual Voice AI Sahayak: Voice-operated in Hindi, Marathi & English for non-literate farmers with 24x7 Toll-Free Helpline (1800-889-2476).", False, 10.5, RGBColor(40, 40, 40))
        ]
        
        for text, bold, size, color in lines:
            p = tf.add_paragraph()
            p.text = text
            p.font.bold = bold
            p.font.size = Pt(size)
            p.font.color.rgb = color
            p.space_after = Pt(3)

slide2.shapes.add_picture("products_modal_shot.png", Inches(6.8), Inches(1.8), width=Inches(3.0))

# ==========================================
# SLIDE 3: TECHNICAL APPROACH
# ==========================================
slide3 = prs.slides[2]
for shape in slide3.shapes:
    if shape.has_text_frame and "Technologies to be used" in shape.text_frame.text:
        tf = shape.text_frame
        tf.clear()
        
        lines = [
            ("Technical Architecture & Execution Methodology", True, 13, RGBColor(23, 58, 37)),
            ("• Modern Web & Mobile Stack: Responsive Glassmorphism architecture, CSS Grid/Flexbox, dynamic modular section routing.", False, 10.5, RGBColor(40, 40, 40)),
            ("• Voice AI Engine: Web Speech API (STT & TTS) + Vapi.ai Telephony Integration supporting Hindi, Marathi, and Indian English.", False, 10.5, RGBColor(40, 40, 40)),
            ("• Logistics & Scheduling Engine: Real-time route progression, live GPS coordinate simulator, and dynamic monthly milestone calendar.", False, 10.5, RGBColor(40, 40, 40)),
            ("• Multilingual I18n System: Real-time DOM dictionary translation across 12 Indian regional languages.", False, 10.5, RGBColor(40, 40, 40)),
            ("• Security & Settlement: PIN-verified weighbridge authorization and instant ledger balance tracking.", False, 10.5, RGBColor(40, 40, 40))
        ]
        
        for text, bold, size, color in lines:
            p = tf.add_paragraph()
            p.text = text
            p.font.bold = bold
            p.font.size = Pt(size)
            p.font.color.rgb = color
            p.space_after = Pt(2.5)

slide3.shapes.add_picture("architecture_flowchart.png", Inches(0.8), Inches(4.2), width=Inches(4.8))
slide3.shapes.add_picture("schedule_shot.png", Inches(5.8), Inches(4.2), width=Inches(3.9))

# ==========================================
# SLIDE 4: FEASIBILITY AND VIABILITY
# ==========================================
slide4 = prs.slides[3]
for shape in slide4.shapes:
    if shape.has_text_frame and "Analysis of the feasibility" in shape.text_frame.text:
        tf = shape.text_frame
        tf.clear()
        
        lines = [
            ("Feasibility, Risk Analysis & Mitigation Strategies", True, 13, RGBColor(23, 58, 37)),
            ("• Technical Feasibility: Lightweight client architecture works on low-bandwidth 2G/3G rural networks with offline resilience.", False, 10.5, RGBColor(40, 40, 40)),
            ("• Operational Feasibility: Multi-channel support (24x7 Toll-Free 1800-889-2476, WhatsApp Photo Grading +91 98200 45678, on-ground APMC officers).", False, 10.5, RGBColor(40, 40, 40)),
            ("• Financial Viability: Disintermediates exploitative middlemen (saving 15-20% margin for farmers); self-sustainable via minimal 0.5% buyer transaction fee.", False, 10.5, RGBColor(40, 40, 40)),
            ("• Challenge: Low Digital Literacy among elderly farmers.", False, 10.5, RGBColor(180, 40, 40)),
            ("  ↳ Mitigation: Multilingual AI Voice Sahayak with one-touch voice chips and natural speech queries.", False, 10.5, RGBColor(23, 58, 37)),
            ("• Challenge: Weight & Quality Disputes at Mandi Yard.", False, 10.5, RGBColor(180, 40, 40)),
            ("  ↳ Mitigation: Digital weighbridge PIN verification receipt and local field officer dispute desk.", False, 10.5, RGBColor(23, 58, 37)),
            ("• Challenge: Spoilage of Perishable Produce.", False, 10.5, RGBColor(180, 40, 40)),
            ("  ↳ Mitigation: Priority Zero-Waste Fast Clearance tag and instant buyer flash-sale notifications.", False, 10.5, RGBColor(23, 58, 37))
        ]
        
        for text, bold, size, color in lines:
            p = tf.add_paragraph()
            p.text = text
            p.font.bold = bold
            p.font.size = Pt(size)
            p.font.color.rgb = color
            p.space_after = Pt(2)

# ==========================================
# SLIDE 5: IMPACT AND BENEFITS
# ==========================================
slide5 = prs.slides[4]

# Remove template placeholder TextBox 8
for shape in list(slide5.shapes):
    if shape.has_text_frame and "Potential impact" in shape.text_frame.text:
        sp = shape._element
        sp.getparent().remove(sp)

# 1. Benefits Card (Left Column)
card1 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.60), Inches(1.30), Inches(5.95), Inches(5.45))
card1.fill.solid()
card1.fill.fore_color.rgb = RGBColor(246, 252, 247)
card1.line.color.rgb = RGBColor(167, 219, 180)
card1.line.width = Pt(1.5)

tf1 = card1.text_frame
tf1.word_wrap = True
tf1.vertical_anchor = MSO_ANCHOR.TOP
tf1.margin_left = Inches(0.25)
tf1.margin_right = Inches(0.25)
tf1.margin_top = Inches(0.20)
tf1.margin_bottom = Inches(0.20)

p = tf1.paragraphs[0]
p.text = "📈 DIRECT & MEASURABLE BENEFITS"
p.font.bold = True
p.font.size = Pt(13.5)
p.font.color.rgb = RGBColor(18, 64, 38)
p.space_after = Pt(2)

p_sub = tf1.add_paragraph()
p_sub.text = "Direct financial gains & operational savings delivered directly to farmers & FPOs"
p_sub.font.size = Pt(9.5)
p_sub.font.italic = True
p_sub.font.color.rgb = RGBColor(50, 95, 60)
p_sub.space_after = Pt(8)

benefits = [
    ("+18% to +25% Farmer Realized Profit: ", "Disintermediates middleman cartels & commission fees (saving 12%–18% margins), putting an extra ₹350–₹550 per quintal directly into farmer bank accounts."),
    ("-30% Logistics & Freight Cost Savings: ", "FPO collective pooling aggregates small 10–20q harvests into 100q+ bulk truckloads, eliminating dead-freight trips with scheduled return-load dispatch."),
    ("-35% Post-Harvest Perishable Loss: ", "Emergency Zero-Waste fast-clearance channel liquidates perishable surpluses (tomatoes, onions) to bulk food processing buyers in <12 hours before rotting."),
    ("100% Escrow Security & 15-Min Payouts: ", "Replaces traditional 15–30 day delayed informal credit default risks with automated bank settlement upon digital weighbridge PIN clearance."),
    ("-85% Mandi Yard Congestion & Wait Times: ", "Digital gate-pass scheduling and weighbridge queue slots compress farmer waiting time from 36 hours down to under 4 hours."),
    ("Predictive Price Discovery & Selling Windows: ", "Multi-mandi 30-day continuous price tracking alerts farmers to peak selling days, avoiding distress offloading during localized market crashes.")
]

for title, desc in benefits:
    p = tf1.add_paragraph()
    r1 = p.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(9.8)
    r1.font.color.rgb = RGBColor(18, 64, 38)
    
    r2 = p.add_run()
    r2.text = desc
    r2.font.bold = False
    r2.font.size = Pt(9.1)
    r2.font.color.rgb = RGBColor(45, 45, 45)
    p.space_after = Pt(5.5)

p_box = tf1.add_paragraph()
r_box = p_box.add_run()
r_box.text = "💡 Tangible Impact Example: A smallholder farmer selling 50 quintals of Grade A onion earns an extra ~₹22,500 net profit and saves ~₹4,200 in pooled transport costs."
r_box.font.bold = True
r_box.font.size = Pt(9.0)
r_box.font.color.rgb = RGBColor(15, 80, 40)
p_box.space_after = Pt(0)

# 2. Impact Card (Right Top)
card2 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(1.30), Inches(5.98), Inches(2.65))
card2.fill.solid()
card2.fill.fore_color.rgb = RGBColor(241, 247, 255)
card2.line.color.rgb = RGBColor(186, 214, 251)
card2.line.width = Pt(1.5)

tf2 = card2.text_frame
tf2.word_wrap = True
tf2.vertical_anchor = MSO_ANCHOR.TOP
tf2.margin_left = Inches(0.25)
tf2.margin_right = Inches(0.25)
tf2.margin_top = Inches(0.18)
tf2.margin_bottom = Inches(0.18)

p = tf2.paragraphs[0]
p.text = "🌍 BROADER & LASTING SOCIETAL IMPACT"
p.font.bold = True
p.font.size = Pt(12.5)
p.font.color.rgb = RGBColor(24, 60, 115)
p.space_after = Pt(2)

p_sub = tf2.add_paragraph()
p_sub.text = "Long-term systemic transformation and societal value created by accumulated benefits over time"
p_sub.font.size = Pt(9.0)
p_sub.font.italic = True
p_sub.font.color.rgb = RGBColor(60, 95, 145)
p_sub.space_after = Pt(5)

impacts = [
    ("Rural Poverty Alleviation & De-leveraging: ", "Sustained profit breaks village moneylender debt traps, fostering inter-generational farm wealth and arresting distress rural migration."),
    ("Smallholder & FPO Institutional Leverage: ", "Organizes 86% marginal farmers into bankable collective enterprises with corporate-level bargaining power."),
    ("National Food Security & Price Stability: ", "Eliminating supply friction and crop spoilage tempers urban food inflation while guaranteeing farmer floor realization."),
    ("Digital & Financial Inclusion for Kisans: ", "Multilingual Voice AI (Hindi/Marathi/English) empowers non-literate farmers with direct digital commerce & UPI banking.")
]

for title, desc in impacts:
    p = tf2.add_paragraph()
    r1 = p.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(9.3)
    r1.font.color.rgb = RGBColor(24, 60, 115)
    
    r2 = p.add_run()
    r2.text = desc
    r2.font.bold = False
    r2.font.size = Pt(8.8)
    r2.font.color.rgb = RGBColor(45, 45, 45)
    p.space_after = Pt(3)

# 3. Revenue Model Card (Right Bottom)
card3 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(4.10), Inches(5.98), Inches(2.65))
card3.fill.solid()
card3.fill.fore_color.rgb = RGBColor(254, 252, 235)
card3.line.color.rgb = RGBColor(245, 222, 140)
card3.line.width = Pt(1.5)

tf3 = card3.text_frame
tf3.word_wrap = True
tf3.vertical_anchor = MSO_ANCHOR.TOP
tf3.margin_left = Inches(0.25)
tf3.margin_right = Inches(0.25)
tf3.margin_top = Inches(0.18)
tf3.margin_bottom = Inches(0.18)

p = tf3.paragraphs[0]
p.text = "💼 HOW WE GENERATE INCOME (REVENUE MODEL)"
p.font.bold = True
p.font.size = Pt(12.5)
p.font.color.rgb = RGBColor(140, 75, 10)
p.space_after = Pt(2)

p_sub = tf3.add_paragraph()
p_sub.text = "100% Free for Farmers — Sustainable monetization via institutional buyers & B2B ecosystem"
p_sub.font.size = Pt(9.0)
p_sub.font.italic = True
p_sub.font.color.rgb = RGBColor(135, 85, 25)
p_sub.space_after = Pt(5)

revenues = [
    ("0.5% – 1.0% Buyer Platform Escrow Fee: ", "Charged to wholesale buyers, food processors & modern retailers on settled escrow orders for digital compliance & lot provenance."),
    ("2% – 3% Logistics Fleet Aggregation Margin: ", "Commission earned from partnered logistics & trucking fleet operators for guaranteed round-trip load dispatch and route optimization."),
    ("Enterprise Market Intelligence SaaS: ", "Subscription fees from FMCG brands, exporters, and agri-lenders for multi-mandi predictive price forecasting, crop yield estimates & audit reports."),
    ("Digital Weighbridge & Assaying Fee: ", "Nominal revenue-sharing margin with APMC yards on automated digital weighbridge slip generation and BIS/AGMARK quality verification.")
]

for title, desc in revenues:
    p = tf3.add_paragraph()
    r1 = p.add_run()
    r1.text = "• " + title
    r1.font.bold = True
    r1.font.size = Pt(9.3)
    r1.font.color.rgb = RGBColor(140, 75, 10)
    
    r2 = p.add_run()
    r2.text = desc
    r2.font.bold = False
    r2.font.size = Pt(8.8)
    r2.font.color.rgb = RGBColor(45, 45, 45)
    p.space_after = Pt(3)

# ==========================================
# SLIDE 6: RESEARCH AND REFERENCES
# ==========================================
slide6 = prs.slides[5]
for shape in slide6.shapes:
    if shape.has_text_frame and "Details / Links" in shape.text_frame.text:
        tf = shape.text_frame
        tf.clear()
        
        lines = [
            ("Research Grounding, Live Deployment & References", True, 13, RGBColor(23, 58, 37)),
            ("• Live Web Platform: https://agrosphere06-ui.github.io/Agro.sphere/", True, 10.5, RGBColor(33, 115, 70)),
            ("• Official GitHub Codebase: https://github.com/agrosphere06-ui/Agro.sphere.git", True, 10.5, RGBColor(20, 80, 160)),
            ("• Government Data Reference: Agmarknet (Directorate of Marketing & Inspection, Ministry of Agriculture & Farmers Welfare).", False, 10.5, RGBColor(40, 40, 40)),
            ("• Post-Harvest Loss Research: NITI Aayog Strategy for Doubling Farmers Income & Central Institute of Post-Harvest Engineering (CIPHET).", False, 10.5, RGBColor(40, 40, 40)),
            ("• Quality & Grading Standards: Bureau of Indian Standards (BIS) & APEDA Export Produce Specifications for Fruits & Vegetables.", False, 10.5, RGBColor(40, 40, 40)),
            ("• Voice AI Technology: Deepgram Multilingual Speech Recognition & Vapi.ai Telephony Voice Pipelines.", False, 10.5, RGBColor(40, 40, 40))
        ]
        
        for text, bold, size, color in lines:
            p = tf.add_paragraph()
            p.text = text
            p.font.bold = bold
            p.font.size = Pt(size)
            p.font.color.rgb = color
            p.space_after = Pt(3)

slide6.shapes.add_picture("prices_shot.png", Inches(5.8), Inches(3.2), width=Inches(3.8))

prs.save("Agro_Sphere_SIH2026_Idea_Presentation.pptx")
print("Saved final polished Agro_Sphere_SIH2026_Idea_Presentation.pptx!")
