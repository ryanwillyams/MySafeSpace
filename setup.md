## Setup


#### 1. Setup Environment
If you have not made a python virtual environment you can do so with the command  
```python3 -m venv .venv```  
**If you make your venv another name make sure not to push it to the repo or add it to the .gitignore**  
Learn more about virtual environments [here](https://docs.python.org/3/library/venv.html)  

In order to start the venv you need to run the activate script  
In Bash the command is:  
```source .venv/bin/activate```  
You will know it worked if to the left of your terminal there is `(.venv)`  


#### 2. Installing dependecies 
Next you will need to install all the dependencies of the app.
Make sure you are in the venv and run
```pip install -r requirements.txt```


#### 3. Starting the interface
Now to actually run the application
```python3 app.py```



## Build  
To build the applcation, ensure you have [pyinstaller](https://pyinstaller.org/en/stable/installation.html) in the venv  

#### Building the executable

Whatever type of machine you are on is the one pyinstaller will create an executable for  
For example, if you are on a 64-bit Ubuntu 22.04 machine it will create an executable for that  

To build the file, run:  
`pyinstaller main.spec` 

#### Running the build

To run the build run:  

`dist/main/main`
