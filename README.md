# popTextureDS
Generating synthetic popTextures

# User instructions

  >> git clone https://github.com/prashanthtr/popTextureDS.git

  >> cd popTextureDS/

  >> conda create -n popTextureDS python=3.8 ipykernel

  >> conda activate popTextureDS

  >> python3 -m pip install -r requirements.txt --src '.'(please run twice - due to numba dependency error)

# Setup and run jupyter notebook

>> pip install jupyter

>> python3 -m ipykernel install --user --name popTextureDS

>> jupyter notebook

>> Select *popTexture-notebook.ipynb* in the browser interface

# Generate files from commandline

>> python3 DSGenerator/generate.py --configfile config_file.json

# Config File descriptions

>> "soundname": "pop_sound",

>> "samplerate": 16000,

>> "numVariations": 2,

>> "soundDuration": 4,

>> "outPath": "pop_sound",

>> "recordFormat": The format of the output parameter records  0 (*paramManager*), 1 (*SonyGan*) and 2 (*Tfrecords*)

>> "paramRange": Normalized(Norm) or Natural(Natural) ranges for parameter interpolation.
	Examples of Interpretations:
	- Norm: Map from 0 to 1 to 400 to 600 in natural range
	- Natural: Map from 400 to 600 to 400 to 600 in natural range
	- Norm: Map from 0 to 1 to 0.4 to 0.6 which is 400 to 600 units in natural range.
	XX: ALl ranges have to be within the synth description
	XX: Use synthInterface to get ranges of current synth parameters.
