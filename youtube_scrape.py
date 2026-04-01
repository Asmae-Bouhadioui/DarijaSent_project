from googleapiclient.discovery import build
import pandas as pd
from tqdm import tqdm

# 🔑 Put your API key here
API_KEY = "AIzaSyAoNw1ch3-IvIpjJk3PTIOCBMC1cv4ghHg"

youtube = build("youtube", "v3", developerKey=API_KEY)

# Darija keywords for filtering (mix of Latin script Darija and Arabic words)
darija_keywords = [
    "ana", "nta", "nti", "hiya", "howa", "kayen", "machi", "wach", "kifach", "fin", "imta", "chno", "hada", "hadi", "hadok", "hadik", "hna", "tam",
    "الله", "شكرا", "مرحبا", "بسم", "الحمد", "ربي", "يا", "واش", "كاين", "ماكينش", "هاد", "هادي", "هادوك", "هاديك", "هنا", "تما", "فين", "كيفاش", "شنو"
]

def is_darija(comment):
    comment_lower = comment.lower()
    return any(keyword in comment_lower for keyword in darija_keywords)

# 🔍 Search for Moroccan videos (Darija)
def search_videos(query, max_results=5):
    request = youtube.search().list(
        q=query,
        part="id",
        type="video",
        maxResults=max_results
    )
    response = request.execute()
    
    video_ids = [item["id"]["videoId"] for item in response["items"]]
    return video_ids

# 💬 Get comments
def get_comments(video_id, max_comments=200):
    comments = []
    
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )

    while request and len(comments) < max_comments:
        response = request.execute()
        
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
            
            if len(comments) >= max_comments:
                break
        
        request = youtube.commentThreads().list_next(request, response)
    
    return comments

# 🔥 MAIN
all_comments = []

queries = [
    "morocco vlog",
    "darija street interview",
    "maroc reaction",
    "casablanca vlog"
]

for query in queries:
    video_ids = search_videos(query)
    
    for vid in tqdm(video_ids):
        comments = get_comments(vid)
        filtered_comments = [c for c in comments if is_darija(c)]
        all_comments.extend(filtered_comments)

# 💾 Save dataset
df = pd.DataFrame(all_comments, columns=["text"])
df.to_csv("youtube_darija_comments2.csv", index=False, encoding="utf-8-sig")

print("Collected:", len(df), "comments")