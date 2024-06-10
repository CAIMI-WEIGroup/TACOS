# Example file: How to use TACOS to transform t-values from DK219 to DK114 atlas

# This example demonstrates how to use the TACOS toolbox to transform t-values from the DK219 atlas to the DK114 atlas.
# The t-values and variance matrix for the DK219 atlas are stored in 'TACOS/example'.

from TACOS import convertStatistics

# Example 1: Using estimated group variance maps from the HCP data
'''
transformed_tval = convertStatistics(
    source_tval='SOURCE_T_STATISTICS_FILE',
    source_atlas='SOURCE_ATLAS_NAME',
    target_atlas='TARGET_ATLAS_NAME',
    type='CONNECTIVITY_TYPE',
)
'''

# Example 2: Using your own group variance maps, saving the transformed t-values as a CSV file, and displaying it
transformed_tval = convertStatistics(
    source_tval='DK219_SOURCE_T_STATISTICS_FILE.csv',
    source_atlas='DK219',
    target_atlas='DK114',
    type='functional',
    variance_group1='DK219_GROUP1_VARIANCE_FILE.csv',
    variance_group2='DK219_GROUP2_VARIANCE_FILE.csv',
    save_transformed_tval=True,
    display_transformed_tval=True
)
