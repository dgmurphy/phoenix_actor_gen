# Phoenix Actor Generator
This is the OEDA Phoenix Pipeline configured to run in Null Actors mode and to generate the actor labels.

### Setup

```git clone https://github.com/dgmurphy/phoenix_pipeline.git```

### Create Python Environment & Install libraries

Create a Python2 virtual environment:

```virtualenv -p /usr/bin/python2.7 venv```

Activate the virtual environment:

```source venv/bin/activate```


### Install Python Libraries

```pip install -r requirements.txt```


## Usage

### Edit the Config File

The pipeline will process events on a per-day basis by checking the date fields of the stories in MongoDB.
To process events for a particular day we need to specify that day in the config file.


In the file `PHOX_config.ini` :

`run_date = 20200713`

NOTE: To process events on the same day they were collected, set the run_date to today's date plus one day.

### Run

```python actor_gen.py```


The actpr generator should produce an actor labels file e.g.

`nullactors.events_null_actors_mode_20200713.txt`

Sample output:

```
{
"id": "5f0bba04bab220237cf581eb",
"sentence": "Mr Elkana, in a statement on Sunday, said the two robbery suspects usually attack motorists held in traffic and collect their belongings in some parts of Lagos. ",
"source": "Mr Elkana",
"target": "the ... robbery suspects",
"evtcode": "112",
"evttext": "said <and> ... attack",
}
```