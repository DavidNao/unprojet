from csv import DictReader, DictWriter
from typing import Dict, List

INPUT_FILE = "/home/david/Bureau/David/Projets/data/source/buildingref-france-majic-parcelles-millesime.csv"
OUTPUT_FILE = "morale_buildingref-france-majic-parcelles-millesime.csv"
# INPUT_FILE = "extract_buildingref-france-majic-parcelles-millesime.csv"
# OUTPUT_FILE = "extract_morale_2.csv"
EXCLUDED_COLUMNS = [
    "Année",
    "Code du département",
    "Code direction",
    "Code du droit exercé par le propriétaire (parcelle)",
    "Abréviation de la forme juridique (propriétaire)",
    "Nom Officiel Département",
    "Code Officiel EPCI",
    "Nom Officiel EPCI",
    "Code Officiel Région",
    "Nom Officiel Région",
]


def transform_columns(columns: List[str]):
    new_columns = [col for col in columns if col not in EXCLUDED_COLUMNS] + ["MORALE"]
    return new_columns


def transform_row(row: Dict) -> Dict:
    code = row.get("Code de la commune ou de l’arrondissement")
    section = row.get("Section (cadastre)")
    num_plan = row.get("Numéro de plan (cadastre)")
    section_mod = f"0{section}" if len(section) == 1 else section
    row["MORALE"] = f"{code}{section_mod}{num_plan}"
    return row


def main():
    print(f"Lecture du fichier {INPUT_FILE}")
    encoding = "utf-8-sig"
    delimiter = ";"
    with open(file=INPUT_FILE, mode="r", encoding=encoding) as read_csvfile:
        with open(file=OUTPUT_FILE, mode="w", encoding=encoding) as write_csvfile:
            reader = DictReader(read_csvfile, delimiter=delimiter)
            new_columns = transform_columns(columns=reader.fieldnames)
            writer = DictWriter(
                write_csvfile,
                fieldnames=new_columns,
                delimiter=delimiter,
                extrasaction="ignore",
            )
            writer.writeheader()
            for index, row in enumerate(reader):
                new_row = transform_row(row=row)
                writer.writerow(rowdict=new_row)
                if index and (index % 100000) == 0:
                    print(f"{str(index)} lignes ont été traitées !")
    print(f"Fin de l'écriture du fichier {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
