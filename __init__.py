from aqt import gui_hooks
from aqt import mw
import datetime

# import aqt

config = mw.addonManager.getConfig(__name__)

colors = {
    0: config['manually-forgot-color'],
    1: config['rated-again-color'], #again
    2: config["rated-hard-color"], #hard
    3: config["rated-good-color"], #good
    4: config["rated-easy-color"] #easy
}

labels = {
    0: "Manually <br> FORGOT on",
    1: "Rated AGAIN on",  # again
    2: "Rated HARD on",  # hard
    3: "Rated GOOD on",  # good
    4: "Rated EASY on" # easy
}

types = {
    0: "(Learning)",
    1: "(Review)",
    2: "(Relearn)",
    3: "(Custom Study)",
    4: ""
}

def init(card):
    cmd = f"select ease, id, ivl, factor,type from revlog where cid = '{card.id}' ORDER BY id ASC "
    rating_list = mw.col.db.all(cmd)

    showLearning = True if (config["show-learning-stage-reviews"] == "true" ) else False

    if (len(rating_list) > 0): #check if a card has an previous ratings 
        combiner = "append" if (config["vertical-position"] == "bottom") else "prepend"

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

        javascript = """

              $('#squares').append(
    
              '<div class = "square tooltip" style = "background-color: %s">  <span class="tooltiptext">%s <br> %s <br> <br> Ease: %s <br> Ivl: %s <br> %s </span> </div>'
    
              )
             """

        if config["show-label"] == "true":
            container += ("""
               $('#legend').prepend(`
                    <span class = "legend-label" > Card Rating <br> History </span>    <div class="vl">
                        </div>
                `)
            """)

        sched = mw.col.schedVer()
        for index, review in enumerate(rating_list):

            rating = review[0]
            timeInMs = review[1]
            rawIvl = review[2]
            rawEase = review[3]
            rawRevType = review[4]

            # "raw" means that the data still needs to be converted to a different format 

            if (timeInMs > 0 and (rawRevType != 0 or showLearning == True)): # check if the card rating time is valid
                
                if (rawIvl < 0): #if the interval is negative, it is expressed in seconds (learning steps)
                    interval = findNearestTimeMultiple(abs(rawIvl)) + "" #convert seconds to nearest multiple
                elif (rawIvl < 30): #if the interval is positive, it is expressed in days 
                    interval = str(rawIvl) + " days"  
                else:
                    interval = str(rawIvl // 30) + " months" 

                if (rawEase != 0):
                    ease = str(rawEase // 10) + "%"   
                else:
                    ease = "N/A"

                if (sched == 1 and rawRevType != 1 and rating != 1): #case in 2.0 scheduler where there is no "hard" option, which requires all buttons other than "again" to offset up by 1
                    off_set = int(rating) + 1
                    color_id = colors[off_set]
                    label = labels[off_set]
                else:
                    color_id = colors[rating]
                    label = labels[rating]

                date = datetime.datetime.fromtimestamp(timeInMs/1000).strftime('%Y-%m-%d <br> %I:%M %p')

                # aqt.utils.showText(str(element[4]))

                reviewType = types[rawRevType]

                container += (javascript % (color_id, label, date, ease, interval, reviewType))

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
            
                 """

        closing_tag = ''' } </style>` )  })() '''

        user_changeable = '''
            width: %s!important;
            zoom: %s!important;
        ''' % ( config["width"], config["size"] )

        container += (user_changeable + closing_tag)

        # aqt.utils.showText(str(mw.col.schedVer()))

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

if (config["constantly-show-addon"] == "true"):
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
    elif (seconds <  2592000) :
        return str(seconds // 86400) + " days"
    else:
        return str(seconds //  2592000) + " months"
