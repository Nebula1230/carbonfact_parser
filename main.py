from csv_parser import parse_garments_csv
import json

def save_to_json(garments, output_file):
    """Sauvegarder les résultats au format JSON"""
    data = [garment.model_dump() for garment in garments]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nDonnées sauvegardées dans {output_file} ({len(garments)} articles)")

if __name__ == "__main__":
    import sys
    if len(sys.argv) not in [2, 3]:
        print("Usage: python main.py <input.csv> [output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else "garments_parsed.json"
    
    try:
        garments = parse_garments_csv(input_file)
        save_to_json(garments, output_file)
    except Exception as e:
        print(f"Erreur : {str(e)}")
        sys.exit(1)