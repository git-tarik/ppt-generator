import logging

logger = logging.getLogger("NotesBuilder")

def add_notes(slide, notes_text: str):
    """
    Adds speaker notes to a slide.
    """
    if not notes_text:
        return

    try:
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes_text
    except Exception as e:
        logger.warning(f"Failed to add notes: {e}")
