You must run the initiation file in order to have a base of employees and jobs to begin with. Also, must have jpg files and employees.pickle file in the same directory as employ_easy. Then simply run employ_easy.

Steps for first use. General use, ignore first 2 steps:

1. Run `python3 initiation_file.py`
2. Initialize by pressing y then Enter
3. Run `python3 employ_easy_1.1.py` to see GUI
4. Edit inputs / worker jobs to your liking
5. Click on Generate Job Placement when you are ready to export to CSV
6. Schedule.csv file will be created (without notifying you :/ ) in the same directory.

Optional Step:

7. Open Schedule.csv and verify that workers can do jobs
8. Verify that the workers don't do the same jobs two time segments in a row (there can be some overlap if absolutely necessary)


GUI Reference:

Click on a worker's job to change their capabilities:

Green   - Worker can do job / is a candidate to be assigned to this job
Yellow  - Worker is training ( will not be automatically assigned to job; requires manual review )
Red     - Worker cannot do job