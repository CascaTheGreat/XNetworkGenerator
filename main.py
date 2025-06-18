if __name__ == "__main__":
    from Network import UserNetwork
    from Scraper import get_tweets
    import json
    from Convert import convert_username


    userHandle = input("Enter the Twitter handle of the user to focus on (e.g., elonmusk): ")
    userHandle = userHandle.lower().strip().replace("@", "")
    print(f"Creating network for user: {userHandle}")

    networkDepth = input("Enter the depth of the network (e.g., 1): ")
    networkDepth = int(networkDepth.strip())

    # resolve handle to user ID

    profile_id = convert_username(userHandle)
    if not profile_id:
        print("Failed to resolve user handle to user ID.")
        exit(1)

    with open("tweets.json", "w") as f:
        tweets = get_tweets(profile_id, lim=1)
        print (f"Fetched {len(tweets)} tweetcbs")
        f.write(json.dumps(tweets, indent=4))

    # Create a new network
    n = UserNetwork()

    main_user = n.add_user(userHandle, userHandle)

    with open("tweets.json", "r+") as f:
        tweets = json.load(f)

        for tweet in tweets:
            name = tweet['name'].lower()
            handle = tweet['handle'].lower()
            user_id = n.add_user(name, handle)

            n.add_friendship(main_user, user_id)
        
        for i in range(networkDepth - 1):
            for user in list(n.users):
                if user != userHandle:
                    print(f"Expanding network for user: {user}")
                    profile_id = convert_username(user)
                    if not profile_id:
                        print(f"Failed to resolve user handle {user} to user ID.")
                        continue

                    tweets = get_tweets(profile_id, lim=1)
                    print (f"Fetched {len(tweets)} tweets for {user}")

                    for tweet in tweets:
                        name = tweet['name'].lower()
                        handle = tweet['handle'].lower()
                        user_id = n.add_user(name, handle)

                        n.add_friendship(user, user_id)
      

    n.display_network(focus_user=userHandle)