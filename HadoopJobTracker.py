import requests as request
import time

def getAllApplicationsIdList(proxies=None):

   requestLinkString = 'http://localhost:8088/ws/v1/cluster/apps'
   allApplications = request.get(requestLinkString,proxies=proxies).json()
   
   #If there is no application running currently
   if(allApplications['apps'] == None):
     return
   else:
     applicationDetailList = allApplications['apps']['app']
     applicationIdList = [applicationDetail['id'] for applicationDetail in applicationDetailList]
     return applicationIdList
     
     
          
def getAllJobsIdList(applicationId , proxies=None):
  requestLinkString = "http://<proxy http address:port>/proxy/" + applicationId + "/ws/v1/mapreduce/jobs"
  allJobs = request.get(requestLinkString,proxies=proxies).json()
  
    #If there are no Jobs running for the given application Id
  if(allJobs['jobs']==None):
      return
  else:
      jobDetailList = allJobs['jobs']['job']
      jobIdList = [str(jobDetail['id']) for jobDetail in jobDetailList]
      return jobIdList

      

def getNewCompletedTasks(applicationId , jobId , alreadyReportedTasks , proxies = None):
  
  requestLinkString = "http://<proxy http address:port>/proxy/" + applicationId + "/ws/v1/mapreduce/jobs/"+jobId+"/tasks"
  
  allTasks =  request.get(requestLinkString,proxies=proxies).json()
  
  if(allTasks['tasks'] == None):
    print('No running task for this' + 'Application ID: ' +applicationId +' Job Id: ' +jobId)
    return
  
  else:
    
       taskDetailList = allTasks['tasks']['task']
       
       #Logic to get the non reported completed task goes here
       
       newCompletedTaskIdList = [str(taskDetail['id']) for taskDetail in taskDetailList if str(taskDetail['state'])=='SUCCEEDED'
                                                             and str(taskDetail['id'])  not in alreadyReportedTasks]
       
       return  newCompletedTaskIdList                     
   


def getSuccessfulTaskAttemptId(applicationId , jobId , taskId ,  proxies = None):
  
  requestLinkString = "http://<proxy http address:port>/proxy/"+applicationId+"/ws/v1/mapreduce/jobs/"+jobId+"/tasks/"+taskId+"/attempts"
  
  allTaskAttempts = request.get(requestLinkString,proxies=proxies).json()
  if(allTaskAttempts['taskAttempts'] == None):
    print('No attempt has made till now for applicationId '+applicationId+' jobId '+jobId+' taskId '+taskId)
    return
  else:
    
    allTaskAttemptDetaillist = allTaskAttempts['taskAttempts']['taskAttempt']
    successfulTaskAttemptIdList = [str(allTaskAttemptDetail['id']) for allTaskAttemptDetail in allTaskAttemptDetaillist 
                                  if str(allTaskAttemptDetail['state']) == 'SUCCEEDED' ]
    return  successfulTaskAttemptIdList


    

def getTaskCounter(applicationId , jobId , taskId , attemptId , proxies = None):
    
    requestLinkString = "http://<proxy http address:port>/proxy/"+applicationId+"/ws/v1/mapreduce/jobs/"+jobId+"/tasks/"+taskId+"/attempts/"+attemptId+"/counters"
                         
    TaskCounter =  request.get(requestLinkString,proxies=proxies).json()
    
    if(TaskCounter['JobTaskAttemptCounters']==None):
      print('There is no task counter data available for attemptId '+attemptId+' Task Id'+ taskId)
    else:
      return TaskCounter      
    
    
def getNodeOfTask(applicationId , jobId , taskId , attemptId ,proxies = None):
    
    requestLinkString = "http://<proxy http address:port>/proxy/" +applicationId +"/ws/v1/mapreduce/jobs/"+jobId+"/tasks/"+taskId+"/attempts"
                       
    #allTaskAttempts = request.get(requestLinkString,proxies=proxies).json()
    
    if(allTaskAttempts['taskAttempts'] == None):
      print('No attempt has made till now for applicationId '+applicationId+' jobId '+jobId+' taskId '+taskId)
      return
    else:
    
      allTaskAttemptDetaiList = allTaskAttempts['taskAttempts']['taskAttempt']
      taskNodeDetailTuple = [( str(allTaskAttemptDetail['nodeHttpAddress']) , str(allTaskAttemptDetail['rack']) )
                                     for allTaskAttemptDetail in allTaskAttemptDetaiList 
                                     if str(allTaskAttemptDetail['id']) == attemptId ]
      return  taskNodeDetailTuple  
      


if __name__=='__main__':
    
#In case of Proxy Server Authentication required , Please put the user , password , ip and port of Client side in the respective variable
#USER =''
#PASSWORD=''
#IP=''
#PORT=''
#proxies = { 'http' : 'http://user:password@ip:port' , 'https' : 'https://user:password@ip:port' }
  
  # If you have given the proxy above , please remoove the variable
  proxies = None
  print("All the running Application's ID")
  
  allApplicationsIdList = getAllApplicationsIdList(proxies=proxies)
  
  if(allApplicationsIdList != None) :
       #printing all the Application Id
       for applicationId in allApplicationsIdList:
          print(applicationId)
       
       print('Please enter the Application ID for toget all the Job Id for the application')
       appId = str(input())
       
       jobIdList = getAllJobsIdList(applicationId = appId , proxies=proxies)
       
       if(jobIdList != None):
         print('All the jobs for application: '+appId)
         for jobId in jobIdList:
           print(jobId)
         
         print('Please enter the job Id to get all the task detail for the job')
         jId = str(input())
         #As in the beginning there is no task reported , so empty list is declared
         alreadyReportedTasks = []
         
         while True:
           newCompletedTasks = getNewCompletedTasks(applicationId = appId , jobId = jId , alreadyReportedTasks = alreadyReportedTasks , proxies=proxies)
           
           if(newCompletedTasks != None): 
             for newCompletedTask in newCompletedTasks:
               #The programmer for this code has assumed that there will be only one successfulTaskAttemptId per Task .
               successfulTaskAttemptId = getSuccessfulTaskAttemptId(applicationId = appId , jobId = jId , taskId = newCompletedTask , proxies=proxies)[0]
               taskCounter = getTaskCounter(applicationId = appId, jobId = jId, taskId = newCompletedTask, attemptId = successfulTaskAttemptId , proxies=proxies)
               print('TaskCounter for the Task: '+newCompletedTask)
               print(taskCounter)
               
               nodeOfTask = getNodeOfTask(applicationId = appId, jobId = jId , taskId =newCompletedTask, attemptId = successfulTaskAttemptId , proxies=proxies)
               
               print('Node Http Address and the rack for the Node on which task completed')
               print(nodeOfTask)
               
             alreadyReportedTasks.extend(newCompletedTasks)  
           
           #sleeps for 20 seconds           
           time.sleep(20)              
               
       else:
         print('No job running for the Application Id: '+appId)       
       
  else:
      print('No Application running currently') 
 
  
