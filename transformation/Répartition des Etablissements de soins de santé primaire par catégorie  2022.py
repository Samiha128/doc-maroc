import pandas as pd


category_abbreviation_dict = {
    'CSU-1': 'Centre de Santé Urbain niveau 1',
    'CSU-2': 'Centre de Santé Urbain niveau 2',
    'CSR-1': 'Centre de Santé Rural niveau 1',
    'CSR-2': 'Centre de Santé Rural niveau 2',
    'DR': 'Dispensaire Rural',
    'LSP': 'Laboratoire de Santé Publique',
    'CRSR': 'Centre de Référence en Santé de Reproduction',
    'CDTMR': 'Centre de Diagnostic et de Traitement des Maladies Respiratoires'
}


def replace_abbreviation(category):
    return category_abbreviation_dict.get(category, category)

excel_file = 'C:\\Users\\hp\\Desktop\\Sante\\Data\\Répartition des Etablissements de soins de santé primaire par catégorie  2022.xlsx'


try:
    df = pd.read_excel(excel_file, header=1)
except ImportError:
    raise ImportError("Module 'xlrd' non trouvé. Installez 'xlrd' >= 2.0.1 pour le support des fichiers Excel au format .xlsx.")


columns = df.columns.tolist()
print(f"Noms de colonnes après lecture : {columns}")


if 'Catégorie' in columns:
   
    df['Catégorie'] = df['Catégorie'].apply(replace_abbreviation)


output_file = excel_file.replace('.xlsx', '-modifie.csv').replace('Data', 'Data_transforme')

df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Le fichier {output_file} a été modifié et sauvegardé avec succès.")
