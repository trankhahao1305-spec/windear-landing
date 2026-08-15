import urllib.request
import urllib.parse
import json

app_id = "1375049340788214"
app_secret = "7d07a285be9023c6d6bd13ca49fabc23"
short_token = "EAATimZAZBBnfYBSOFWzNuP9sFLR2d5GxR25Y9W92XtbBoapJIZBz6CI0xcyLroJbYtGnSs9TjKhgOlSabOQRVZBTZBii42KvXz0GvZAAdhOPA8WFJ3ZCiZBHOrDlPwiLJ5r8HjrzPBn8atErRnStQjmwqU7EK5CHqdLeADgxKrMYP7XqDcs5QB7RrNnO9itRz9aEkuYwOoBauXvvMwZAwhE4CHGcNptZA16nFovBJinXaNZAx0tGaqdVdxRSHrXpEFPcHnAfxZA7A0afDtnpJ1nIZBB6OVwZDZD"

try:
    # Step 3.2: Exchange short-lived token for long-lived user token
    url1 = f"https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={short_token}"
    req1 = urllib.request.urlopen(url1)
    res1 = json.loads(req1.read().decode())
    long_token = res1.get("access_token")
    print(f"Long-lived User Token acquired: {long_token[:20]}...")

    # Step 3.3a: Get User ID
    url2 = f"https://graph.facebook.com/v18.0/me?access_token={long_token}"
    req2 = urllib.request.urlopen(url2)
    res2 = json.loads(req2.read().decode())
    user_id = res2.get("id")
    user_name = res2.get("name")
    print(f"User: {user_name} (ID: {user_id})")

    # Step 3.3b: Get Permanent Page Access Tokens
    url3 = f"https://graph.facebook.com/v18.0/{user_id}/accounts?access_token={long_token}"
    req3 = urllib.request.urlopen(url3)
    res3 = json.loads(req3.read().decode())
    pages = res3.get("data", [])
    
    with open("facebook_tokens_result.json", "w", encoding="utf-8") as f:
        json.dump({"user_id": user_id, "user_name": user_name, "pages": pages}, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully fetched {len(pages)} Facebook Pages!")
    for page in pages:
        print("--------------------------------------------------")
        print(f"Page Name: {page.get('name')}")
        print(f"Page ID: {page.get('id')}")
        print(f"Permanent Page Token: {page.get('access_token')}")
        print("--------------------------------------------------")

except Exception as e:
    print(f"Error: {e}")
