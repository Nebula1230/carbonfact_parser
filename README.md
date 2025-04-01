##### The logic behind the three classes

* Materiel Class: Represents a single material component in a garment construction

    - fabric_type: Optional technical specification (e.g "GORE-TEX", CORDURA")
    - name: Base material name (e.g. "cotton", "polyster")
    - percentage: Composition percentage in the construction element

* ConstructionElement Class: Represents a distinct part of a garment's construction

    - name: Component identifier (e.g., "Main", "Lining", "Pocket lining")

    - colors: List of color codes associated with this element

    - materials: List of Material objects making up this element

    - weight: Weight specification (e.g., "220 g/m²")

* Garment Class: Represents a complete garment product

    - code: Unique product identifier

    - category: Product type (e.g., "JACKET", "TSHIRT")

    - construction: List of all construction elements in the garment

Example of the output: 

**Before:**

 `#1102,JACKET,"Main: 100% polyamide, 220 g/m2. Reinforcement: 100% polyamide CORDURAÂ®, 205 g/mÂ². Lining: 100% solution dyed polyamide 65 g/mÂ². Cuff stretch: 90% polyester 10% elastane, 253 g/mÂ².  Insulation: 50% 37.5Â® polyester, 35% REPREVEÂ® recycled polyester, 15% polyester, 120 g/mÂ². Mesh: 100% polyester, 367 g/mÂ². Pocket lining: 100% polyester, 215 g/mÂ². "`

**After:**
`{
    "code": "#1102",
    "category": "JACKET",
    "construction": [
      {
        "name": "Main",
        "colors": [],
        "materials": [
          {
            "fabric_type": null,
            "name": "polyamide",
            "percentage": 100
          }
        ],
        "weight": "220 g/m²"
      },
      {
        "name": "Reinforcement",
        "colors": [],
        "materials": [
          {
            "fabric_type": null,
            "name": "polyamide cordura®",
            "percentage": 100
          }
        ],
        "weight": "205 g/m²"
      },
      {
        "name": "Lining",
        "colors": [],
        "materials": [
          {
            "fabric_type": null,
            "name": "solution dyed polyamide",
            "percentage": 100
          }
        ],
        "weight": "65 g/m²"
      },
      {
        "name": "Cuff stretch",
        "colors": [],
        "materials": [
          {
            "fabric_type": null,
            "name": "polyester",
            "percentage": 90
          },
          {
            "fabric_type": null,
            "name": "elastane",
            "percentage": 10
          }
        ],
        "weight": "253 g/m²"
      },
      {
        "name": "Insulation",
        "colors": [],
        "materials": [
          {
            "fabric_type": null,
            "name": "37.5® polyester",
            "percentage": 50
          },
          {
            "fabric_type": null,
            "name": "repreve® recycled polyester",
            "percentage": 35
          },
          {
            "fabric_type": null,
            "name": "polyester",
            "percentage": 15
          }
        ],
        "weight": "120 g/m²"
      },
      {
        "name": "Mesh",
        "colors": [],
        "materials": [
          {
            "fabric_type": null,
            "name": "polyester",
            "percentage": 100
          }
        ],
        "weight": "367 g/m²"
      },
      {
        "name": "Pocket lining",
        "colors": [],
        "materials": [
          {
            "fabric_type": null,
            "name": "polyester",
            "percentage": 100
          }
        ],
        "weight": "215 g/m²"
      }
    ]
  }`

  The algorithm rely on the csv_parser.py that contains multiple parse functions. 

## `clean_text(text: str) -> str`

**Purpose:**  
Normalizes and cleans raw text from the CSV file. This includes replacing common encoding artifacts, normalizing units, and removing extra whitespace around percentage signs.

---

## `parse_colors(segment: str) -> tuple[List[str], str]`

**Purpose:**  
Extracts color declarations from a segment of the construction details.  
For instance, if a segment starts with "Color:" or "Col:", it retrieves the color codes and returns the list along with the remainder of the segment without the color declaration.

**Logic:**  
- Uses a case‑insensitive regex pattern to match variations of "Color", "Colours", or "Col." followed by digits.
- Extracts color codes (e.g., four-digit numbers) from the matched group.
- Removes the color declaration from the original segment and returns both the list of color codes and the cleaned segment text.

---

## `parse_materials_and_weight(material_text: str) -> tuple[List[Material], str]`

**Purpose:**  
Parses a text string that contains one or more material definitions (each specified by a percentage and material name) and an optional weight value.  
It returns a list of `Material` objects along with a weight string (if found).

**Logic:**  
1. **Global Weight Extraction:**
   - Searches for a weight expression (e.g., `"280 g/m²"`).
   - If found, assigns it to `weight` and removes that substring from the material text.
2. **Fabric Type Prefix:**
   - Checks whether the material text starts with a fabric type descriptor.
   - If detected, saves it in `fabric_type` and removes it from the text.
3. **Splitting Material Definitions:**
   - Splits the remaining text into parts where each part should begin with a percentage.
4. **Processing Each Material:**
   - For each part, it extracts the percentage and material name via the regex `(\d+)%\s*(.*)`.
   - It further checks if the material name contains an embedded weight and removes it.
   - Handles nested material definitions (if a material name contains parenthesis), creating a separate `Material` for the nested information. (e.g. `"60% Cotton (40% Recycled Cotton)"`)
5. **Return:**
   - Finally, it returns a tuple containing the list of `Material` objects and the weight string.

---

## `parse_construction_details(detail_text: str) -> List[dict]`

**Purpose:**  
Splits the raw construction details into separate segments (each representing a distinct construction element) and then extracts the element name, associated color codes, material compositions, and weight.

**Logic:**  
- First, cleans the input text using `clean_text`.
- Splits the cleaned text into segments based on punctuation (e.g., periods and semicolons), while trying to preserve any context for color declarations.
- For each segment:
  - Calls `parse_colors` to extract any color declarations. If colors are found, they are stored as the current color context.
  - Splits the segment at a colon (`:`) into an element name and detail part. If no colon is found, defaults to `"Main"` as the element name.
  - Calls `parse_materials_and_weight` on the detail part to extract materials and weight.
  - If materials are successfully extracted, a dictionary is created containing:
    - `"name"`: The element’s name.
    - `"materials"`: A list of dictionaries representing each `Material` .
    - `"weight"`: The extracted weight.
    - `"colors"`: A copy of the current colors (if any).
- Returns a list of these construction element dictionaries.

PS: There is still some edge cases where the parse doesn't work well such as products that contains `body and sleeves` associated with weight (the weight is parsed but the suffix will be kept in the name e.g. product_id #1158)


The logic behind this kind of structuration is that we will be able by the end to create a One Big Table which is a modelisation suitable for Data analysis especially if we use a column based database.


The run command is the following:

`pip install -r requirements.txt`

`python main.py care_labels.csv`.

It will generate an output file by default called garments_parsed.json
