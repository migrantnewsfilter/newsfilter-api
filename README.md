## Architecture

Two services are actively gathering news and writing them directly to our application database, [Twitter](https://github.com/migrantnewsfilter/twitter) and [Alerts-RSS](https://github.com/migrantnewsfilter/alerts-rss).

To develop locally, [dumper](https://github.com/migrantnewsfilter/dumper) is running on a cron job and taking mongodb dumps every day at midnight and writing them to S3. Whenever you need to get a new seeded database for development with a copy of the latest production data, use [seed-db](https://github.com/migrantnewsfilter/seed-db), which will grab the latest dumps from S3 and index it to your database.


## Develop on API

You will need to have docker installed, and then you can run:

```
docker-compose up
```

Then seed the mongo database with our latest dump from production:

```
docker run --net host migrantnewsfilter/seed-db
```

## Schemes + Data

At this stage, we are taking full advantage of Mongo's schemaless design and tossing everythign in. As the application develops and solidifies we will use protobuf's to enforce schema changes and keep the UI and content-producing applications in-sync.

Currently the schema of our article content is defined by the producers, so take a look [here](https://github.com/migrantnewsfilter/alerts-rss/blob/master/mongo.py#L6) and [here](https://github.com/migrantnewsfilter/alerts-rss/blob/master/mongo.py#L6).
