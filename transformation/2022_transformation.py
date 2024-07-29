import pandas as pd


abbreviation_dict = {
    'HP': 'Hôpital Provincial/Préfectoral',
    'HR': 'Hôpital Régional',
    'HIR': 'Hospital Interrégional',
    'HPr': 'Hôpital de Proximité',
    'CJ': 'Clinique du Jour',
    'HPsyP': 'Hôpital Psychiatrique Provincial/préfectoral',
    'CRO': 'Centre Régional d\'Oncologie',
    'CHD': 'Centre d\'HémoDialyse',
    'HPsyR': 'Hôpital Psychiatrique Régional',
    'CPU': 'Centre Psychiatrique Universitaire'
}


def replace_abbreviation(abbreviation):
    return abbreviation_dict.get(abbreviation, 'Unknown')

excel_file = 'C:\\Users\\hp\\Desktop\\Sante\\Data\\repartition des hoptales 2022.xlsx'


df = pd.read_excel(excel_file, header=1)

columns = df.columns.tolist()
print(f"Noms de colonnes après lecture : {columns}")

category_column = next((col for col in columns if 'Catégorie' in str(col)), None)

if category_column:
    
    df['Nom Complet'] = df[category_column].apply(replace_abbreviation)

   
    output_file = excel_file.replace('.xlsx', '-modifie.csv').replace('Data', 'Data_transforme')

   
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"Le fichier {output_file} a été modifié et sauvegardé avec succès.")
else:
    raise KeyError(f"La colonne 'Catégorie' est introuvable dans le fichier {excel_file}. Vérifiez les noms de colonnes.")
