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

label = {
    0: "Manually forgot on",
    1: "Rated AGAIN on",  # again
    2: "Rated HARD on",  # hard
    3: "Rated GOOD on",  # good
    4: "Rated EASY on" # easy
}

def init(card):
    cmd = f"select ease, id, ivl, factor from revlog where cid = '{card.id}' ORDER BY id ASC "
    rating_list = mw.col.db.all(cmd)

    # aqt.utils.showText(str(rating_list))

    if (len(rating_list) > 0):
        javascript = """

              $('#squares').append(
    
              '<div class = "square tooltip" style = "background-color: %s">  <span class="tooltiptext">%s <br> %s <br> <br> Ease: %s <br> Ivl: %s </span> </div>'
    
              )
             """

        combiner = "append" if (config["vertical-position"] == "bottom") else "prepend"

        container = """
            (function(){
                $('#legend').remove()
                $("#legend-container").remove()
                $('#qa').%s(`
            
            
                <div id = "legend-container">
                   <div id = "legend">  
                        <div id = "squares">
                         </div> 
                    </div>
                </div>
               
                `)
             
            """ % (combiner)

        if config["show-label"] == "true":
            container += ("""
               $('#legend').prepend(`
                    <span class = "legend-label" > Card Rating <br> History </span>    <div class="vl">
                        </div>
                `)
            """)

        for index, element in enumerate(rating_list):
            # aqt.utils.showText(str(element[1]))
            if (element[1] > 0):


                if (element[2] <= 0):
                    interval = findNearestTimeMultiple(abs(element[2])) + ""
                else:
                    interval = str(element[2]) + " days" if (element[2] < 30) else str(element[2] // 30) + " months"

                ease = str(element[3] // 10) + "%" if (element[3] > 0) else "learning"

                container += (javascript % (colors[element[0]], label[element[0]], datetime.datetime.fromtimestamp(element[1]/1000).strftime('%Y-%m-%d <br> %I:%M %p') ,ease , interval



                                            ))

        zoom = config["size"]

        container += """ 
                $('head').append(`
                 <style id="legend-style">
                 .square {
                      height: 20px;
                      width: 20px;
                      margin: 5px;
                      border-radius: 5px;
                  }

                #legend{
                    display: flex;
                    justify-content: center;
                    border-radius: 5px;
                    width: max-content;
                    padding: 5px;
                    margin-top: 20px;
                    margin-bottom: 20px;
                    padding-left: 5px;
                    padding-right: 5px;
                    border-radius: 10px;
                    background-color: #F0F0F0;
                    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
                }
                
                .night_mode #legend{
                    background-color: #46464A;
                }
   
                .tooltip {
                  position: relative;
                  display: inline-block;
                }
                
                .tooltip .tooltiptext {
                  visibility: hidden;
                  width: 200px;
                  max-width: 700px;
                  background-color: black;
                  font-family:  ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace!important;
                  color: #fff;
                  text-align: center;
                  border-radius: 6px;
                  padding: 5px 0;
                  position: absolute;
                  z-index: 1;
                  top: 200%;
                  left: 50%;
                  font-size: 20px;
                  margin-left: -100px;
                }

                .tooltip .tooltiptext::after {
                  content: "";
                  position: absolute;
                  bottom: 100%;
                  left: 50%;
                  margin-left: -5px;
                  border-width: 5px;
                  border-style: solid;
                  border-color: transparent transparent black transparent;
                }
  
                .tooltip:hover .tooltiptext {
                  visibility: visible;
                }
                
                #squares{
                    display: flex;
                    align-items: center;
                    max-width: 660px;
                    flex-wrap: wrap;
                }
                
                .legend-label{
                    display: flex;
                    align-items: center;
                    text-align: center;
                    font-weight: 1000;
                    font-size: 15px;
                    font-family:  ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace!important;
                    padding-left: 8px;
                    color: #CACACA;
                }
                
                .night_mode .legend-label{
                    color: #75757A;
                }
                
                #legend-container{
                    display: flex;
                    justify-content: center;
                }
            
                 .vl {
                    border-left: 2px solid #75757A;
                    margin-left: 10px;
                    margin-right: 10px;
                    align-self: center;
                    height: 29px;
                     }
                </style>`
                )  })() """

        # aqt.utils.showText(container)

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
    elif (seconds < 2.628e+6):
        return str(seconds // 86400) + " days"
    else:
        return str(seconds // 2.628e+6) + " months"






