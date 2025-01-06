from aqt import gui_hooks
from aqt import mw
from aqt import utils
import datetime

class ReviewConfig:
    """Configuration settings for the add-on"""
    config: dict = mw.addonManager.getConfig(__name__)
    size: str = "100%"
    width: str = "inherit"
    vertical_position: str = "bottom"
    show_label: str = "true"
    constantly_show_addon: str = "false"
    manually_forgot_color: str = "white"
    rated_again_color: str = "#c03c1c"
    rated_hard_color: str = "#D8A700"
    rated_good_color: str = "#B9D870"
    rated_easy_color: str = "#006344"
    only_show_learning_reviews_in_learning_stage: str = "true"
    dont_show_reviews_before_manually_forgot: str = "false"
    limit_number: int = 5

    def __init__(self):
        try:
            self.size = self.config.get('size', self.size)
            self.width = self.config.get('width', self.width)
            self.vertical_position = self.config.get('vertical_position', self.vertical_position)
            
            # Handle boolean string values
            self.show_label = str(self.config.get('show_label', self.show_label)).lower()
            self.constantly_show_addon = str(self.config.get('constantly_show_addon', self.constantly_show_addon)).lower()
            self.only_show_learning_reviews_in_learning_stage = str(self.config.get(
                'only_show_learning_reviews_in_learning_stage', 
                self.only_show_learning_reviews_in_learning_stage
            )).lower()

            self.dont_show_reviews_before_manually_forgot = str(self.config.get(
                'dont_show_reviews_before_manually_forgot', 
                self.dont_show_reviews_before_manually_forgot
            )).lower()
            
            # Handle color values
            self.manually_forgot_color = self.config.get('manually_forgot_color', self.manually_forgot_color)
            self.rated_again_color = self.config.get('rated_again_color', self.rated_again_color)
            self.rated_hard_color = self.config.get('rated_hard_color', self.rated_hard_color)
            self.rated_good_color = self.config.get('rated_good_color', self.rated_good_color)
            self.rated_easy_color = self.config.get('rated_easy_color', self.rated_easy_color)
            
            # Handle numeric value
            try:
                limit_number = self.config.get('limit_number', str(self.limit_number))
                self.limit_number = int(limit_number.strip())
            except (ValueError, AttributeError):
                pass  # Keep default value
                
        except Exception as e:
            utils.showText(f"Warning: There is an invalid config in the See Previous Ratings Addon: {str(e)}")

    def is_true(self, value: str) -> bool:
        """Convert string boolean to Python boolean"""
        return value.lower() == "true"

config = ReviewConfig()

colors = {
    0: config.manually_forgot_color,
    1: config.rated_again_color,  # again
    2: config.rated_hard_color,  # hard
    3: config.rated_good_color,  # good
    4: config.rated_easy_color  # easy
}

labels = {
    0: "Manually <br> FORGOT on",
    1: "Rated AGAIN on",  # again
    2: "Rated HARD on",  # hard
    3: "Rated GOOD on",  # good
    4: "Rated EASY on"  # easy
}

types = {
    0: "(Learning)",
    1: "(Review)",
    2: "(Relearn)",
    3: "(Filtered)",
    4: "(Manual)",
    5: "(Rescheduled)"
}


def init(card):

    # Revlog Schema: 
    # id: Primary key, timestamp in milliseconds
    # cid: Card ID this review belongs to
    # usn: Update sequence number used for syncing
    # ease: Button pressed (1-4) or 0 for manual reschedule
    # ivl: New interval (positive = days, negative = seconds)
    # lastIvl: Previous interval
    # factor: Ease factor (stored as 10x the percentage, e.g. 2500 = 250%)
    # time: Review time taken in milliseconds
    # type: Review type (0=learn, 1=review, 2=relearn, 3=filtered, 4=manual, 5=rescheduled)
    
    cmd = f"select ease, id, ivl, factor, type from revlog where cid = '{card.id}' ORDER BY id ASC "
    card_review_history: list[tuple[int, int, int, int, int]] = mw.col.db.all(cmd)

    n = len(card_review_history)

    if (n > 0):  
        combiner = "append" if (config.vertical_position == "bottom") else "prepend"

        # Remove the legend if it exists
        # Create a new legend container
        container = """
                  (function(){
                      $('#legend').remove()
                      $("#legend-container").remove()
                      $('body').%s(`
                      <div id = "legend-container">
                         <div id = "legend">  
                              <div id = "squares">
                               </div> 
                          </div>
                      </div>

                      `)

                  """ % (combiner)

        sched = mw.col.schedVer()

        # The total number of statistics
        againSum = 0 # again
        hardSum = 0 # hard
        goodSum = 0 # good
        easySum = 0 # easy

        # The data of review statistics
        allData = []

        for review in card_review_history:

            # Rating Number Mapping 
            # 0: Manually FORGOT
            # 1: Rated AGAIN
            # 2: Rated HARD
            # 3: Rated GOOD
            # 4: Rated EASY
            # 5: Rescheduled
            rating: int = review[0]

            # Time in milliseconds when the card was reviewed
            reviewDateMs: int = review[1]

            # New Interval After Review
            rawIvl: int = review[2]

            # Ease factor
            rawEase: int = review[3]

            # Review Type
            # 0: Learning
            # 1: Review
            # 2: Relearn
            # 3: Filtered
            # 4: Manual
            # 5: Rescheduled
            rawRevType: int = review[4]
                
            if (reviewDateMs > 0):  # check if the card rating time is valid

                # if the review type is 0, the card is not in learning stage, and it's been explictly configured to be on 
                if (config.is_true(config.only_show_learning_reviews_in_learning_stage) and 
                    rawRevType == 0 and 
                    card_review_history[n - 1][4] != 0):
                    continue
                    
                if (rawIvl < 0):  # if the interval is negative, it is expressed in seconds (learning steps)
                    interval = findNearestTimeMultiple(abs(rawIvl)) + ""  # convert seconds to nearest multiple
                elif (rawIvl < 30):  # if the interval is positive, it is expressed in days
                    interval = str(rawIvl) + " days"
                else:
                    interval = str(rawIvl // 30) + " months"

                if (rawEase != 0):
                    ease = str(rawEase // 10) + "%"
                else:
                    ease = "N/A"

                if (config.is_true(config.dont_show_reviews_before_manually_forgot) and rating == 0):
                    allData = []
                    continue

                if (sched == 1 and rawRevType != 1 and rating != 1):  # case in 2.0 scheduler where there is no "hard" option, which requires all buttons other than "again" to offset up by 1
                    off_set = int(rating) + 1
                    againSum, hardSum, goodSum, easySum = countNumberOfTimes(off_set, againSum, hardSum, goodSum, easySum)
                    color_id = colors[off_set]
                    label = labels[off_set]
                else:
                    againSum, hardSum, goodSum, easySum = countNumberOfTimes(rating, againSum, hardSum, goodSum, easySum)
                    color_id = colors[rating]
                    label = labels[rating]

                date = datetime.datetime.fromtimestamp(reviewDateMs / 1000).strftime('%Y-%m-%d <br> %I:%M %p')

                reviewType = types[rawRevType]

                singleData = {
                    "color": color_id,
                    "label": label,
                    "date": date,
                    "ease": ease,
                    "interval": interval,
                    "reviewType": reviewType,
                }

                allData.append(singleData)
        
        if (len(allData) == 0):
            return

        # add card history to the container
        container = addCardHistory(allData, container)

        if config.is_true(config.show_label):
            container += ("""
               $('#legend').prepend(`
                    <div class = "legend-label" > Card Rating <br> History <br> 
                    </div>
                    <div class="vl"></div>                    
                `)
            """)

        container += """ 
                $('head').append(`
                 <style id="legend-style">
                 .square {
                      height: 20px!important;
                      width: 20px!important;
                      margin: 5px!important;
                      border-radius: 5px!important;
                  }

                .night_mode #legend{
                    background-color: #46464A!important;
                }

                .tooltip {
                  position: relative!important;
                  display: inline-block!important;
                }

                .tooltip .tooltiptext {
                  visibility: hidden!important;
                  width: 200px!important;
                  max-width: 700px!important;
                  background-color: black!important;
                  font-family:  ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace!important;
                  color: #fff!important;
                  text-align: center!important;
                  border-radius: 6px!important;
                  padding: 5px 0!important;
                  position: absolute!important;
                  z-index: 1!important;
                  top: 200%!important;
                  left: 50%!important;
                  font-size: 20px!important;
                  margin-left: -100px!important;
                  line-height: normal !important;
                }

                .tooltip .tooltiptext::after {
                  content: ""!important;
                  position: absolute!important;
                  bottom: 100%!important;
                  left: 50%!important;
                  margin-left: -5px!important;
                  border-width: 5px !important;
                  border-style: solid !important;
                  border-color: transparent transparent black transparent !important;
                }

                .tooltip:hover .tooltiptext {
                  visibility: visible !important;
                }

                #squares{
                    display: flex !important;
                    align-items: center !important;
                    max-width: 660px !important;
                    flex-wrap: wrap !important;
                }

                .legend-label{
                    display: flex !important;
                    align-items: center !important;
                    text-align: center !important;
                    font-weight: 1000 !important;
                    font-size: 15px !important;
                    font-family:  ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace!important;
                    padding-left: 8px !important;
                    color: #CACACA !important;
                }

                .night_mode .legend-label{
                    color: #75757A !important;
                }

                #legend-container{
                    display: flex !important;
                    justify-content: center !important;
                }

                 .vl {
                    border-left: 2px solid #75757A !important;
                    margin-left: 10px !important;
                    margin-right: 10px !important;
                    align-self: center !important;
                    height: 29px !important;
                     }

                #legend{
                    direction: ltr !important;
                    display: flex !important;
                    justify-content: center !important;
                    border-radius: 5px !important;
                    width: max-content !important;
                    padding: 5px !important;
                    margin-top: 20px !important;
                    margin-bottom: 20px !important;
                    padding-left: 5px !important;
                    padding-right: 5px !important;
                    border-radius: 10px !important;
                    background-color: #F0F0F0 !important;
                    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19) !important;
                    line-height: normal !important;
                 """

        closing_tag = ''' } </style>` )  })() '''

        user_changeable = '''
            width: %s!important;
            zoom: %s!important;
        ''' % (config.width, config.size)

        container += (user_changeable + closing_tag)

    else:
        container = """ (function(){
                      $('#legend').remove()
                      $("#legend-container").remove()
                      })()
                      """

    mw.reviewer.web.eval(container)


def unInit(card):
    mw.reviewer.web.eval("""
      (function () {
        $("#legend-container").remove()
        $("#legend").remove()
        })()
    """)

if config.is_true(config.constantly_show_addon):
    gui_hooks.reviewer_did_show_question.append(init)
    gui_hooks.reviewer_did_show_answer.append(init)

else:
    gui_hooks.reviewer_did_show_question.append(unInit)
    gui_hooks.reviewer_did_show_answer.append(init)


def findNearestTimeMultiple(seconds):
    if (seconds < 60):
        return str(seconds) + " secs"
    elif (seconds < 3600):
        return str(seconds // 60) + " mins"
    elif (seconds < 86400):
        return str(seconds // 3600) + " hours"
    elif (seconds < 2592000):
        return str(seconds // 86400) + " days"
    else:
        return str(seconds // 2592000) + " months"

def countNumberOfTimes(i, againSum, hardSum, goodSum, easySum):
    if i == 1:
        againSum += 1 # again
    elif i == 2:
        hardSum += 1 # hard
    elif i == 3:
        goodSum += 1 # good
    elif i == 4:
        easySum += 1 # easy
    else:
        pass

    return againSum, hardSum, goodSum, easySum

def addCardHistory(allData, container):
    javascript = """

            $('#squares').append(

            '<div class = "square tooltip" style = "background-color: %s">  <span class="tooltiptext">%s <br> %s <br> <br> Ease: %s <br> Ivl: %s <br> %s </span> </div>'

            )
            """
    lenOfallData = len(allData)

    for i in range(lenOfallData - 1, max(-1, lenOfallData - config.limit_number - 1), -1):
        container += javascript % (allData[i]["color"], allData[i]["label"], allData[i]["date"], allData[i]["ease"], allData[i]["interval"], allData[i]["reviewType"])

    return container
