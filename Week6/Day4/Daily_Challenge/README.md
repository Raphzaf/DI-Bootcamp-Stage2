# Week6 - Day4 - Daily Challenge

## Global Power Plant Database Analysis

Ce dossier contient un notebook complet pour analyser le dataset **Global Power Plant Database** avec :
- NumPy
- Pandas
- Matplotlib
- Seaborn

## Fichier principal
- `global_power_plant_analysis.ipynb`

## Ce que couvre l'analyse
1. Import et nettoyage des donnees (gestion des valeurs manquantes)
2. Conversion des colonnes numeriques
3. Statistiques descriptives (moyenne, mediane, ecart-type)
4. Distribution des centrales par pays et par type de carburant
5. Analyse statistique de la capacite (MW) par fuel
6. Test d'hypothese (permutation test) pour comparer les moyennes de capacite
7. Analyse temporelle via `commissioning_year`
8. Evolution du mix energetique par decennie
9. Visualisations avancees (barplots, boxplots, heatmap, geo scatter)
10. Operations matricielles (covariance, decomposition en valeurs propres)
11. Integration pratique NumPy + Pandas + Matplotlib

## Installation (si necessaire)
```bash
pip install numpy pandas matplotlib seaborn requests
```

## Execution
1. Ouvrir le notebook `global_power_plant_analysis.ipynb`
2. Lancer toutes les cellules dans l'ordre
3. Le dataset est telecharge automatiquement dans le dossier `data/` si absent

## Insights a mettre en avant dans le repo GitHub
Quand tu executes le notebook, mets en avant dans ton README principal :
- Les pays qui concentrent le plus grand nombre de centrales
- Les types de carburant les plus representes
- Les differences de capacite moyenne entre fuels (avec p-value)
- Les tendances temporelles de mise en service des centrales
- Les changements du mix energetique selon les decennies
- Ce que montrent les valeurs propres (axes de variation dominants)

## Suggestion de commit
```bash
git add Week6/Day4/Daily_Challenge
git commit -m "Add Day4 daily challenge notebook: global power plant analysis"
git push
```
