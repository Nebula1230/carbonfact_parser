import csv
import re
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class Material(BaseModel):
    fabric_type: Optional[str] = None
    name: str
    percentage: int

class ConstructionElement(BaseModel):
    name: str
    colors: List[str] = Field(default_factory=list)
    materials: List[Material]
    weight: str

class Garment(BaseModel):
    code: str
    category: str
    construction: List[ConstructionElement]

def clean_text(text: str) -> str:
    """Enhanced cleaning with comprehensive weight normalization"""
    replacements = {
        "Â®": "®", "Ã©": "é", "Â²": "²", 
        "gr": "g", "Gr": "g", "GR": "g",
        "CORDURAÂ®": "CORDURA®",
        "REPREVEÂ®": "REPREVE®",
        "g/m2": "g/m²"  # Add explicit normalization for g/m2
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r'\s*%\s*', '%', text)
    return re.sub(r'\s+', ' ', text).strip()

def parse_construction_details(detail_text: str) -> List[dict]:
    """Parse construction details with enhanced color and element grouping"""
    elements = []
    detail_text = clean_text(detail_text)
    
    # Split segments while preserving color contexts
    segments = re.split(r'(?<!\bCol\.)(?<!\bCol)\s*[.;](?!\s*\d)', detail_text)
    
    current_colors = []
    
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        # Extract colors first
        colors, cleaned_segment = parse_colors(segment)
        current_colors = colors if colors else current_colors

        # Handle element name and details
        if ':' in cleaned_segment:
            name_part, detail_part = cleaned_segment.split(':', 1)
            name = name_part.strip()
            details = detail_part.strip()
        else:
            name = "Main"
            details = cleaned_segment

        # Extract weight and materials
        materials, weight = parse_materials_and_weight(details)

        if materials:
            elements.append({
                "name": name,
                "materials": [m.model_dump() for m in materials],
                "weight": weight,
                "colors": current_colors.copy()
            })
            current_colors = []

    return elements

def parse_materials_and_weight(material_text: str) -> tuple[List[Material], str]:
    """Improved material parser that extracts weight from material descriptions"""
    materials = []
    weight = ""
    
    # First check for separate weight specification in the text
    weight_match = re.search(r'(\d+\s*g(?:/m²)?)', material_text)
    if weight_match:
        weight = weight_match.group(1)
        # Remove standalone weight from material text
        material_text = material_text.replace(weight_match.group(0), '').strip(' ,')
    
    # Detect and extract fabric type prefix
    fabric_type = None
    fabric_match = re.match(r'^([A-Za-z®.\-\s]+?)\s(?=\d+%)', material_text)
    if fabric_match:
        fabric_type = fabric_match.group(1).strip()
        material_text = material_text[len(fabric_type):].strip()

    # Split materials while preserving technical specifications
    parts = re.split(r',\s*(?=\d+%)|\s+(?=\d+%)', material_text)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # Skip if this part is just a weight specification
        if re.match(r'^\d+\s*g', part, re.IGNORECASE) and len(part.split()) <= 2:
            continue

        match = re.match(r'(\d+)%\s*(.*)', part)
        if match:
            percentage = int(match.group(1))
            name = match.group(2).strip().lower()
            
            # Extract weight from material name if present
            material_weight_match = re.search(r'(\d+\s*g(?:/m²)?)', name)
            if material_weight_match:
                if not weight:  # Only use if we don't already have a weight
                    weight = material_weight_match.group(1)
                # Remove weight from material name
                name = name.replace(material_weight_match.group(0), '').strip(' ,')
            
            # Handle specific location mentions in the weight
            body_sleeves_match = re.search(r'in\s+body\s+and\s+sleeves', name)
            if body_sleeves_match:
                location_info = body_sleeves_match.group(0)
                name = name.replace(location_info, '').strip()
                # Attach the location info to the weight instead
                if weight:
                    weight += f" {location_info}"
            
            # Handle nested materials
            if '(' in name:
                name, nested = name.split('(', 1)
                nested = nested.rstrip(')').strip()
                nested_match = re.match(r'(\d+)%\s*(.*)', nested)
                if nested_match:
                    materials.append(Material(
                        name=nested_match.group(2).strip(),
                        percentage=int(nested_match.group(1)),
                        fabric_type=name.strip()
                    ))

            materials.append(Material(
                name=name,
                percentage=percentage,
                fabric_type=fabric_type
            ))

    return materials, weight

def parse_colors(segment: str) -> tuple[List[str], str]:
    """Enhanced color extraction with plural and abbreviated forms"""
    color_pattern = r'(?i)(?:Colou?rs?|Col\.?)(?:s|)\s*([\d\s,and]+?)(?=\s*\d+%|:|;|\.)'
    match = re.search(color_pattern, segment)
    if not match:
        return [], segment
    
    color_str = match.group(1).strip()
    color_str = re.sub(r'[^\d\s,and]+$', '', color_str)
    colors = [c.strip() for c in re.split(r',|\s+and\s+', color_str) if c.strip()]
    
    cleaned_segment = re.sub(color_pattern, '', segment, flags=re.IGNORECASE)
    return colors, cleaned_segment.strip(' :;,.')

def parse_garments_csv(file_path: str) -> List[Garment]:
    garments = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue
                
            code = row[0].strip()
            category = row[1].strip()
            details = clean_text(row[2])
            
            try:
                construction = parse_construction_details(details)
                garment = Garment.model_validate({
                    "code": code,
                    "category": category,
                    "construction": construction
                })
                garments.append(garment)
            except ValidationError as e:
                print(f"Error parsing row {row}: {e}")

    return garments