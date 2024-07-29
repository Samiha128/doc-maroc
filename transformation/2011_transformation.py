import pandas as pd


abbreviation_dict = {
    'CSU': 'Centre de santé urbain',
    'CSUA': 'Centre de santé urbain avec module d\'accouchement',
    'CSC': 'Centre de santé communal',
    'CSCA': 'Centre de santé communal avec module d\'accouchement',
    'DR': 'Dispensaire Rural',
    'LEHM': 'Laboratoire épidémiologique et d\'hygiène de milieu',
    'CDTMR': 'Centre de diagnostic et de Traitement des maladies respiratoires',
    'CRSR': 'Centre de référence en santé reproductive'
}

def replace_abbreviation(abbreviation):
    return abbreviation_dict.get(abbreviation, abbreviation) 
excel_file = 'C:\\Users\\hp\\Desktop\\Sante\\Data\\liste-des-centres-de-sante-2011.xls'


try:
    df = pd.read_excel(excel_file, header=1)
except ImportError:
    raise ImportError("Module 'xlrd' non trouvé. Installez 'xlrd' >= 2.0.1 pour le support des fichiers Excel au format .xls.")

columns = df.columns.tolist()
print(f"Noms de colonnes après lecture : {columns}")

category_column = next((col for col in columns if 'Categorie' in str(col)), None)

if category_column:
    
    df['Nom Complet'] = df[category_column].apply(replace_abbreviation)

    
    df = df.iloc[:, 3:]

  
    output_file = excel_file.replace('.xls', '-modifie.csv').replace('Data', 'Data_transforme')

   
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"Le fichier {output_file} a été modifié et sauvegardé avec succès.")
else:
    raise KeyError(f"La colonne 'Categorie' est introuvable dans le fichier {excel_file}. Vérifiez les noms de colonnes.")
