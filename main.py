if __name__ == "__main__":
    from Network import UserNetwork
    from Scraper import get_tweets
    import json
    from Convert import convert_username

    userHandle = input("Enter the Twitter handle of the user to focus on (e.g., elonmusk): ")
    print(f"Creating network for user: {userHandle}")

    # resolve handle to user ID

    profile_id = convert_username(userHandle)
    if not profile_id:
        print("Failed to resolve user handle to user ID.")
        exit(1)

    with open("tweets.json", "w") as f:
        tweets = get_tweets(profile_id, 1)
        print (f"Fetched {len(tweets)} tweets")
        f.write(json.dumps(tweets, indent=4))
    

    # Create a new network
    n = UserNetwork()

    main_user = n.add_user("Elon Musk", userHandle)

    with open("tweets.json", "r") as f:
        tweets = json.load(f)

    for tweet in tweets:
        name = tweet['name']
        handle = tweet['handle']
        user_id = n.add_user(name, handle)

        n.add_friendship(main_user, user_id)
      

    n.display_network(focus_user=userHandle)