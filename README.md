# twitter-nuke
Permanantly remove your tweets (including media), retweets, and favorites from your Twitter profile. It's recommended to download your archive prior to doing this. 

## Dependencies 
Depends on [tweepy](https://pypi.org/project/tweepy/).

## Usage
Steps:
1. Generate your `consumer_key`, `consumer_secret`, `access_token`, `access_token_secret` via the Twitter developer portal. Place them in `keys.yaml`
2. `python nuke.py`
3. You may need to repeat step 2 several times, e.g., if you meet the API rate limit.

## Known issues
- Retweets and favorites that were deleted by the author cannot be removed from your profile. If the author "undeletes" their post, it will reappear on your profile. Once it reappears, you can remove it from your profile with this script or manually. 
