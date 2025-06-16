import requests

def convert_username(handle: str):
    params = {
      "variables":
      f'{{"screen_name":"{handle}"}}}}',
      "features": '{"responsive_web_grok_bio_auto_translation_is_enabled":false,"hidden_profile_subscriptions_enabled":true,"payments_enabled":false,"profile_label_improvements_pcf_label_in_post_enabled":true,"rweb_tipjar_consumption_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"subscriptions_feature_can_gift_premium":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
    }

    headers = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "Cookie": 'guest_id_marketing=v1%3A174973919619409054; guest_id_ads=v1%3A174973919619409054; guest_id=v1%3A174973919619409054; __cf_bm=6yYWavQIsUQaFnidE83l1bhunGxikyMzM6COWmh7MhQ-1749739196-1.0.1.1-5N9xy5qtGOongNSELs0kTfHzPeW2dRkaFpvoV6jofVLw_P7Z9uBlgWjFFdiWZZsdcoY_gF7sIn9j7MebI2TlHSXQqK3pK4Jn5Gq0Mw4cfgE; gt=1933172420132635092; personalization_id="v1_3i/stAuLGUyrhwLFbjjX5g=="; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGMTl2SXAToMY3NyZl9p%250AZCIlNmUwZjIxNTU3NjIzMWNkNDNiOTM4ZTRjNzVlOTk0YmQ6B2lkIiUzNjk2%250AZjJmYzhiMmJjYWM5Nzc4ODkyZWRiNDI1MDA0MA%253D%253D--32c4e0943c6c2d9683bd573c026c92bb80378a4a; kdt=J3yDI0583qJLK1GkL3EWOI7mIJl2J3Ym1QSnSKSn; auth_token=bbf24dbe0498ea1f781c916f8b87eb28c9f73c79; ct0=a86f3acf802295821c56f0417cd0d7ed9a13ebe411590b799b76bf138a25e6c7ca2ba1a0e029a986a518e6e424335035b2e42a09bc028a76482253a78d1deaa667ad5d766a311561fa5b7e3d6da4a0b5; lang=en; twid=u%3D1933173310105284608',
        "X-Csrf-Token": "a86f3acf802295821c56f0417cd0d7ed9a13ebe411590b799b76bf138a25e6c7ca2ba1a0e029a986a518e6e424335035b2e42a09bc028a76482253a78d1deaa667ad5d766a311561fa5b7e3d6da4a0b5"
    }

    url = "https://x.com/i/api/graphql/jUKA--0QkqGIFhmfRZdWrQ/UserByScreenName"

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        userId = data['data']['user']['result']['rest_id']
        if userId:
            print(f"User ID for @{handle}: {userId}")
            return userId
        else:
            print("User not found or no data available.")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None