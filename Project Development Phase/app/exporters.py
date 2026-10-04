import os
from fpdf import FPDF


def save_pdf(layout: list, output_path: str = "static/exports/comic.pdf"):
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
   
    pdf.add_page()
    pdf.set_font("Arial", 'B', 28)
    pdf.ln(80)
    pdf.cell(0, 20, "ComicCraft AI", ln=True, align='C')
    pdf.set_font("Arial", 'I', 16)
    pdf.cell(0, 10, "Your AI Generated Comic Book", ln=True, align='C')
    
   
    for i, panel in enumerate(layout):
        pdf.add_page()
        
        pdf.set_font("Arial", 'B', 18)
        title = panel.get('title', f"Panel {i+1}")
        title = str(title).encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(0, 15, title, ln=True, align='C')
        pdf.ln(5)
        
        img_path = panel.get('image_path')
        if img_path and os.path.exists(img_path):
            img_w = 140
            x_pos = (210 - img_w) / 2
            y_pos = pdf.get_y()
            
            pdf.image(img_path, x=x_pos, y=y_pos, w=img_w)
            pdf.set_y(y_pos + img_w + 15)
        else:
            pdf.ln(20)
            
        pdf.set_font("Arial", '', 14)
        story_text = panel.get('text') or panel.get('story_text', '')
        story_text = str(story_text).encode('latin-1', 'replace').decode('latin-1')
        
        pdf.multi_cell(0, 8, story_text)
        
    pdf.output(output_path)
    return output_path