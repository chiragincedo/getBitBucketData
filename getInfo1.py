import requests
import csv
from datetime import datetime

# Bitbucket repository details
username = 'chirag220401'
repository = 'chirag-demo-project1/demo-repo1'

# Bitbucket credentials (Use app passwords or OAuth token for security)
password = 'ATBB8UpB36wxKjjBWCtF4QYKubetB4A3EB5C'


# List to store PR details
all_pull_requests = []
base_url = 'https://api.bitbucket.org/2.0'
endpoint = f'/repositories/{repository}/pullrequests'
url = base_url + endpoint
auth = (username, password)
data=[]
# Send GET request to Bitbucket API
while True:
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        pr_data = response.json()
        all_pull_requests.extend(pr_data['values'])
        break
    else:
        print(response)
        print('Error fetching PRs: {}'.format(response.status_code))
        break



#get date range between which we have to find PR details
get_author=False
print("Enter Range of Date between which you have to fetch data")
start_date= input("Enter Start Date in format (YYYY-MM-DD) :")
end_date= input("Enter End Date in format (YYYY-MM-DD) : ")

c= input("Press 'Y' to get PR from specific author : ")
authors=[]
if(c=='Y'):
    get_author=True
    while(c=='Y'):
        author_name= input("Enter Authors Name : ")
        authors.append(author_name)
        c= input("Press 'Y' to enter more authors : ")



# Print PR details
for pr in all_pull_requests:
        pr_no= pr['id']
        pr_name = pr["title"]
        pr_url = pr["links"]["self"]["href"]
        pr_author= pr['author']['display_name']

        #get no. of commits
        api_url=pr["links"]["commits"]["href"]
        response = requests.get(api_url, auth=auth)
        if response.status_code == 200:
            commits_data = response.json()
            no_of_commits = len(commits_data["values"])
        else:
            no_of_commits=1
            
        #get raised and merge dates and their difference
        pr_raised_date = pr["created_on"][:10]
        pr_merged_date = pr.get("merged_on", "Not Merged")[:10]

        date_format = "%Y-%m-%d"
        date1 = datetime.strptime(pr_raised_date, date_format)
        if(pr_merged_date!='Not Merged'):
           date2 = datetime.strptime(pr_merged_date, date_format)
           date_difference= abs(date1-date2) +1
        else:
             date_difference='Not Merged'

        if(pr_raised_date>=start_date and pr_raised_date<=end_date and (pr_author in authors if get_author else True)):
            #appending all data in list to write in csv file
            data.append({'PR No.':pr_no,
                        'PR Name':pr_name,
                        'PR URL':pr_url,
                        'Author':pr_author,
                        'No. of commits':no_of_commits,
                        'PR Raised Date': pr_raised_date,
                        'PR Merged Date':pr_merged_date,
                        'Time taken to merge the PR': date_difference })

            print("PR No.: ",pr_no)
            print("PR Name:", pr_name)
            print("PR URL:", pr_url)
            print("Author :",pr_author)
            print("No. of Commits:", no_of_commits)
            print("PR Raised Date:", pr_raised_date)
            print("PR Merged Date:", pr_merged_date)
            print('Time taken to merge the PR :',date_difference)
            print('---')


if len(data)==0:
    print("No data found to write!")
    exit(0)

#path of file to be used
csv_file = 'data.csv'

# Field names in csv 
field_names = ['PR No.','PR Name','PR URL','Author','No. of commits','PR Raised Date','PR Merged Date','Time taken to merge the PR']

# Writing data to CSV file
with open(csv_file, 'w',encoding='utf8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    
    # Write the header
    writer.writeheader()
    
    # Write the data
    for row in data:
        writer.writerow(row)

print(f'Data written to {csv_file}')

