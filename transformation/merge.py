import pandas as pd


file1 = 'C:\\Users\\hp\\Desktop\\Sante\\Data_transforme\\repartition-des-hopitaux-modifie.csv'
file2 = 'C:\\Users\\hp\\Desktop\\Sante\\Data_transforme\\repartition des hoptales 2022-modifie.csv'


df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)


df2.rename(columns={
    'Etablissement hospitalier': 'Nom de l\'hôpital',
    'Commune': 'Commune/ville d\'implantation',
    'Delegation':'Délégation'
}, inplace=True)


merged_df = pd.concat([df1, df2], ignore_index=True, sort=False)


output_file = 'fichier_fusionne.csv'
merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Le fichier fusionné a été enregistré avec succès sous {output_file}.")
