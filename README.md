# Garment Data Model Explanation

This project uses a hierarchical data model to parse garment construction details from a CSV file into a JSON output suitable for analysis. The model is built around three main classes: **Material**, **ConstructionElement**, and **Garment**.

---

## 1. Material Class

**Purpose:**  
Represents a single material component in a garment construction.

**Fields:**

- **fabric_type (Optional):**  
  - A technical specification, for example, "GORE-TEX" or "CORDURA®".
  
- **name:**  
  - The base material name (e.g., "cotton", "polyester").
  
- **percentage:**  
  - The composition percentage of this material within the construction element (e.g., for "82% cotton", the percentage is `82`).

---

## 2. ConstructionElement Class

**Purpose:**  
Represents a distinct part of a garment's construction. Each element can describe different sections of a garment such as the main fabric, lining, or pocket lining.

**Fields:**

- **name:**  
  - The component identifier (e.g., "Main", "Lining", "Pocket lining").  
  - In cases where the input contains color information (e.g., `"Col 0400 and 2800:"`), the parser extracts the color codes into a separate list and uses a default element name (e.g., "Fabric Composition") instead.
  
- **colors:**  
  - A list of color codes associated with this element (e.g., `["0400", "2800"]`).
  
- **materials:**  
  - A list of **Material** objects that together describe the material composition (e.g., 82% cotton and 18% polyester).
  
- **weight:**  
  - The weight specification for the element (e.g., "220 g/m²").

---

## 3. Garment Class

**Purpose:**  
Represents a complete garment product by combining all its construction elements into a single record.

**Fields:**

- **code:**  
  - A unique product identifier (e.g., "#2877").
  
- **category:**  
  - The product type or category (e.g., "JACKET", "TSHIRT", "SWEATER/HOODIE").
  
- **construction:**  
  - A list of all **ConstructionElement** objects that describe the garment's build.

---
  The hierarchical structure can be flattened into a single table (or record set) with columns such as product code, category, element name, material percentages, material names, weight, and colors. This flat structure is ideal for column-based databases and analytical queries.

  ---

## How to Run the Application

1. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   python main.py care_labels.csv
