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


df = pd.read_excel('C:\\Users\\hp\\Desktop\\Sante\\Data\\repartition-des-hopitaux.xlsx')


def replace_abbreviation(abbreviation):
    return abbreviation_dict.get(abbreviation, 'Unknown')


df['Nom Complet'] = df['Catégorie'].apply(replace_abbreviation)

df.to_csv('C:\\Users\\hp\\Desktop\\Sante\\Data_transforme\\repartition-des-hopitaux-modifie.csv', index=False, encoding='utf-8-sig')

print("Le fichier CSV a été modifié et sauvegardé avec succès.")


