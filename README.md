# Workflow Issue Analysis

This repository contains the analysis of issue existence in workflow files in different repositories.

## Preprocessing Steps

### Step 1:
- Run ActionLint on the workflow files.
- Run the script to count the total number of lines in the workflows.

### Step 2:
- Choose only the workflow files that are valid workflow files.

### Step 3:
- Merge the dataset with the dataset from ActionLint on the `file_hash` column.

### Step 4:
- Create new features such as: `status`, `next commit`, `error count`, `unique workflow id`.

### Step 5:
- Perform resampling to obtain a normalized dataset.

### Step 6:
- Map the custom Issue Rule to the dataset.

## Dataset Features
The dataset comprises numerous features which are as follows:

1. **Message:** Error message in the workflow file reported by ActionLint.
2. **Line:** Line of the error message in the workflow file.
3. **Column:** Column of the error message in the workflow file.
4. **Kind:** Error messages are divided into various kinds such as: `deprecated-commands`, `expression`, `runner-label`, `events`, `action`, `syntax-check`, `workflow-call`, `matrix`, `glob`, `job-needs`, `id`, `env-var`, `shell-name`, `yaml-syntax` depending on the text of the error message.
5. **Snippet:** Information about the code snippet where the error occurs in the workflow file.
6. **End Column:** End column of the error message in the workflow file.
7. **File Hash:** Hash of the workflow file.
8. **Repository:** Repository of the workfile.
9. **Commit Hash:** Hash of the commit of the workflow file in the repository.
10. **Author Name:** Author name of the committer.
11. **Author Email:** Author email of the committer.
12. **Committer Name:** Name of the committer.
13. **Committer Email:** Email of the committer.
14. **Committed Date:** Committed date of the commit.
15. **Authored Date:** Date and time when the changes were originally created by the contributor.
16. **File Path:** File path of the workflow in the repository.
17. **Previous File Path:** Previous file path of the workflow file in the repository.
18. **Previous File Hash:** Hash of the previous workflow file in the repository.
19. **Change Type:** Refers to the change in the workflow file such as Added (A), Modified (M), and Remove (R).
20. **Valid YAML:** Provides information about the file that it is a valid YAML file but not clear that it is a workflow file.
21. **Valid Workflow:** Provides information that it is a valid workflow file.
22. **Lines Count:** Total number of lines in the workflow.
23. **Time Lapse:** Provides the time difference between the first commit with the error message and the specified commit in the repository.
24. **Status:** Provides the information that the issue is open or closed in the workflow file at the specified commit.
25. **Error Count:** Provides the information about the total number of issues at a specified commit in the workflow.
26. **Unique Workflow ID:** Gives the unique workflow ID that is the combination of the `{author}/{repo}/{filepath}/{hash_val}` of the workflow.



## Pseudocode for Extracted Features
Here's a glimpse of the pseudocode for extracting essential features:

### Error Count Feature
```python
  function error_count(repository, dataframe):
      count = 0 
      msgstack = []
  
      for each row in dataframe:
          if row['repository'] equals repository then
              if row['message'] is in msgstack then
                  Remove row['message'] from msgstack
                  count = count - 1
                  Update row['error_count'] in dataframe to count
              else:
                  Add row['message'] to msgstack
                  count = count + 1
                  Update row['error_count'] in dataframe to count
          end if
      end for
  
      return dataframe
```
### Time Lapse
```python
function time_lapse(repository, dataset):
    for each row in dataset:
        if row['repository'] equals repository then
            Convert row['committed_date'] to datetime object
            Add converted row['committed_date'] back to dataset

    Sort dataset by 'committed_date' in ascending order
    Set start_date TO MINIMUM 'committed_date' value in dataset

    for each row in dataset:
        Calculate time difference between row['committed_date'] and start_date
        Set row['time_lapse'] to calculated time difference

    return dataset
```
### Status
```python
function status_feature(df):
    for each unique_commit in df['commit_hash']:
        Create df_temp containing rows where 'commit_hash' EQUALS unique_commit
        next_commit = rows in df where 'commit_hash' equals the 'next_commit_hash' of the first row of df_temp

        common_messages = get common messages between df_temp and next_commit

        set 'status' to "closed" for rows where 'commit_hash' equals unique_commit in df
        set 'status' to "open" for rows where 'commit_hash' equals unique_commit and 'message' is in common_messages in df

    return df
```
### Unique Workflow Id:
```python
function generate_workflow_id(dataset):
    sort dataset by 'committed_date'
    mapping = {}
    result = {}

    for each row in dataset:
        repo = get 'repository' from row
        filepath = get 'file_path' from row
        hash_val = get 'commit_hash' from row
        previous = get 'previous_file_path' from row
        author = get 'author_name' from row

        if filepath is not empty and type of previous equals float then
            unique_id = concatenate author, "/", repo, "/", filepath, "/", hash_val
            mapping[(repo, filepath)] = unique_id
            result[index of row] = unique_id

        else if filepath is empty and previous is not empty then
            if (repo, previous) not in mapping then
                raise value error
            else:
                delete mapping[(repo, previous)]
                result[index of row] = null

        else if filepath is not empty and previous is not empty then
            unique_id = concatenate author, "/", repo, "/", filepath, "/", hash_val
            if (repo, previous) not in mapping then
                print "cannot find unique id for previous filepath: {repo}/{previous}"
                result[index of row] = unique_id
                continue
            else:
                mapping[(repo, filepath)] = mapping[(repo, previous)]
                result[index of row] = mapping[(repo, filepath)]

    return result
```
### Resampling of the dataset wrt to date
```python
function resampling(dataset, repository):
    dataset = filter dataset where 'repository' equals repository
    if length of dataset < 2 then
        return dataset
    else:
        error_count_sum = sum of 'error_count' grouped by 'date' in dataset
        sort dataset by 'committed_date'
        temp_list = []

        for each row in dataset:
            date = get 'date' from row
            next_date = get 'next_date' from row
            number_of_days = calculate difference in days between next_date and date
            expected_next_date = calculate the expected next date

            error_sum = get error count sum for the date from error_count_sum
            if date equals next_date then
                continue to next iteration

            else if date not equal to next_date and number_of_days > 1 then
                insert duplicate row for expected next date
                append inserted rows to temp_list
                print "row inserted !!!"

        if temp_list is empty then
            return dataset
        else:
            concatenate temp_list and dataset into df_data
            sort df_data by 'committed_date'
            return df_data
```
