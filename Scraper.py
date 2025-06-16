import requests
from time import sleep
from random import randint

def get_followers(userId: str):
  params = {
      "variables":
      f'{{"userId":"{userId}","count":20, "includePromotedContent":false}}}}',
      "features":'{"rweb_video_screen_enabled":false,"profile_label_improvements_pcf_label_in_post_enabled":true,"rweb_tipjar_consumption_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"premium_content_api_read_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"responsive_web_grok_analyze_button_fetch_trends_enabled":false,"responsive_web_grok_analyze_post_followups_enabled":true,"responsive_web_jetfuel_frame":false,"responsive_web_grok_share_attachment_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"responsive_web_grok_show_grok_translated_post":false,"responsive_web_grok_analysis_button_from_backend":true,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_grok_image_annotation_enabled":true,"responsive_web_enhance_cards_enabled":false}'
  }

  headers = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "Cookie": 'guest_id_marketing=v1%3A174973919619409054; guest_id_ads=v1%3A174973919619409054; guest_id=v1%3A174973919619409054; __cf_bm=6yYWavQIsUQaFnidE83l1bhunGxikyMzM6COWmh7MhQ-1749739196-1.0.1.1-5N9xy5qtGOongNSELs0kTfHzPeW2dRkaFpvoV6jofVLw_P7Z9uBlgWjFFdiWZZsdcoY_gF7sIn9j7MebI2TlHSXQqK3pK4Jn5Gq0Mw4cfgE; gt=1933172420132635092; personalization_id="v1_3i/stAuLGUyrhwLFbjjX5g=="; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGMTl2SXAToMY3NyZl9p%250AZCIlNmUwZjIxNTU3NjIzMWNkNDNiOTM4ZTRjNzVlOTk0YmQ6B2lkIiUzNjk2%250AZjJmYzhiMmJjYWM5Nzc4ODkyZWRiNDI1MDA0MA%253D%253D--32c4e0943c6c2d9683bd573c026c92bb80378a4a; kdt=J3yDI0583qJLK1GkL3EWOI7mIJl2J3Ym1QSnSKSn; auth_token=bbf24dbe0498ea1f781c916f8b87eb28c9f73c79; ct0=a86f3acf802295821c56f0417cd0d7ed9a13ebe411590b799b76bf138a25e6c7ca2ba1a0e029a986a518e6e424335035b2e42a09bc028a76482253a78d1deaa667ad5d766a311561fa5b7e3d6da4a0b5; lang=en; twid=u%3D1933173310105284608',
    "X-Csrf-Token": "a86f3acf802295821c56f0417cd0d7ed9a13ebe411590b799b76bf138a25e6c7ca2ba1a0e029a986a518e6e424335035b2e42a09bc028a76482253a78d1deaa667ad5d766a311561fa5b7e3d6da4a0b5"
  }

  url = "https://x.com/i/api/graphql/c_jgHCwuRXq4nOT9iklyDg/Following"
  
  response = requests.get(url, headers=headers, params=params)

  if response.status_code == 200:
    data = response.json()
    return data
  else:
    return None
  
def parse_tweet_text(post):
    text = ""
    name = ""
    handle = ""
    try:
      if post['entryId'].startswith('cursor'):
          print("Skipping cursor entry:", post['entryId'])
          return None
      if ('items' in post['content'] and post['content']['items'][0]['item']['itemContent']['itemType'] != 'TimelineTweet'):
          text = "Err: Not a tweet"
          return None
      if ('items' in post['content'] and post['content']['items'][0]['item']['itemContent']['itemType'] == 'TimelineTweet' and 'note_tweet' in post['content']['items'][0]['item']['itemContent']['tweet_results']['result']):
          text = post['content']['items'][0]['item']['itemContent']['tweet_results']['result']['note_tweet']['note_tweet_results']['result']['text']
          name = post['content']['items'][0]['item']['itemContent']['tweet_results']['result']['core']['user_results']['result']['core']['name']
          handle = post['content']['items'][0]['item']['itemContent']['tweet_results']['result']['core']['user_results']['result']['core']['screen_name']
      elif ('items' in post['content'] and 'tweet_results' in post['content']['items'][0]['item']['itemContent'] and 'legacy' in post['content']['items'][0]['item']['itemContent']['tweet_results']['result']):
          text = post['content']['items'][0]['item']['itemContent']['tweet_results']['result']['legacy']['full_text']
          name = post['content']['items'][0]['item']['itemContent']['tweet_results']['result']['core']['user_results']['result']['core']['name']
          handle = post['content']['items'][0]['item']['itemContent']['tweet_results']['result']['core']['user_results']['result']['core']['screen_name']
      elif ('items' in post['content'] and 'tweet_results' in post['content']['items'][0]['item']['itemContent']):
          text = post['content']['items'][0]['item']['itemContent']['tweet_results']['result']['tweet']['legacy']['full_text']
          name = post['content']['items'][0]['item']['itemContent']['tweet_results']['result']['tweet']['core']['user_results']['result']['core']['name']
          handle = post['content']['items'][0]['item']['itemContent']['tweet_results']['result']['tweet']['core']['user_results']['result']['core']['screen_name']
      elif ('tweet' in post['content']['itemContent']['tweet_results']['result']):
          text = post['content']['itemContent']['tweet_results']['result']['tweet']['legacy']['full_text']
          handle = post['content']['itemContent']['tweet_results']['result']['tweet']['legacy']['entities']['user_mentions'][0]['screen_name']
          name = post['content']['itemContent']['tweet_results']['result']['tweet']['legacy']['entities']['user_mentions'][0]['name']
      else:
          text = post['content']['itemContent']['tweet_results']['result']['legacy']['full_text']
          name = post['content']['itemContent']['tweet_results']['result']['legacy']['retweeted_status_result']['result']['core']['user_results']['result']['core']['name']
          handle = post['content']['itemContent']['tweet_results']['result']['legacy']['retweeted_status_result']['result']['core']['user_results']['result']['core']['screen_name']
      return text, name, handle
    except KeyError as e:
      print(f"KeyError: {e} in post: {post}")
      return None

if __name__ == "__main__":
  user_id = "1933173310105284608"  # Example user ID
  followers_data = get_followers(user_id)
  
  if followers_data:
    print(followers_data)
  else:
    print("Failed to retrieve followers data.")

def get_tweets(userId: str, lim: int):
  # each call returns 20 tweets (and two cursor objects), and we do different logic on the first call
  if lim <= 0:
    lim = 1

  if lim > 40:
    print("You are attempting to make many calls to the API. This may result in rate limiting.\n")
    conf = input("Do you want to continue? (y/n): ")
    if conf.lower() != 'y':
      return None
  
  lim *= 2

  tweets = []

  params = {
    "variables": f'{{"userId":"{userId}","count":20,"withCommunity":true,"withVoice":true,"includePromotedContent":false}}',
    "features": '{"rweb_video_screen_enabled":false,"payments_enabled":false,"profile_label_improvements_pcf_label_in_post_enabled":true,"rweb_tipjar_consumption_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"premium_content_api_read_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"responsive_web_grok_analyze_button_fetch_trends_enabled":false,"responsive_web_grok_analyze_post_followups_enabled":true,"responsive_web_jetfuel_frame":false,"responsive_web_grok_share_attachment_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"responsive_web_grok_show_grok_translated_post":false,"responsive_web_grok_analysis_button_from_backend":true,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_grok_image_annotation_enabled":true,"responsive_web_enhance_cards_enabled":false}'
  }

  #todo: replace with some chromedp logic to refresh the cookies
  #csrf and client transaction are needed, but have a super long TTL?
  headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'Content-Type': 'application/json',
    'Cookie': 'guest_id_marketing=v1%3A174973919619409054; guest_id_ads=v1%3A174973919619409054; guest_id=v1%3A174973919619409054; personalization_id="v1_3i/stAuLGUyrhwLFbjjX5g=="; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGMTl2SXAToMY3NyZl9p%250AZCIlNmUwZjIxNTU3NjIzMWNkNDNiOTM4ZTRjNzVlOTk0YmQ6B2lkIiUzNjk2%250AZjJmYzhiMmJjYWM5Nzc4ODkyZWRiNDI1MDA0MA%253D%253D--32c4e0943c6c2d9683bd573c026c92bb80378a4a; kdt=J3yDI0583qJLK1GkL3EWOI7mIJl2J3Ym1QSnSKSn; auth_token=bbf24dbe0498ea1f781c916f8b87eb28c9f73c79; ct0=a86f3acf802295821c56f0417cd0d7ed9a13ebe411590b799b76bf138a25e6c7ca2ba1a0e029a986a518e6e424335035b2e42a09bc028a76482253a78d1deaa667ad5d766a311561fa5b7e3d6da4a0b5; lang=en; twid=u%3D1933173310105284608; external_referer=padhuUp37zj8EmLbOM3WbV5l0GjLCcayDDEsgmoWhxc%3D|0|8e8t2xd8A2w%3D; __cf_bm=ClbXZ8VF8Oif174LPTTX5oFnp5NAOQTazPp2FLcuwdU-1749750582-1.0.1.1-2PZutk6DIU3gSi7lmN5CUhZOZJsdhDAblMOEHiNx.fZ4Szc_vb_wZgHEXSo0pDjryMBa5xXOF32zoLnszihQfGsWRSDEN_Vv8iiMfOE.YYg',
    'X-Csrf-Token': 'a86f3acf802295821c56f0417cd0d7ed9a13ebe411590b799b76bf138a25e6c7ca2ba1a0e029a986a518e6e424335035b2e42a09bc028a76482253a78d1deaa667ad5d766a311561fa5b7e3d6da4a0b5',
    'X-Client-Transaction-Id': 'ZBu6tTuWW1BmXyUdD8Tz2J/7U/gaB0Dx6qac9P5+qT/yb5PJ+1SnKgxdFhmdJYD8QcnUn2erUASMWeb4m4WkIY8fiOWrZw'
  }

  #fetches user replies
  url = "https://x.com/i/api/graphql/Z9gIrY5Gq-2K7HXhIimlyQ/UserTweetsAndReplies"

  #special for the first call, because we need to get the first cursor
  response = requests.get(url, headers=headers, params=params)

  if response.status_code == 200:
    data = response.json()
    data = data['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries']

    #fetches the next cursor from the last val of the response
    next = data[-1]['content']['value']

    for post in data:

      parsed = parse_tweet_text(post)
      if parsed is None:
        continue

      text, name, handle = parsed

    tweets.append({'name': name, 'handle': handle, 'text': text})

    for i in range(lim - 1):
      sleep(randint(2, 6))  # Sleep to avoid rate limiting

      if next == 0:
        break

      params['variables'] = f'{{"userId":"{userId}","count":20,"withCommunity":true,"withVoice":true,"includePromotedContent":false,"cursor":"{next}"}}'
      response = requests.get(url, headers=headers, params=params)

      print(f"Fetching tweets for cursor: {next}")

      if response.status_code == 200:
        data = response.json()
        data = data['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries']

        #fetches the next cursor from the last val of the response
        next = data[-1]['content']['value']
        for post in data:

          parsed = parse_tweet_text(post)

          if parsed is None:
            continue

          text, name, handle = parsed

          tweets.append({'name': name, 'handle': handle, 'text': text})

  
  else:
    Exception("Failed to retrieve tweets data. You might be rate limited.")

  return tweets