# Welcome to the TACOS
## What is TACOS？
TACOS (Transform brAin COnnectomes across atlaSes) is a toolbox that converts network-based statistics from structural and functional brain connectomes across different atlases. Specifically, network-based t values (usually derived from group comparisons in case-control connectomic studies) are converted from one atlas (referred to as the source atlas) to another (referred to as the target atlas). A series of commonly used atlases are currently available in TACOS, including but not limited to the Desikan-Killiany atlas, the Schaefer atlas, the HCP-MMP atlas, the Brainnetome atlas, and the AAL atlas (see below a full list of 17 included atlases). TACOS is available in Python and MATLAB. 

## Installation
### Python
TACOS has the following dependencies:

- **python >= 3.9**
- **numpy>=1.21.5**
- **scipy>=1.9.1**
- **matplotlib>=3.5.2**

TACOS can be directly downloaded from Github as follows:
```
git clone https://github.com/CAIMI-WEIGroup/TACOS.git
cd TACOS
python setup.py install
```

### Matlab
TACOS can be directly downloaded from Github as follows:
```
git clone https://github.com/CAIMI-WEIGroup/TACOS.git
```
Start MATLAB and navigate to the directory containing the `installation.m` script:
```matlab
cd 'TOOLBOX_DIRECTORY'
```
Replace `TOOLBOX_DIRECTORY` with the actual directory where the TACOS Toolbox has been downloaded.
Run the `installation.m` script to set up the toolbox:
```matlab
installation
```
This will add the necessary paths to MATLAB's search path and set up any required resources.

## Start to use TACOS
### The convertStatistics function
After successfully downloaded and installed TACOS, you can use the convertStatistics function to transform network-based t-statistics from a source atlas to a target atlas. This function allows you to specify directories to your data files and select the appropriate atlases and transformation form. The transformed t-statistics matrix in the target atlas will be saved as a '.csv' file.

### Python Usage
To call the convertStatistics function, follow the template below in your Python script:
```
from TACOS import convertStatistics

transformed_tval = convertStatistics(
    source_tval='SOURCE_T_STATISTICS_FILE',
    source_atlas='SOURCE_ATLAS_NAME',
    target_atlas='TARGET_ATLAS_NAME',
    type='CONNECTIVITY_TYPE',
)
```

Parameter:
- **source_tval (required)**: A .csv file containing a t-value matrix from the source atlas.
- **source_atlas (required)**: Name of the source atlas. Currently available: 'aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK',  'DK219', 'BN', 'arslan', 'baldassano', 'Brodmann', 'economo', 'ica', 'nspn500', 'power', 'shen', 'Schaefer300', 'Schaefer400'
- **target_atlas (required)**: Name of the target atlas. Currently available: 'aal', 'DK114', 'Schaefer200', 'HCP_MMP'
- **type (required)**: Connectivity type:  'functional' for functional connectivity; 'structural' for structural connectivity.

Notably, the estimated group variance maps from the HCP data are used here (for details, see Liu et al., 2024). You can also use your own group variance maps to achieve a more accurate mapping.
You can specify whether to save the transformed t-values as a CSV file by using `save_transformed_tval`, and whether to display the transformed t-values as an SVG file by using `display_transformed_tval`.

```
from TACOS import convertStatistics

transformed_tval = convertStatistics(
    source_tval='SOURCE_T_STATISTICS_FILE',
    source_atlas='SOURCE_ATLAS_NAME',
    target_atlas='TARGET_ATLAS_NAME',
    type='CONNECTIVITY_TYPE',
    variance_group1='GROUP1_VARIANCE_FILE',
    variance_group2='GROUP2_VARIANCE_FILE',
    save_transformed_tval=True,
    display_transformed_tval=True
)
```

- **variance_group1 (optional)**: A .csv file containing the variance matrix of group 1. If not provided, a default variance matrix derived from the HCP dataset will be used.
- **variance_group2 (optional)**: A .csv file containing the variance matrix of group 2. If not provided, a default variance matrix derived from the HCP dataset will be used.
- **save_transformed_tval (optional)**: Whether to store the transformed tval as csv, acceptable value is `True` or `False`. defaults to `False` if not provided.
- **display_transformed_tval (optional)**: Whether to display the transformed tval as svg, acceptable value is `True` or `False`, defaults to `False` if not provided.

### MATLAB Usage
The above function is also avaible in MATLAB:

```
transformed_tval = convertStatistics(...
    'source_tval', 'SOURCE_T_STATISTICS_FILE', ...
    'source_atlas', 'SOURCE_ATLAS_NAME', ...
    'target_atlas', 'TARGET_ATLAS_NAME', ...
    'type', 'CONNECTIVITY_TYPE', ...
);
```
You can optionally use custom variance maps, save the `transformed_tval` as a CSV file, and display it, based on your requirements.

```
transformed_tval = convertStatistics(...
    'source_tval', 'SOURCE_T_STATISTICS_FILE', ...
    'source_atlas', 'SOURCE_ATLAS_NAME', ...
    'target_atlas', 'TARGET_ATLAS_NAME', ...
    'type', 'CONNECTIVITY_TYPE', ...
    'variance_group1', 'GROUP1_VARIANCE_FILE', ...
    'variance_group2', 'GROUP2_VARIANCE_FILE', ...
    'save_transformed_tval', true, ...
    'display_transformed_tval', true, ...
);
```

### Important Notes
Before calling the convertStatistics function, ensure that the brain region order in your source t-statistics aligns with the TACOS-provided brain region order for the specified source atlas. Failing to align the brain region order could result in incorrect analysis outcomes. For the specific brain region order, please see the [TACOS/region_order](region_order).

### Examples
Example scripts are available for both Python and Matlab. Please find details in [examples.py](example/examples.py) and [examples.m](example/examples.m).

## Resource
To enhance your experience with TACOS and ensure successful analyses, we have compiled a list of resources that you might find helpful:

- **Currently included atlases**: The Desikan-Killiany (DK) atlas (N = 68), the 114-region subdivision of the DK atlas (Lausanne DK-114; N = 114), the 219-region subdivision of the DK  atlas (Lausanne DK219; N = 219), the Brainnetome (BN) atlas (N = 210), the HCP-MMP atlas (N = 360), the Schaefer 200 atlas (N = 200), the AAL atlas (N = 82), the arslan atlas (N = 50), the baldassano atlas (N = 170), the Brodmann atlas (N = 78), the economo atlas (N = 86), the ica atlas (N = 168), the nspn500 atlas (N = 308), the power atlas (N = 130), and the shen atlas (N = 200). 
- **TACOS Documentation**: Comprehensive guide and reference for using TACOS. [View Documentation](README.md).
- **Supported Atlases and Region orders**: A detailed list of all brain atlases that TACOS supports, including their brain region orders. [View Supported Atlases](Python/TACOS/resources/region_order).
- **Default Variance Matrix**:  The default variance matrix from the HCP dataset in atlases supported by TACOS.[Default Variance Matrix](Python/TACOS/resources/default_variance).
- **Source Code**: Explore the TACOS source code for a deeper understanding of the tool. [View in Python](Python/TACOS). [View in Matlab](Matlab/TACOS).
- **Citing TACOS**: If you use TACOS in your research, please consider citing it. [Citation Information](Liu et al., 2024).
For any additional information or support, feel free to contact us at [yongbin.wei@bupt.edu.cn](yongbin.wei@bupt.edu.cn).
## Licence
This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License - see the [LICENSE.txt](LICENSE.txt) file for details.