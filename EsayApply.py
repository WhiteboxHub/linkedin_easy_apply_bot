from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import yaml
import random
from bs4 import BeautifulSoup 
from selenium.webdriver.support.ui import WebDriverWait
import csv
import re
from datetime import datetime,timedelta
from pathlib import Path
import pandas as pd
from ChoseCandidate import chooseCandidate,getFull_path_Resume
from postioin_role import UI_roles,ML_roles,QA_roles
from test import main as mymain_brower
#importing the config values form config.yaml
def Main():

    fileLocation = chooseCandidate()
    with open(fileLocation,'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc
    assert len(parameters['positions']) > 0
    assert len(parameters['locations']) > 0
    assert parameters['username'] is not None
    assert parameters['password'] is not None
    assert parameters['phone_number'] is not None
    username = parameters['username']
    password = parameters['password']
    phonenumber = parameters['phone_number']
    locations = [l for l in parameters['locations'] if l is not None]
    role_type = parameters['role_type']
    if role_type == 'ML':
        positions = ML_roles
    elif role_type == "QA":
        positions = QA_roles
    elif role_type == "UI":
        positions = UI_roles


    blacklist = parameters.get('blacklist',[])
    blacklisttitles = parameters.get('blackListTitles',[])
    uploads = {} if parameters.get('uploads', {}) is None else parameters.get('uploads', {})
    outputfilename = f"Output/Output_of_{parameters['username']}.csv"
    experiencelevel = parameters.get('experience_level',[])
    rate = parameters['rate']
    salary = parameters['salary']
    roletype = parameters.get('roletype',[])
    gender = parameters['gender']
    for key in uploads.keys():
        assert uploads[key] is not None
    
    ApplyBot(username=username,
             password=password,
             phonenumber=phonenumber
             ,locations=locations,
             salary=salary,
             uploads=uploads,
             blacklist=blacklist,
             blacklisttitles=blacklisttitles,
             experiencelevel=experiencelevel,
             positions=positions,
             rate=rate,
             roletype=roletype,gender=gender,filename=outputfilename)
    

class ApplyBot():
    def __init__(self,
                 username,
                 password,
                 phonenumber,gender,
                 salary,rate,filename,uploads={},
                 blacklist=[],blacklisttitles=[],experiencelevel=[],locations=[],positions= [],roletype=[]):
        self.username = username          
        self.password = password
        self.phonenumber = phonenumber
        self.salary = salary
        self.rate = rate
        self.uploads = uploads
        self.resume_path = getFull_path_Resume(uploads["Resume"])
        self.roletype = roletype
        self.filename = filename
        self.blacklist = blacklist
        self.blacklisttitles = blacklisttitles
        self.experiencelevel = experiencelevel
        self.locations=locations
        self.positions=positions
        # self.browser =  webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.browser =  mymain_brower()
        self.wait= WebDriverWait(self.browser,30)
        self.gender = gender
        self.qa_file = Path(f"Qa/qa_{self.username}.csv")
        self.answer = {}

        if self.qa_file.is_file():
            df = pd.read_csv(self.qa_file)
            for index,row in df.iterrows():
                self.answer[row['Question']]= row["Answer"]
        else:
            df = pd.DataFrame(columns=["Question","Answer"])
            df.to_csv(self.qa_file,index=False,encoding='utf-8')

        self.locator = {
            "next": (By.CSS_SELECTOR, "button[aria-label='Continue to next step']"),
            "review": (By.CSS_SELECTOR, "button[aria-label='Review your application']"),
            "submit": (By.CSS_SELECTOR, "button[aria-label='Submit application']"),
            "error": (By.CLASS_NAME, "artdeco-inline-feedback__message"),
            "upload_resume": (By.XPATH, "//*[contains(@id, 'jobs-document-upload-file-input-upload-resume')]"),
            "upload_cv": (By.XPATH, "//*[contains(@id, 'jobs-document-upload-file-input-upload-cover-letter')]"),
            "follow": (By.CSS_SELECTOR, "label[for='follow-company-checkbox']"),
            "upload": (By.NAME, "file"),
            "search": (By.CLASS_NAME, "jobs-search-results-list"),
            "links": ("xpath", '//div[@data-job-id]'),
            "fields": (By.CLASS_NAME, "jobs-easy-apply-form-section__grouping"),
            "radio_select": (By.CSS_SELECTOR, "input[type='radio']"), #need to append [value={}].format(answer)
            "multi_select": (By.XPATH, "//*[contains(@id, 'text-entity-list-form-component')]"),
            "text_select": (By.CLASS_NAME, "artdeco-text-input--input"),
            "2fa_oneClick": (By.ID, 'reset-password-submit-button'),
            "easy_apply_button": (By.XPATH, '//button[contains(@class, "jobs-apply-button")]')

        }
        print(f"--------------------------the Candidate Selected for Marketing is {self.username}------------------------------")
        print(f'{self.phonenumber}\n')
        print(f'{self.salary}\n')
        print(f'{self.uploads}\n')
        print(f'{self.experiencelevel}\n')
        print(f'{self.locations}\n')
        print(f'{self.positions}\n')
        print('Linkedin Login is initiated')
        self.login_linkedin()
        

    def login_linkedin(self):
        self.browser.get('https://www.linkedin.com/login')
        self.sleep(8)
        try:
            self.browser.find_element(By.ID, 'username').clear()
            self.browser.find_element(By.ID, 'username').send_keys(self.username)
            self.browser.find_element(By.ID, 'password').clear()
            self.browser.find_element(By.ID, 'password').send_keys(self.password)
            self.browser.find_element(By.XPATH, "//button[@type='submit']").click()
            #sleeping for the page to load 
            self.sleep(10)
        except NoSuchElementException:
            print("Already logged in.Ski[pping login....")
        self.findingCombos_postion_location()

    def sleep(self,sleeptime =random.randrange(3,6) ):
        #this function will sleep for a random amount of time between 0 - 5sec
        randomtime = sleeptime
        print(f"Application is sleeping for a random time of {randomtime} seconds")
        time.sleep(randomtime)
    
    def fill_data(self) -> None:
        self.browser.set_window_size(1, 1)
        self.browser.set_window_position(2000, 2000)

    def roletypestr_convertion(self):
        rolearr = self.roletype
        if rolearr==[]:
            return ""
        elif rolearr ==[1] or rolearr==[2] or rolearr==[3]:
            return f"&f_WT={str(rolearr[0])}"
        elif rolearr == [1,2]:
            return "&f_WT=1%2C3"
        elif rolearr == [1,3]:
            return "&f_WT=1%2C2"
        elif rolearr == [2,3]:
            return "&f_WT=3%2C2"
        elif rolearr == [1,2,3]:
            return "&f_WT=1%2C3%2C2"
    def findingCombos_postion_location(self):
        combolist : list = []
        while len(combolist)<len(self.positions)*len(self.locations):
            for i in self.positions:
                for j in self.locations:
                    combo: tuple = (i,j)
                    combolist.append(combo)
                    self.Get_job_application_page(position=i,location=j)
        
    def Get_job_application_page(self,location,position):
        # construct the experience level part of URL
        exp_lvl_str = ",".join(map(str,self.experiencelevel)) if self.experiencelevel else ""
        exp_lvl_param = f"&f_E={exp_lvl_str}" if exp_lvl_str else ""
        location_str = f"&location={location}"
        position_str = f"&keywords={position}"
        Job_per_page = 0
        self.sleep()
        rolestring = self.roletypestr_convertion()
        print(f"Searching for the location= {location} and job = {position} ")
        URL = "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords="+position_str+str(rolestring)+location_str+exp_lvl_param+"&start="+str(Job_per_page)
        self.browser.get(URL)
        #sleeping for 10 sec for page load
        self.sleep(10)
        try:
            print('--try here----'*20)
            # self.sleep(200)
            count_xpath = '//*[@id="main"]/div/div[2]/div[1]/header/div[1]/div/small/div/span'
            TotalresultsFound = self.browser.find_element(By.XPATH,count_xpath)
            print('--try here 1111----'*20)

            self.sleep(2)
            resultsFoundnumber = ''.join(re.findall(r'\d',TotalresultsFound.text))
            print('--try her 222e----'*20)

            Job_Search_Results_count = int(resultsFoundnumber)
        except Exception as e:
            print('--Except -- here----'*200)

            Job_Search_Results_count = 0
        print(f"-----------------------This is the total count fo the results that can be get --{Job_Search_Results_count}----------------------------------------------------")
        while Job_per_page<Job_Search_Results_count:
            print("")
            URL = "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords="+position_str+rolestring+location_str+exp_lvl_param+"&start="+str(Job_per_page)
            self.browser.get(URL)
            self.sleep()
            self.Load_page_Scroll_page()
            if self.is_present(self.locator["search"]):
                scrollresult = self.get_elements("search")
                for i in range(300,3000,100):
                    self.browser.execute_script("arguments[0].scrollTo(0, {})".format(i), scrollresult[0])
                scrollresult = self.get_elements("search")
                self.sleep(1)


            if self.is_present(self.locator["links"]):
                links = self.get_elements("links")
                # links = self.browser.find_elements("xpath",
                #     '//div[@data-job-id]'
                # )

                jobIDs = {} #{Job id: processed_status}
            
                # children selector is the container of the job cards on the left
                for link in links:
                        print(f"the link.text is {link.text}")
                        if 'Applied' not in link.text: #checking if applied already
                            if link.text not in self.blacklist: #checking if blacklisted
                                jobID = link.get_attribute("data-job-id")
                                if jobID == "search":
                                    print("Job ID not found, search keyword found instead? {}")
                                    continue
                                else:
                                    jobIDs[jobID] = "To be processed"
                if len(jobIDs) > 0:
                    self.job_apply_loop(jobIDs)
            Job_per_page+=25
        return
    def job_apply_loop(self,jobIDS):
        for jobID in jobIDS:
            if jobIDS[jobID] == "To be processed":
                try:
                    applied = self.Start_applying_with_jobid(jobID)
                except Exception as e:
                    print(e)
                    continue

    def Start_applying_with_jobid(self,jobid):
        #navigating to the job page with the help of jobID 
        self.Get_Job_page_with_jobid(jobid)

        self.sleep(4)
        #find the easy apply  button in the page

        button = self.get_easy_apply_button()

        #word filter to skip positions not wanted

        if button is not False:
            if any(word in self.browser.title for word in self.blacklisttitles):
                print('skipping this application, a blacklisted keyword was found in the job position')
                string_easy = "* Contains blacklisted keyword"
                result = False
            else:
                string_easy = "* has Easy Apply Button"
                print("Found Easy Apply button and clicking the button")
                self.sleep(1)
                button.click()
                clicked = True
                self.sleep(2)
                self.fill_out_fields()
                result : bool = self.send_resume()

                if result:
                    string_easy= '*Applied : Sent the Resume'
                else:
                    string_easy= '*Did not apply: Faild to send Resume'
        elif "You applied on" in self.browser.page_source:
            print("You have already applied to this position.")
            string_easy = "* Already Applied"
            result = False
        else:
            print("The Easy apply button does not exist.")
            string_easy = "* Doesn't have Easy Apply Button"
            result = False
        print(f"\nPosition {jobid}:\n {self.browser.title} \n {string_easy} \n")

        self.write_to_file(button, jobid, self.browser.title, result)
        return result

    def write_to_file(self, button, jobID, browserTitle, result) -> None:
        def re_extract(text, pattern):
            target = re.search(pattern, text)
            if target:
                target = target.group(1)
            return target

        timestamp: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        attempted: bool = False if button == False else True
        job = re_extract(browserTitle.split(' | ')[0], r"\(?\d?\)?\s?(\w.*)")
        company = re_extract(browserTitle.split(' | ')[1], r"(\w.*)")

        toWrite: list = [timestamp, jobID, job, company, attempted, result]
        with open(self.filename, 'a+') as f:
            writer = csv.writer(f)
            writer.writerow(toWrite)

    def Get_Job_page_with_jobid(self,jobID):
        joburl :str ="https://www.linkedin.com/jobs/view/"+str(jobID)
        self.browser.get(joburl)
        self.job_page = self.Load_page_Scroll_page()
        self.sleep(1)
        return self.job_page

    def Load_page_Scroll_page(self):
        scrollpage = 0
        while scrollpage<4000:
            self.browser.execute_script("window.scrollTo(0,"+str(scrollpage)+");")
            scrollpage+=500
            self.sleep(0.2)
        self.sleep()
        self.browser.execute_script("window.scrollTo(0,0);")
        page = BeautifulSoup(self.browser.page_source,'lxml')
        return page
    
    def is_present(self, locator):
        return len(self.browser.find_elements(locator[0],
                                              locator[1])) > 0
    
    def get_elements(self, type) -> list:
        elements = []
        element = self.locator[type]
        if self.is_present(element):
            elements = self.browser.find_elements(element[0], element[1])
        return elements
    
    def get_easy_apply_button(self):
        EasyApplyButton = False
        try:
            buttons = self.get_elements("easy_apply_button")
            
            for button in buttons:
                if "Easy Apply" in button.text:
                    EasyApplyButton = button
                    self.wait.until(EC.element_to_be_clickable(EasyApplyButton))
                else:
                    print("Easy Apply button not found")
            
        except Exception as e: 
            print("Exception:",e)
        return EasyApplyButton
    def fill_out_fields(self):
        fields = self.browser.find_elements(By.CLASS_NAME, "fb-dash-form-element")
        for field in fields:
            if "Mobile phone number" in field.text:
                field_input = field.find_element(By.TAG_NAME, "input")
                field_input.clear()
                field_input.send_keys(self.phonenumber)
        return
    

    def send_resume(self):
        def is_present(button_locator) -> bool:
            return len(self.browser.find_elements(button_locator[0],
                                              button_locator[1])) > 0
        
        try:


            next_locator = (By.CSS_SELECTOR,
                            "button[aria-label='Continue to next step']")
            
            review_locator = (By.CSS_SELECTOR,
                              "button[aria-label='Review your application']")
            
            submit_locator = (By.CSS_SELECTOR,
                              "button[aria-label='Submit application']")
            error_locator = (By.CLASS_NAME,"artdeco-inline-feedback__message")
            upload_resume_locator = (By.XPATH, '//span[text()="Upload resume"]')
            upload_cv_locator = (By.XPATH, '//span[text()="Upload cover letter"]')
            # WebElement upload_locator = self.browser.find_element(By.NAME, "file")
            follow_locator = (By.CSS_SELECTOR, "label[for='follow-company-checkbox']")

            submitted = False
            loop = 0

            while loop <2:
                self.sleep(3)
                #upload resume
                if is_present(upload_resume_locator):
                    #upload_locator = self.browser.find_element(By.NAME, "file")
                    try:
                        resume_locator = self.browser.find_element(By.XPATH, "//*[contains(@id, 'jobs-document-upload-file-input-upload-resume')]")
                        resume = self.resume_path
                        resume_locator.send_keys(resume)
                    except Exception as e:
                        print(e)
                        print("Resume upload failed")
                        print("Resume: " + resume)
                        print("Resume Locator: " + str(resume_locator))
                #upload cover letter if possible
                if is_present(upload_cv_locator):
                    cv = self.uploads["Cover Letter"]
                    cv_locator = self.browser.find_element(By.XPATH, "//*[contains(@id, 'jobs-document-upload-file-input-upload-cover-letter')]")
                    cv_locator.send_keys(cv)
                
                elif len(self.get_elements("follow")) > 0:
                    elements = self.get_elements("follow")
                    for element in elements:
                        button = self.wait.until(EC.element_to_be_clickable(element))
                        button.click()
                if len(self.get_elements("submit")) >0:
                    elements = self.get_elements("submit")
                    for element in elements:
                        button = self.wait.until(EC.element_to_be_clickable(element))
                        button.click()
                        print("Application Submitted")
                        submitted = True
                        break
                
                elif len(self.get_elements("error")) > 0:
                    elements = self.get_elements("error")
                    if "application was sent" in self.browser.page_source:
                        print("Application Submitted")
                        submitted = True
                        break
                    elif len(elements) > 0:
                        while len(elements) > 0:
                            for element in elements:
                                self.process_questions()

                            print("...........................................Please answer the questions, waiting 20 seconds...................................................")
                            self.sleep(20)
                            elements = self.get_elements("error")

                            

                            if "application was sent" in self.browser.page_source:
                                print("Application Submitted")
                                submitted = True
                                break
                            elif is_present(self.locator["easy_apply_button"]):
                                print("Skipping application")
                                submitted = False
                                break
                        continue
                    else:
                        print("Application not submitted")
                        self.sleep(2)
                        break
                elif len(self.get_elements("next")) > 0:
                    elements = self.get_elements("next")
                    for element in elements:
                        button = self.wait.until(EC.element_to_be_clickable(element))
                        button.click()
                elif len(self.get_elements("review")) > 0:
                    elements = self.get_elements("review")
                    for element in elements:
                        button = self.wait.until(EC.element_to_be_clickable(element))
                        button.click()

                elif len(self.get_elements("follow")) > 0:
                    elements = self.get_elements("follow")
                    for element in elements:
                        button = self.wait.until(EC.element_to_be_clickable(element))
                        button.click()
        except Exception as e:
            print(e)
            print("cannot apply to this job")
            pass
        return submitted
    def process_questions(self):
        self.sleep(3)
        form = self.get_elements("fields")
        self.sleep(2)
        for field in form:
            question = field.text
            answer = self.answer_Questions(question.lower())
            if self.is_present(self.locator["radio_select"]):
                try:
                    input = field.find_element(By.CSS_SELECTOR, "input[type='radio'][value={}]".format(answer))
                    input.execute_script("arguments[0].click();", input)
                except Exception as e:
                    print(e)
                    continue
            #multi select
            elif self.is_present(self.locator["multi_select"]):
                try:
                    input = field.find_element(self.locator["multi_select"])
                    input.send_keys(answer)
                except Exception as e:
                    print(e)
                    continue
            # text box
            elif self.is_present(self.locator["text_select"]):
                try:
                    input = field.find_element(self.locator["text_select"])
                    input.send_keys(answer)
                except Exception as e:
                    print(e)
                    continue

            elif self.is_present(self.locator["text_select"]):
               pass

            if "Yes" or "No" in answer: #radio button
                try: #debug this
                    input = form.find_element(By.CSS_SELECTOR, "input[type='radio'][value={}]".format(answer))
                    form.execute_script("arguments[0].click();", input)
                except:
                    pass


            else:
                input = form.find_element(By.CLASS_NAME, "artdeco-text-input--input")
                input.send_keys(answer)
    def answer_Questions(self,question):
        answer = None
        if "salary" in question:
            answer = self.salary
        elif "gender" in question:
            answer = self.gender
        elif "relocate" in question:
            answer = "Yes"
        elif "bachelor's degree" in question:
            answer = "Yes"
        elif "are you comfortable" in question:
            answer = "Yes"
        elif "race" in question:
            answer = "Wish not to answer"
        elif "lgbtq" in question:
            answer = "Wish not to answer"
        elif "ethnicity" in question:
            answer = "Wish not to answer"
        elif "nationality" in question:
            answer = "Wish not to answer"
        elif "government" in question:
            answer = "I do not wish to self-identify"
        elif "are you legally" in question:
            answer = "Yes"
        elif "US citizen" in question:
            answer = "Yes"
        else:
            print("Not able to answer question automatically. Please provide answer")
            #open file and document unanswerable questions, appending to it
            answer = "user provided"
            self.sleep(9)
            if question not in self.answer:
                self.answer[question] = answer
                new_data = pd.DataFrame({"Question":[question],"Answer":[answer]})
                new_data.to_csv(self.qa_file,mode='a',header=False,index=False,encoding='utf-8')
                print(f"Appended to QA file: '{question}' with answer: '{answer}'.")
           
        print("Answering question: " + question + " with answer: " + answer)
        
        

        return answer
Main()


