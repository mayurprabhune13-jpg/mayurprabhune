# Automatic LinkedIn and Instagram feed updates

The website stores the latest public LinkedIn posts and Instagram feed/Reel items in `social_post`. A Railway Cron service refreshes that cache daily at 03:15 UTC. The site reads from the cache, so the homepage stays responsive and continues showing the last successful sync if a provider has a temporary outage.

## One-time Railway setup

1. Deploy the website code from GitHub using the existing manual Railway deploy process. The web service's `preDeployCommand` applies the additive `social_post` migration.
2. In Railway, create a second service from the same GitHub repository and production branch. Name it `social-sync`.
3. Set its Config-as-Code file to `/railway-social-sync.json`. This config starts `scripts/sync_social_posts.py` on a daily schedule and exits after the fetch.
4. Give the worker the same production `DATABASE_URL` as the web service and add the social variables below through Railway's Variables screen. Do not put access tokens in GitHub, this file, or chat.
5. Run the worker once from Railway's Cron Runs panel and confirm successful provider syncs in its logs.

Railway cron schedules use UTC. The provided schedule runs daily at 03:15 UTC (08:45 India Standard Time). Change `cronSchedule` in `railway-social-sync.json` if a different refresh time is preferred.

## LinkedIn variables

- `LINKEDIN_ACCESS_TOKEN`: bearer token for the authorized member account.
- `LINKEDIN_AUTHOR_URN`: Mayur's person URN, in `urn:li:person:...` format.
- `LINKEDIN_API_VERSION`: active LinkedIn Marketing API version, formatted `YYYYMM`; the current code default is `202610`.

The LinkedIn Posts API requires `r_member_social` to read a member's posts, and LinkedIn restricts that permission to approved applications. A normal sign-in or public profile URL does not grant this access.

## Instagram variables

- `INSTAGRAM_ACCESS_TOKEN`: access token for the professional `aiwali_duniya` account.
- `INSTAGRAM_GRAPH_API_VERSION`: active Instagram API version; the code default is `v25.0`.

The fetcher uses Instagram Login's `/me/media` endpoint and requests captions, media type, product type, permalink, media URL, thumbnail and timestamp. The account must be a Creator or Business account and authorize the app with the basic media-reading permission. The token must be renewed before it expires; update it through Railway Variables. Instagram image/video URLs are refreshed on each successful run.

## Feed behavior

- The homepage displays the three newest fetched LinkedIn posts and three newest Instagram items. Reels are labeled from Instagram's media metadata and link to the original Reel.
- `/blog` includes the newest LinkedIn posts alongside published site articles.
- API errors do not delete the previous cache. The cron run logs a provider failure so it can be investigated.
- Without API authorization, the pages show profile links instead of pretending the curated highlights are live.
- Fetching updates content in the database. It does not publish a new website deployment; the site templates only need to be deployed once when this feature is installed.

## Applying the database migration manually

If the deployed web service does not run the configured pre-deploy command, run this in its Railway shell before starting the cron service:

```sh
flask --app wsgi:app db upgrade
```
