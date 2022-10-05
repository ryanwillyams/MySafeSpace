## Setup

#### 1. Change Directory
In order to run the graphical interface, we need to first change our directory to the GUI folder.
To do this 
`cd ./GUI`


#### 2. Setup Environment
If you have not made a python virtual environment you can do so with the command  
```python3 -m venv .venv```  
**If you make your venv another name make sure not to push it to the repo or add it to the .gitignore**  
Learn more about virtual environments [here](https://docs.python.org/3/library/venv.html)  

In order to start the venv you need to run the activate script  
In Bash the command is:  
```source .venv/bin/activate```  
You will know it worked if to the left of your terminal there is `(.venv)`  


#### 3. Installing dependecies 
Next you will need to install all the dependencies of the app.
Make sure you are in the venv and run
```pip install -r requirements.txt```


#### 4. Starting the interface
Now to actually run the application
```python3 app.py```