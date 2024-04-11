# Welcome to the TACOS：Transform brAin COnnectomes across atlaSes
## What is this？
TACOS could convert network-based t-statistics derived from structural and functional connectomes from one atlas(referred to the source atlas) to another(target atlas), specifically Desikan-Killiany (DK) atlas (N = 68), a  114-region subdivision of the DK atlas (DK114; N = 114) and a 219-region subdivision of the same DK  atlas (DK219; N = 219), the Brainnetome (BN) atlas (N = 210), the HCP-MMP atlas (N = 360), the Schaefer 200 atlas (N = 200), the aal atlas (N = 82), the arslan atlas (N = 50), the baldassano atlas (N = 170), the Brodmann atlas (N = 78), the economo atlas (N = 86), the ica atlas (N = 168), the nspn500 atlas (N = 308), the power atlas (N = 130), and the shen atlas (N = 200). 
## Installation
### Python
TACOS has the following dependencies:

- **python >= 3.9**
- **numpy>=1.21.5**
- **scipy>=1.9.1**
- **matplotlib>=3.5.2**

TACOS can be directly downloaded from Github as follows:
```
https://github.com/CAIMI-WEIGroup/TACOS.git
cd TACOS
python setup.py install
```
### Matlab
TACOS has the following dependencies:

- **python >= 3.9**
- **numpy>=1.21.5**
- **scipy>=1.9.1**
- **matplotlib>=3.5.2**

TACOS can be directly downloaded from Github as follows:
```
https://github.com/CAIMI-WEIGroup/TACOS.git
cd TACOS
python setup.py install
```
## Start to use TACOS
### How to Use convertStatistics Function
After successfully downloading and installing the TACOS toolkit, you can use the convertStatistics function to transform source atlas t-statistics to target atlas t-statistics. This function allowed you to specify paths to your data files and select the appropriate atlases and transformation form. The transformed t-statistics matrix in the target atlas and will be saved as '.csv' in current directory.
### Usage
To call the convertStatistics function, follow the template below in your Python script:
```
from TACOS import convertStatistics

convertStatistics(
    sourceT_Path='path/to/your/source_t_statistics.csv',
    source_Atlas='SourceAtlasName',
    target_Atlas='TargetAtlasName',
    form='transformationForm',
    controlS_Path='path/to/your/control_group_variance.csv',
    patientS_Path='path/to/your/patient_group_variance.csv'
)
```
Or in your Matlab script:
```
convertStatistics(
    sourceT_Path='path/to/your/source_t_statistics.csv',
    source_Atlas='SourceAtlasName',
    target_Atlas='TargetAtlasName',
    form='transformationForm',
    controlS_Path='path/to/your/control_group_variance.csv',
    patientS_Path='path/to/your/patient_group_variance.csv'
)
```
Replace the paths and parameters with those relevant to your data and analysis needs. Below are descriptions for each parameter:
- **sourceT_Path (required)**: Path to the CSV file containing source t-statistics.
- **source_Atlas (required)**: Name of the source atlas. Please ensure it aligns with one of the supported atlases by TACOS.
- **target_Atlas (required)**: Name of the target atlas. Make sure to choose from the atlases supported by TACOS.
- **form (required)**: Specifies whether the transformation is 'functional' or 'structural'.
- **controlS_Path (optional)**: Path to the CSV file containing control group variance matrix. If not provided, a default variance matrix derived from the HCP dataset will be used.
- **patientS_Path (optional)**: Path to the CSV file containing patient group variance matrix. Similarly, if not provided, a default variance matrix from the HCP dataset will be used.

Beloe are the source and target atlases supported by TACOS:
- **target_Atlas**: ['aal', 'DK114', 'Schaefer200', 'HCP_MMP']
- **source_Atlas**: ['aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK',  'DK219', 'BN', 'arslan', 'baldassano', 'Brodmann', 'economo', 'ica', 'nspn500', 'power', 'shen', 'Schaefer300', 'Schaefer400']
### Important Notes
Before calling the convertStatistics function, ensure that the brain region order in your source t-statistics aligns with the TACOS-provided brain region order for the specified source atlas. Failing to align the brain region order could result in incorrect analysis outcomes. For the specific brain region order, please see the [TACOS/Python/TACOS/resources/region_order](Python/TACOS/resources/region_order).
## Resource
To enhance your experience with TACOS and ensure successful analyses, we have compiled a list of resources that you might find helpful:
- **TACOS Documentation**: Comprehensive guide and reference for using TACOS. [View Documentation](README.md).
- **Supported Atlases and Region orders**: A detailed list of all brain atlases that TACOS supports, including their brain region orders. [View Supported Atlases](Python/TACOS/resources/region_order).
- **Default Variance Matrix**:  The default variance matrix from the HCP dataset in atlases supported by TACOS.[Default Variance Matrix](Python/TACOS/resources/region_order/default_variance).
- **Source Code**: Explore the TACOS source code for a deeper understanding of the tool. [View in Python](Python/TACOS). [View in Matlab](Matlab/TACOS).
- **Citing TACOS**: If you use TACOS in your research, please consider citing it. [Citation Information](#).
For any additional information or support, feel free to contact us at [yongbin.wei@bupt.edu.cn](yongbin.wei@bupt.edu.cn).
## Licence
This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License - see the [LICENSE.txt](LICENSE.txt) file for details.