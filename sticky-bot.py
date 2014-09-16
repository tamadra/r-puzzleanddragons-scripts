import praw
import requests
import bs4
from datetime import datetime, timedelta
from descends import descends

#Date suffix
def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

#Updates the sidebar sticky every 3 days
def updateSidebarSticky():
    pad = r.get_subreddit("puzzleanddragons")
    current_sidebar = pad.get_settings()['description']
    idx1 = current_sidebar.find(START_TAG)
    idx2 = current_sidebar.find(END_TAG)
    if idx1 < 0 or idx2 < 0:
        print "Not Found"

    else:
        start_idx = idx1 + len(START_TAG);
        stickytext = current_sidebar[start_idx : idx2] 
        idx3 = stickytext.find('/comments/')
        if idx3 < 0:
            print "Not Found"

        else:
            previous_submission_id = stickytext[idx3+len('/comments/'):].split('/')[0]
            submission = r.get_submission(submission_id = previous_submission_id)            
            previous_time = datetime.fromtimestamp(submission.created_utc)
            now_time = datetime.now()
            hours_ago = (now_time - previous_time).days * 24 + (now_time - previous_time).seconds/3600
            if (hours_ago >= 60):
                print "Creating new post"
                future_date = now_time + timedelta(days=3)
                title = 'General Help & Discussion Thread.  '+now_time.strftime('%b')+" "+ord(now_time.day)+" - "+future_date.strftime('%b')+" "+ord(future_date.day)
                submit_result = r.submit(pad, title, text="###Post your questions or box help requests in this thread\n\n* Please use PadHerder to show your monster box.\n* Be specific with your questions so people have a better understanding of your needs.\n* Show some love for the people who took time to respond to your question; upvote any responses that were helpful.\n\nPrevious thread [here]("+submission.permalink+")")
                new_sidebar = current_sidebar[0:start_idx] + "\n> ## ["+title+"]("+submit_result.permalink+"?sort=new#icon-exclamation-red)  **0 Questions**\n" + current_sidebar[idx2:]         
                pad.update_settings(description=new_sidebar)
                print "New post created: "+submit_result.permalink

            else:
                print "Less than 3 days"
                submission.replace_more_comments(limit=None, threshold=0)
                num_unanswered = num_replies = 0
                for question in submission.comments:
                    replies = praw.helpers.flatten_tree(question.replies)
                    num_replies += len(replies)
                    if len(replies) == 0:
                        num_unanswered += 1
                new_sidebar = current_sidebar[0:start_idx] + "\n> ## ["+submission.title+"]("+submission.permalink+"?sort=new#icon-exclamation-red)  **"+str(len(submission.comments))+" Questions** ("+str(num_unanswered)+" unanswered) **"+str(num_replies)+" Replies**\n" + current_sidebar[idx2:]         
                pad.update_settings(description=new_sidebar)

#Updates the Descends Sticky
def updateDescendsSticky():
    pad = r.get_subreddit("puzzleanddragons")
    now = datetime.now()
    #Grab current PADwiki schedule
    soup = bs4.BeautifulSoup(requests.get("http://pad.wikia.com/wiki/Event_Schedule").content)
    #Get proper elements
    rows = soup.find("table", {"id": "currentEvents"}).find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        try:
            #Check Date
            if str(cells[0].text) == now.strftime('%m/%d 00:00\n').lstrip("0"):
                print "Found a dungeon that starts today..."
                for descend in descends:
                    #Check Descends
                    if cells[2].find('a', title=descend[0]) != None or cells[2].find('a', title=descend[0][:-1]) != None:
                        title = str(now.strftime('%m/%d').lstrip("0")) + " - " + descend[0] + " Discussion Thread"
                        #Post new sticky
                        post = r.submit(pad, title, text=descend[1])
                        post.sticky()
                        print "Posted " + str(descend[0])
        except:
            #exception required because of the table header
            pass


#Kick off main function
def main():
    global r
    global START_TAG
    global END_TAG
    START_TAG = '> [](#s1)';
    END_TAG = '> [](#s1_)';
    r = praw.Reddit(user_agent='/r/PuzzleAndDragons Sidebar Updater')
    r.config.decode_html_entities = True
    r.login('_moderators', 'password')
    updateSidebarSticky()
    #updateDescendsSticky()


if __name__ == '__main__':
    main()
