## Run

You will need to have this repo and alerts-rss repo cloned, in sibling files, in order to run the application.

You will also need Docker.

```
docker-compose up
```

Then seed the mongo database with our latest dump from production:

```
docker run --net host migrantnewsfilter/seed-db
```

Then clone the newsfilter-ui repo. You will need to follow the instructions there in order to run the UI in development mode.
