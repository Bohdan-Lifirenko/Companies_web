**Створити середовище:**
````
conda env create -f environment.yml
````

**Активувати:**
````
conda activate companies_web
````

**Перевірити середовище:**
````
conda env list
````

**Запустити проект:**
````
python src/app.py
````
Додатково:
1) Переконайся, де встановлена Conda
2) Додай Conda в PATH
```
C:\Users\...\miniconda3
C:\Users\...\miniconda3\Scripts
C:\Users\...\miniconda3\condabin
```
3) В cmd перевірити:
```
 conda --version
```

**При проблемах з встановленням середовища, видаліть файли environment.yml, requirements.txt.**
