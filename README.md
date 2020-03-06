# MAppleT

## Developer - Installation 

We use conda system to manage our dependencies, so first install conda on your machine.

https://docs.conda.io/en/latest/miniconda.html

### Install dependencies and environement

Now, install dependencies of MappleT by create firstly a conda environment with 

```
conda create -y -n mappleT -c openalea -c conda-forge python=2.7 \
scons=2 \
openalea.sconsx \
openalea.plantgl \
openalea.lpy \
boost=1.66.0 \
scipy \
pillow \
nose \
xlrd \
cython
```

##### Activate your environement

```
conda activate mappleT
```

##### Continue dependencies installation with pip install

```
pip install matplotlib
```

##### Continue dependencies installation with openalea noy conda released package

###### Plantik 

```
git clone https://github.com/openalea-incubator/plantik
cd plantik; python setup.py install; cd ..
```
###### MISC

```
git clone https://github.com/openalea/misc
cd misc; python setup.py install; cd ..
```

###### Fractalysis

```
git clone https://github.com/openalea/fractalysis
cd fractalysis; python setup.py install; cd ..
```

###### Structure Analysis

```
git clone https://github.com/openalea/StructureAnalysis/
cd StructureAnalysis/
git checkout 59332198b74380f67df0f8e7dff3be36fb1785e2
cd tool; python setup.py install; cd ..
cd stat_tool; python setup.py install; cd ..
cd sequence_analysis; python setup.py install; cd ..
cd ..
```

### And finally ... Install MappleT !

```
git clone https://github.com/openalea-incubator/MAppleT
cd MAppleT
python setup.py develop
```

