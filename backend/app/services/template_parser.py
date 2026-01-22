from pptx import Presentation
import io
import logging

# Configure logger
logger = logging.getLogger("TemplateParser")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(name)s] %(levelname)s: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.propagate = False


def analyze_presentation(file_content: bytes) -> dict:
    """
    Analyzes a PPTX file and extracts structural metadata.
    Returns a dictionary complying with Phase 2 requirements.
    """
    try:
        prs = Presentation(io.BytesIO(file_content))
    except Exception as e:
        logger.error(f"Failed to load presentation: {e}")
        return {"error": "Invalid PPTX file"}

    metadata = {
        "layout_count": len(prs.slide_layouts),
        "layouts": [],
        "theme": {
            "colors": {}, # Extraction of theme colors is complex in python-pptx, keeping placeholder
            "fonts": {}   # python-pptx doesn't easily expose theme fonts directly without XML parsing
        },
        "image_placeholders": []
    }

    for index, layout in enumerate(prs.slide_layouts):
        layout_data = {
            "index": index,
            "name": layout.name,
            "placeholders": []
        }
        
        for shape in layout.placeholders:
            ph_type = str(shape.placeholder_format.type)
            layout_data["placeholders"].append(ph_type)
            
            if 'PICTURE' in ph_type or 'BITMAP' in ph_type: 
                metadata["image_placeholders"].append({
                    "layout_index": index,
                    "placeholder_type": ph_type
                })

        metadata["layouts"].append(layout_data)

    metadata["theme"]["colors"] = {"note": "Deep theme extraction requires xml parsing"}
    metadata["theme"]["fonts"] = {"note": "Deep theme extraction requires xml parsing"}

    logger.info(f"Detected {metadata['layout_count']} layouts")
    
    for layout in metadata["layouts"]:
        logger.info(f"Layout {layout['index']} '{layout['name']}': {layout['placeholders']}")
        
    return metadata
