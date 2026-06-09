# Dataset Information

## Source

2024 Nigeria Demographic and Health Survey (NDHS), Children's Recode file.

Conducted by the National Population Commission (NPC) Nigeria and ICF International.
Funded by the United States Agency for International Development (USAID).

Access via: https://dhsprogram.com

File used: NGKR8BFL.dta (Stata format)

## Important Note on Data Access

This dataset is licensed and not publicly available without registration.
Access requires a free account at dhsprogram.com and project approval.
The raw data file is not included in this repository for that reason.

To replicate this analysis, apply for access at dhsprogram.com,
request the 2024 Nigeria DHS Children's Recode (Stata format),
and place the file at data/raw/NGKR8BFL.dta.

## Survey Description

The Nigeria DHS is a nationally representative household survey
conducted periodically to collect data on population, health, and nutrition.
The 2024 survey is the most recent available.

The Children's Recode contains one record per child born in the
five years preceding the survey, with data on nutrition, vaccination,
illness, and household characteristics.

## Why This Dataset Was Chosen

The Nigeria Demographic and Health Survey (DHS) is one of the most widely used sources of population, health, and nutrition data in low- and middle-income countries. I selected this dataset because it provides nationally representative information on child health, nutrition, household characteristics, and maternal factors, making it well suited for exploring public health questions related to child malnutrition in Nigeria.

Its breadth and geographic coverage also make it possible to examine how health outcomes differ across regions and population groups, which aligns with my broader interest in healthcare analytics and evidence-based public health decision-making.

## Key Variables Used

| Variable | DHS Code | Description |
|---|---|---|
| Stunting Z-score | hw70 | Height-for-age Z-score (x100) |
| Wasting Z-score | hw71 | Weight-for-height Z-score (x100) |
| Underweight Z-score | hw72 | Weight-for-age Z-score (x100) |
| Region | v024 | Six geopolitical zones |
| Residence | v025 | Urban or rural |
| Wealth index | v190 | Household wealth quintile |
| Child sex | b4 | Male or female |
| Child age | b8 | Age in completed years |
| Mother's education | v106 | Highest education level attained |

## Sample

- Total records: 27,783 children
- Children with anthropometric measurements: 9,528
- Age range: 0 to 4 years (children under 5)
- Coverage: All 6 geopolitical zones of Nigeria

## Data Quality Notes

Z-scores in DHS are stored as integers multiplied by 100.
Values were divided by 100 to convert to standard Z-score format.

WHO plausibility ranges were applied to exclude implausible values:
- Height-for-age: -6 to +6
- Weight-for-height: -5 to +5
- Weight-for-age: -6 to +5

Children flagged as implausible cases in the original dataset
were excluded via pd.to_numeric with errors set to coerce.

Malnutrition was defined using the WHO standard threshold:
Z-score below -2 standard deviations = malnourished.