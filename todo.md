Steps: 
    <!-- - If website is youtube, detect the category by scraping the html page. -->
    - Change the way data is entered every 5 minutes and every new day:
            - For every 5 minutes:
                    - If an online activity, check if its youtube or any other website. In case of youtube, use youtube's categorization map other wise check if the domain is present in the categorization map or not. If yes, Add 5 minutes to the respective category, otherwise simply add it to the uncategorized_category["website"] as a list of domains. 
                    - For an offline activity, use the "offline" section of categorization map. If there is an entry, then add 5 to the respective category, otherwise add the activity within uncategorised_category["offline"] as a list of activities.
            
            - For everyday:
                  - Take all the uncategorised_data from the previous AVAILABLE date.
                  - Update the browser_history_log with respective "websites" and "offline" data from the uncategorised_data by incrementing count values associated to them.
    
    - Change display function to show bar chart of all activities, where each category's bar will have sub-division for each activity. The uncategorised bar will just show one color.
    
    - Don't ask for categorization when count <=1 .

    - How to close a tab when quota is completed. 
    - Private category in anomaly. Find a way to distinguish between new Tab and private tab
    - Add code in timer.py to detect private browsing
    <!-- - Just after installation, read history from browser, and count frequency of website which are un-categorised. Ask the user for a few suggestions. -->
    <!-- - Make a legend mapping all system program names to human readable names to be referenced before making the bar graph -->
    