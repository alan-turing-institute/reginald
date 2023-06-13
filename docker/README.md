To build this Docker image you need to be in the parent directory.
The following command will build it:

```
docker build . -t reginald:latest -f docker/Dockerfile
```

The following environment variables will be used by this image:

- `REGINALD_MODEL`: name of model to use
- `SLACK_APP_TOKEN`: app token for Slack
- `SLACK_BOT_TOKEN`: bot token for Slack
