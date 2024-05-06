# Welcome to the TACOS
## What is TACOS？
TACOS (Transform brAin COnnectomes across atlaSes) is a toolbox that converts network-based statistics from structural and functional brain connectomes across different atlases. Specifically, network-based t values (usually derived from group comparisons in case-control connectomic studies) are converted from one atlas (referred to as the source atlas) to another (referred to as the target atlas). A series of commonly used atlases are currently available in TACOS, including but not limited to the Desikan-Killiany atlas, the HCP-MMP atlas, the Brainnetome atlas, the Schaefer atlas, and the AAL atlas (see below a full list of 17 included atlases). TACOS is available in Python and MATLAB. 

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
Navigate to the directory containing the `installToolbox.m` script:
```matlab
cd 'PATH_TO_TACOS'
```
Replace `PATH_TO_TACOS` with the actual path where the TACOS Toolbox has been downloaded on your system.
Run the `installToolbox.m` script to set up the toolbox:
```matlab
installToolbox
```
This will add the necessary paths to MATLAB's search path and set up any required resources.

## Start to use TACOS
### The convertStatistics function
After successfully downloaded and installed TACOS, you can use the convertStatistics function to transform network-based t-statistics from a source atlas to a target atlas. This function allows you to specify paths to your data files and select the appropriate atlases and transformation form. The transformed t-statistics matrix in the target atlas will be saved as a '.csv' file.

### Usage
To call the convertStatistics function, follow the template below in your Python script:
```
from TACOS import convertStatistics

convertStatistics(
    sourceT_Path='PATH/TO/YOUR/SOURCE_T_STATISTICS.csv',
    source_Atlas='SourceAtlasName',
    target_Atlas='TargetAtlasName',
    form='transformationForm',
)
```

Parameter:
- **sourceT_Path (required)**: Path to the CSV file containing a t-value matrix in the source atlas.
- **source_Atlas (required)**: Name of the source atlas. Currently available: 'aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK',  'DK219', 'BN', 'arslan', 'baldassano', 'Brodmann', 'economo', 'ica', 'nspn500', 'power', 'shen', 'Schaefer300', 'Schaefer400'.
- **target_Atlas (required)**: Name of the target atlas. Currently available: 'aal', 'DK114', 'Schaefer200', 'HCP_MMP'
- **form (required)**: Data type:  'functional' for functional network; 'structural' for structural network.

Notably, the estimated group variance maps are used here (for details, see Liu et al., 2024). You can also use your own group variance maps to achieve a more accurate mapping.

```
from TACOS import convertStatistics

convertStatistics(
    sourceT_Path='PATH/TO/YOUR/SOURCE_T_STATISTICS.csv',
    source_Atlas='SourceAtlasName',
    target_Atlas='TargetAtlasName',
    form='transformationForm',
    controlS_Path='PATH/TO/YOUR/CONTROLS_VARIANCE.csv',
    patientS_Path='PATH/TO/YOUR/PATIENTS_VARIANCE.csv'
)
```

- **controlS_Path (optional)**: Path to the CSV file containing control group variance matrix. If not provided, a default variance matrix derived from the HCP dataset will be used.
- **patientS_Path (optional)**: Path to the CSV file containing patient group variance matrix. Similarly, if not provided, a default variance matrix from the HCP dataset will be used.


The above function is also avaible in MATLAB:

```
convertStatistics(...
    'sourceT_Path', 'PATH/TO/YOUR/SOURCE_T_STATISTICS.csv', ...
    'source_Atlas', 'SourceAtlasName', ...
    'target_Atlas', 'TargetAtlasName', ...
    'form', 'transformationForm', ...
);
```
or when customised variance maps available:

```
convertStatistics(...
    'sourceT_Path', 'PATH/TO/YOUR/SOURCE_T_STATISTICS.csv', ...
    'source_Atlas', 'SourceAtlasName', ...
    'target_Atlas', 'TargetAtlasName', ...
    'form', 'transformationForm', ...
    'controlS_Path', 'PATH/TO/YOUR/CONTROLS_VARIANCE.csv', ...
    'patientS_Path', 'PATH/TO/YOUR/PATIENTS_VARIANCE.csv'
);
```

### Important Notes
Before calling the convertStatistics function, ensure that the brain region order in your source t-statistics aligns with the TACOS-provided brain region order for the specified source atlas. Failing to align the brain region order could result in incorrect analysis outcomes. For the specific brain region order, please see the [region_order](region_order).

## Resource
To enhance your experience with TACOS and ensure successful analyses, we have compiled a list of resources that you might find helpful:

- **Currently included atlases**: The Desikan-Killiany (DK) atlas (N = 68), the 114-region subdivision of the DK atlas (Lausanne DK-114; N = 114), the 219-region subdivision of the DK atlas (Lausanne DK219; N = 219), the Brainnetome (BN) atlas (N = 210), the HCP-MMP atlas (N = 360), the Schaefer200 atlas (N = 200), the aal atlas (N = 82), the arslan atlas (N = 50), the baldassano atlas (N = 170), the Brodmann atlas (N = 78), the economo atlas (N = 86), the ica atlas (N = 168), the nspn500 atlas (N = 308), the power atlas (N = 130), and the shen atlas (N = 200). 
- **TACOS Documentation**: Comprehensive guide and reference for using TACOS. [View Documentation](README.md).
- **Supported Atlases and Region orders**: A detailed list of all brain atlases that TACOS supports, including their brain region orders. [View Supported Atlases](region_order).
- **Default Variance Matrix**:  The default variance matrix from the HCP dataset in atlases supported by TACOS.[Default Variance Matrix](Python/TACOS/resources/default_variance).
- **Source Code**: Explore the TACOS source code for a deeper understanding of the tool. [View in Python](Python/TACOS). [View in Matlab](Matlab/TACOS).
- **Citing TACOS**: If you use TACOS in your research, please consider citing it. [Citation Information](Liu et al., 2024).
For any additional information or support, feel free to contact us at [yongbin.wei@bupt.edu.cn](yongbin.wei@bupt.edu.cn).
## Licence
This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License - see the [LICENSE.txt](LICENSE.txt) file for details.