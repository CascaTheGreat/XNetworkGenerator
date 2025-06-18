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
    #todo: replace with some chromedp logic to refresh the cookies
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

  cookies = {
    'guest_id_marketing': 'v1%3A174887429613421182',
    'guest_id_ads': 'v1%3A174887429613421182',
    'guest_id': 'v1%3A174887429613421182',
    'ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog': '%7B%22distinct_id%22%3A%2201977a38-7e0e-7791-ba50-491acdfa4ac3%22%2C%22%24sesid%22%3A%5B1750102450100%2C%2201977a38-7e0e-7791-ba50-4918119bee2e%22%2C1750102212110%5D%7D',
    'personalization_id': '"v1_6/k/Z4FCL9Ka7UGoxumAOQ=="',
    'kdt': 'Mn3Kn7Vq2EddWk0DMSx1nkoM9d80ux2yxA5uqFer',
    'auth_token': '279f5730ca35170bdb3a4d8ca02f0e580fe200bb',
    'ct0': 'aa7a76a8a6dce7083aa732caaa3b65dd2c1ec056e84bc52f4e7eaaa4108872a9e0edb12dd454631850cae5af2d8c88bd0edc588423d11918dafbbb094c7776b38c6930af30e070839347373e16b92026',
    'twid': 'u%3D1933173310105284608',
    'lang': 'en',
    'external_referer': 'padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D',
    '__cf_bm': 'vKamq84f9RAvmZzXF2d3o1kgoLtsc1Ytzr2QSfbFsOs-1750283887-1.0.1.1-I_OOUX9HCR.7wdnQfaK06jLV_W41vEgF6sYJKtcPfYnnUwUUQgOVtzxQKhe4_aYnCo7u9Fqz0PvH08L11hYkHREPB3JIa1TfngeBkR7QNKU',
  }

  params = {
    "variables": f'{{"userId":"{userId}","count":20, "includePromotedContent":false, "withCommunity":true,"withVoice":true}}',
    'features': '{"rweb_video_screen_enabled":false,"payments_enabled":false,"profile_label_improvements_pcf_label_in_post_enabled":true,"rweb_tipjar_consumption_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"premium_content_api_read_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"responsive_web_grok_analyze_button_fetch_trends_enabled":false,"responsive_web_grok_analyze_post_followups_enabled":true,"responsive_web_jetfuel_frame":false,"responsive_web_grok_share_attachment_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"responsive_web_grok_show_grok_translated_post":false,"responsive_web_grok_analysis_button_from_backend":true,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_grok_image_annotation_enabled":true,"responsive_web_enhance_cards_enabled":false}',
    'fieldToggles': '{"withArticlePlainText":false}',
  
  }

  #todo: replace with some chromedp logic to refresh the cookies
  #csrf and client transaction are needed, but have a super long TTL?
  headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'content-type': 'application/json',
    'priority': 'u=1, i',
    'referer': 'https://x.com/realDonaldTrump/with_replies?lang=en',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-client-transaction-id': 'r3JH6ePkfOaRaqFx7Hj+3831P+5AIT2BVZLFZwAgu/NXOQP9zgz540YMszCexk7a9th8rKueiO4368m1jluwuIsVHV+mrA',
    'x-csrf-token': 'aa7a76a8a6dce7083aa732caaa3b65dd2c1ec056e84bc52f4e7eaaa4108872a9e0edb12dd454631850cae5af2d8c88bd0edc588423d11918dafbbb094c7776b38c6930af30e070839347373e16b92026',
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'en',
    'x-xp-forwarded-for': '7ef6e1c0cde24a6a8f811b400f6ac00bcd6efe5c738713412b9c6282cff1d2e2ab99981d2b01f87fa56b31b33b7538f13135d3d6effba29519bfb6cb33ea32887f3b6b649b0da15683e0ac608087dbcac118288b738afbf64bcc789f9a807780e0a5297c9f0dbee3eccbf7d56d47463b2e13a6fed115c95bd6838631690a28256910b0764e2b27a56978bfff7820bd32e18e86e54037261dd8e10433d0d7f5127ec052e6e26cbd6ba9d59a71221a668c55c4c85ca2c1451ca62c1b3e13a3917b1f7f477c4748946c500a29485a5e556800a5b40b643e0e8680d747f776f06fb4627dfe45e08b8b82a27304eafd7f33471034d799c553043ab7c9e84a349a6fa443',
    # 'cookie': 'guest_id_marketing=v1%3A174887429613421182; guest_id_ads=v1%3A174887429613421182; guest_id=v1%3A174887429613421182; ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog=%7B%22distinct_id%22%3A%2201977a38-7e0e-7791-ba50-491acdfa4ac3%22%2C%22%24sesid%22%3A%5B1750102450100%2C%2201977a38-7e0e-7791-ba50-4918119bee2e%22%2C1750102212110%5D%7D; personalization_id="v1_6/k/Z4FCL9Ka7UGoxumAOQ=="; kdt=Mn3Kn7Vq2EddWk0DMSx1nkoM9d80ux2yxA5uqFer; auth_token=279f5730ca35170bdb3a4d8ca02f0e580fe200bb; ct0=aa7a76a8a6dce7083aa732caaa3b65dd2c1ec056e84bc52f4e7eaaa4108872a9e0edb12dd454631850cae5af2d8c88bd0edc588423d11918dafbbb094c7776b38c6930af30e070839347373e16b92026; twid=u%3D1933173310105284608; lang=en; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; __cf_bm=vKamq84f9RAvmZzXF2d3o1kgoLtsc1Ytzr2QSfbFsOs-1750283887-1.0.1.1-I_OOUX9HCR.7wdnQfaK06jLV_W41vEgF6sYJKtcPfYnnUwUUQgOVtzxQKhe4_aYnCo7u9Fqz0PvH08L11hYkHREPB3JIa1TfngeBkR7QNKU',
  }
  
  #fetches user replies
  url = "https://x.com/i/api/graphql/Z9gIrY5Gq-2K7HXhIimlyQ/UserTweetsAndReplies"

  #special for the first call, because we need to get the first cursor
  response = requests.get(url, headers=headers, params=params, cookies=cookies)

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
      print (i)
      sleep(randint(4, 7))  # Sleep to avoid rate limiting

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