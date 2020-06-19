Steps: 
    <!-- - (completed but failed)If website is youtube, detect the category by scraping the html page. -->
    - Change the way data is entered every 5 minutes and every new day:
            - For every 5 minutes:
                - If online activity, save it under "website" key as {site1: 2, site2: 8, site3: 1, ...}
                - If offline activity, save it under "offline" key as {activity1:2, activity2:1, activity3:7, ...}
            
            - For everyday:
                - We need to create report for the previous_date along with adding the uncategorised data to the browser_history_log file:
                
                    - First under "website" category, goto each <site> entry, find its domain and check if it is already categorised. If not, under that domain, simply append the site, and increment the count of <site_i> to the total count of that domain.

                    - 
                  - Take all the uncategorised_data from the previous AVAILABLE date.
                  - Update the browser_history_log with respective "websites" and "offline" data from the uncategorised_data by incrementing count values associated to them.
    
    - Change display function to show bar chart of all activities, where each category's bar will have sub-division for each activity. The uncategorised bar will just show one color.
    
    - Don't ask for categorization when count <=1 .

    - How to close a tab when quota is completed. 
    - Private category in anomaly. Find a way to distinguish between new Tab and private tab
    - Add code in timer.py to detect private browsing
    - Just after installation, read history from browser, and count frequency of website which are un-categorised. Ask the user for a few suggestions.
    <!-- - Make a legend mapping all system program names to human readable names to be referenced before making the bar graph -->
    