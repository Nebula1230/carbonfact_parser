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


The logic behind this kind of structuration is that we will be able by the end to create a One Big Table which a modelisation suitable for Data analysis especially if we use a column based database.


The run command is the following:

pip install -r requirements.txt

python main.py care_labels.csv. It will generate an output file by default called garments_parsed.json