import logging
from pptx.enum.shapes import PP_PLACEHOLDER

logger = logging.getLogger("SlideBuilder")

def update_slide_content(slide, slide_data: dict):
    """
    Updates the text content of a slide's placeholders.
    """
    
    # 1. Identify Placeholders
    title_ph = None
    body_ph = None
    
    # Scan shapes to find placeholders (even if cloned)
    for shape in slide.shapes:
        if not shape.is_placeholder:
            continue
            
        ph_type = shape.placeholder_format.type
        
        # TITLE
        if ph_type == PP_PLACEHOLDER.TITLE or ph_type == PP_PLACEHOLDER.CENTER_TITLE:
            if not title_ph: title_ph = shape
            
        # BODY
        if ph_type == PP_PLACEHOLDER.BODY or ph_type == PP_PLACEHOLDER.OBJECT:
            if not body_ph: body_ph = shape
            
    # 2. Update Title
    if title_ph and 'title' in slide_data:
        try:
            if title_ph.text_frame:
                if title_ph.text_frame.paragraphs:
                    # Preserve formatting of the first paragraph if it exists
                    title_ph.text_frame.paragraphs[0].text = slide_data['title']
                else:
                    title_ph.text = slide_data['title']
        except Exception as e:
            logger.warning(f"Failed to update title: {e}")

    # 3. Update Body (Bullets)
    if body_ph and 'bullets' in slide_data:
        try:
            text_frame = body_ph.text_frame
            text_frame.clear() 
            
            bullets = slide_data.get("bullets", [])
            for bullet_text in bullets:
                p = text_frame.add_paragraph()
                p.text = bullet_text
                p.level = 0
        except Exception as e:
            logger.warning(f"Failed to update body: {e}")
            
    # 4. Update Notes
    if "notes" in slide_data and slide_data["notes"]:
        try:
            if not slide.has_notes_slide:
                slide.notes_slide
            
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            text_frame.text = slide_data["notes"]
        except Exception as e:
            logger.warning(f"Failed to add notes: {e}")
