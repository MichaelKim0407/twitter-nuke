# Twitter Nuke

Delete all contents on Twitter.

## Description

Delete all tweets and likes on your Twitter account after backing them up,
while allowing you to select the ones you want to keep.

## Intended user

There are commercial products out there that are easier to use,
however this is free and open source if you'd like to jump through some hoops.

You should have at least basic proficiency with Python programming, data handling,
programming against an API, and containerization (Docker).

**USE AT YOUR OWN RISK.**

Commercial use and redistribution of this software is strongly discouraged.
Please see [LICENSE](LICENSE).

## Prerequisites

* This project is Dockerized, so you need to have Docker installed.

## Preparations

1. Request an archive of your Twitter data.
   The request may take a few days to process.
   Download the data when it's ready.

2. Create a Twitter developer account.
   Create an app and generate access tokens with write permissions.
   As of writing (Aug 2022), Twitter makes you jump through a bunch of hoops to get there.
   You will need to:
   a) request "Elevated" access;
   b) create a project and an app after getting the access;
   c) change your app permission to Read/Write in the "User authentication settings" section;
   d) generate access tokens.

## Steps

1. Clone this repo.

2. Make `twitter.env` from `twitter.env.template` and fill in the keys and tokens you got from Twitter.
   User ID is a numerical ID of your account, not your Twitter handle.
   You can find your ID in `(archive)/data/account.js`.

3. Run `make` to build a Docker image with Python dependencies installed.

4. Unzip your Twitter archive and copy these files:
   * `(archive)/data/tweet.js` -> `(project)/data/backup-data/tweet.js`
   * `(archive)/data/like.js` -> `(project)/data/backup-data/like.js`

5. Generate ID lists of tweets and likes.
   ```
   docker-compose run --rm backup_extract
   ```
   This will create the following files:
   ```
   (project)/
     data/
       extracted/
         tweet.csv
         like.csv
       extract-tmp/
         ... (a few JSON files you can use to manually explore the data)
   ```

6. Select tweets and likes you want to keep.
   Since what you want to keep is entirely up to you, there is no standardized procedure for this step.
   However you should be able to utilize the JSON tmp files from the step above.
   Place the ID lists here:
   ```
   (project)/
     data/
       customize/
         keep/
           tweet.csv
           like.csv
   ```
   Either file is optional. If you don't provide a list, all items of that type will be selected for deletion.

7. Generate final ID lists for deletion.
   ```
   docker-compose run --rm gen_final
   ```
   This will create the following files:
   ```
   (project)/
     data/
       to-delete/
         tweet.csv
         like.csv
   ```
   If you have provided lists to keep,
   it might be a good idea to manually check the results before
   continuing on to the next step.

8. Delete your tweets and likes.
   ```
   docker-compose run --rm delete
   ```
   **THIS IS NOT UNDO-ABLE.**
   This operation may take a while as Twitter API has a very small rate limit of 50 requests per 15 minutes for deletion.
   The logic to wait for the rate limit to reset is included. Just let it run.
   The following log files will be generated:
   ```
   (project)/
     data/
       delete-logs/
         tweet.log
         like.log
   ```
