# Child Malnutrition in Nigeria: A Landscape Analysis (2024 DHS)

This project analyses the prevalence and distribution of child malnutrition
across Nigeria using data from the 2024 Demographic and Health Survey (DHS).
It examines stunting, wasting, and underweight rates across regions,
residence type, household wealth, maternal education, and child age.

## Project Overview

Malnutrition remains one of the most significant public health challenges facing children in Nigeria. This analysis uses nationally representative survey data to answer a central question:

**Where is child malnutrition most concentrated in Nigeria, and what demographic and socioeconomic factors are associated with higher rates?**

As I became more interested in the use of data for healthcare and public health, I found myself returning to a simple question: how evenly are health outcomes distributed across different groups of people?

In this project, I use data from the 2024 Nigeria Demographic and Health Survey (DHS) to explore the prevalence and distribution of child malnutrition across the country. Rather than focusing only on national estimates, I wanted to understand how outcomes differ across regions, urban and rural communities, household wealth levels, maternal education groups, and child age categories.

The goal of this analysis is not to explain why malnutrition occurs, but to build a clearer picture of where it is most concentrated and identify patterns that may warrant further investigation.

## Why This Matters

Child malnutrition affects growth, development, educational outcomes, and long-term health. Understanding where malnutrition is most concentrated can help support more targeted interventions and better-informed public health decisions.

The most interesting part about this dataset was the opportunity to look beyond national averages. National figures can be useful, but they often hide important differences between regions and population groups. Exploring those differences was the main motivation for this analysis.

## Dataset

- Source: 2024 Nigeria Demographic and Health Survey, Children's Recode
- Conducted by: National Population Commission (NPC) Nigeria and ICF International
- Children measured: 9,528 (from 27,783 total records)
- Age group: Children under 5 years
- Access: dhsprogram.com (free registration required)

See `data/about_dataset.md` for full dataset documentation.

## Tools Used

- Python
- pandas
- NumPy
- matplotlib
- pyreadstat (for reading Stata DHS files)

## Repository Structure
child-malnutrition-nigeria/
│
├── data/
│   └── about_dataset.md
├── notebooks/
│   └── malnutrition_analysis.py
├── visuals/
│   ├── national_prevalence.png
│   ├── prevalence_by_region.png
│   ├── prevalence_by_residence.png
│   ├── prevalence_by_wealth.png
│   ├── prevalence_by_education.png
│   └── prevalence_by_age.png
└── README.md

## Key Findings

### National Prevalence

Among children under five measured in the 2024 Nigeria DHS:

- Stunting (chronic malnutrition): 36.6%
- Wasting (acute malnutrition): 24.9%
- Underweight: 8.3%

The wasting rate of 24.9% is particularly concerning. WHO classifies
wasting above 15% as a serious public health emergency. Nigeria's 2024 figure significantly exceeds that threshold. This raised further questions about how nutritional outcomes vary across regions and socioeconomic groups.

### Regional Inequality

Malnutrition is not distributed evenly across Nigeria.

Children living in the North West and North East experience substantially higher levels of stunting and wasting than children in the southern regions. In both northern regions, more than half of children measured were classified as stunted.

These differences highlight the importance of looking beyond national averages when assessing public health challenges.

Stunting rates by region:

| Region | Stunting | Wasting | Underweight |
|---|---|---|---|
| North West | 52.1% | 32.6% | 8.2% |
| North East | 52.1% | 34.2% | 8.7% |
| North Central | 35.5% | 20.6% | 6.3% |
| South West | 21.2% | 21.8% | 10.6% |
| South South | 20.0% | 17.9% | 10.6% |
| South East | 19.3% | 15.0% | 7.4% |

### Wealth and Malnutrition

A clear socioeconomic gradient emerged across the analysis.

Children in the poorest households are more than four times as likely
to be stunted as children in the richest households.

| Wealth Quintile | Stunting | Wasting |
|---|---|---|
| Poorest | 54.7% | 37.5% |
| Poorer | 48.3% | 30.1% |
| Middle | 37.2% | 24.3% |
| Richer | 28.2% | 20.3% |
| Richest | 13.1% | 11.0% |

### Maternal Education

Maternal education showed a pattern similar to household wealth.

Children whose mothers had no formal education experienced substantially higher levels of malnutrition than children whose mothers had attained higher education. The findings suggest that educational inequalities and health outcomes remain closely linked.

| Education Level | Stunting | Wasting |
|---|---|---|
| No education | 54.0% | 35.5% |
| Primary | 37.1% | 23.9% |
| Secondary | 27.4% | 20.0% |
| Higher | 13.2% | 9.6% |

### Age Pattern

Stunting increases sharply from age 0 to age 3, peaking at 44.3%,
before declining slightly at age 4. This pattern is consistent with
cumulative growth faltering, where nutritional deficits compound over
time during early childhood.

Underweight follows the opposite trend, declining from 13.1% at age 0
to 4.8% at age 4, which shows how strongly age influenced nutritional outcomes, reinforcing the importance of interventions during the earliest years of life.

### Urban vs Rural

Rural children have higher stunting (44.1% vs 26.4%) and wasting
(28.1% vs 20.5%) than urban children. Underweight shows a slight
reversal, with urban children marginally more affected (9.2% vs 7.7%),
which may suggest persistent differences in living conditions, access to services, and socioeconomic circumstances between rural and urban communities.

## Limitations

- Anthropometric measurements were available for approximately 34% of children in the dataset. Children without measurements may differ systematically from those included in the analysis.
- The DHS uses a cross-sectional survey design, meaning observed relationships should not be interpreted as causal.
- Household wealth and maternal education are closely related, making it difficult to isolate the independent contribution of either factor.
- State-level analysis was not conducted in this version of the project. Regional estimates may conceal important within-region variation.

## Future Directions

This project focuses on descriptive analysis. Future work could explore:

- State-level malnutrition patterns.
- Geographic visualisation of nutritional outcomes.
- Statistical modelling of malnutrition risk factors.
- Machine learning approaches for risk prediction.
- Links between nutrition, maternal characteristics, and healthcare access.

## How to Reproduce

1. Register at dhsprogram.com and request access to the 2024 Nigeria DHS Children's Recode (Stata format)
2. Place the file at `data/raw/NGKR8BFL.dta`
3. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install pandas numpy matplotlib pyreadstat
```

5. Run the analysis:

```bash
python notebooks/malnutrition_analysis.py
```

## Author

Faith Olaniyi, LAUTECH Nigeria
GitHub: github.com/faithopia21
LinkedIn: linkedin.com/in/faith-oluwanifemi-olaniyi/

## About the Author

Faith Olaniyi is a Computer Science graduate with interests in healthcare analytics, public health data, machine learning, and AI applications in healthcare. She is currently building research and technical experience through health-focused data science projects while preparing for graduate studies in Data Science and Artificial Intelligence.
