from aqt import gui_hooks
from aqt import mw

config = mw.addonManager.getConfig(__name__)

colors = {
    1: config['rated-again-color'], #again
    2: config["rated-hard-color"], #hard
    3: config["rated-good-color"], #good
    4: config["rated-easy-color"] #easy
}

def init(card):
    id = card.id
    truncation = 10 #to do
    cmd = f"select ease from revlog where cid = '{id}' "
    rating_list = mw.col.db.all(cmd)

    # aqt.utils.showText(str(rating_list))

    javascript = """
          $('#legend').append(

          '<div class = "square" style = "background-color: %s">  </div>'

          )
         """
    container = """
        (function(){
            $('#legend').remove()
            $('body').append(`
               <div id = "legend"> </div>
            `)
        """

    for index, element in enumerate(rating_list):
        # aqt.utils.showText(str(element[0]))
        container += (javascript % (colors[element[0]]))

    container += "})()"

    # aqt.utils.showText(container)

    mw.reviewer.web.eval(container)

def setUpLegend(new_state, old_state):
       if (new_state == 'review'):
           from aqt import mw
           # aqt.utils.showText(str(dir(mw.reviewer)))
           mw.reviewer.web.eval("""
           (function () {
             // innerHTML of style element is read-only. remove & recreate css
             $('#legend-style').remove()
             $('head').append(`
                 <style id="legend-style">
                 .square {
                      height: 15px;
                      width: 15px;
                      margin: 5px;
                      border-radius: 5px;
                  }

                  #legend{
                      display: flex;
                      justify-content: center;
                      border-radius: 5px;
                      width: max-content;
                      margin: auto;
                      margin-top: 20px;
                  }
                  </style>
                  `)   
           })()
           """)


gui_hooks.reviewer_did_show_question.append(init)
gui_hooks.state_did_change.append(setUpLegend)



