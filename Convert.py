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
        "Cookie": 'guest_id_marketing=v1%3A174887429613421182; guest_id_ads=v1%3A174887429613421182; guest_id=v1%3A174887429613421182; gt=1934686809851617729; ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog=%7B%22distinct_id%22%3A%2201977a38-7e0e-7791-ba50-491acdfa4ac3%22%2C%22%24sesid%22%3A%5B1750102450100%2C%2201977a38-7e0e-7791-ba50-4918119bee2e%22%2C1750102212110%5D%7D; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; personalization_id="v1_6/k/Z4FCL9Ka7UGoxumAOQ=="; kdt=Mn3Kn7Vq2EddWk0DMSx1nkoM9d80ux2yxA5uqFer; auth_token=279f5730ca35170bdb3a4d8ca02f0e580fe200bb; ct0=aa7a76a8a6dce7083aa732caaa3b65dd2c1ec056e84bc52f4e7eaaa4108872a9e0edb12dd454631850cae5af2d8c88bd0edc588423d11918dafbbb094c7776b38c6930af30e070839347373e16b92026; att=1-f8nk9zEEif2H8S7anEmoiMwEi0RT0O9CUfvK5CNv; lang=en; twid=u%3D1933173310105284608; __cf_bm=_EtYjaaMMMYleKv0qARx2DQoCd0RKcAAdHzeddx06gc-1750109013-1.0.1.1-CvZTAxqkw39nMfyG68S2.W9vW8yJIUU._83ww7rtcyF3Bk.iL6C5lwcZiyidd.5giF0oobKN9YOcOMm9va4.TbM9aSVDdthPPD_BueZNgpI',
        "X-Csrf-Token": "aa7a76a8a6dce7083aa732caaa3b65dd2c1ec056e84bc52f4e7eaaa4108872a9e0edb12dd454631850cae5af2d8c88bd0edc588423d11918dafbbb094c7776b38c6930af30e070839347373e16b92026"
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