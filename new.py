from aqt import gui_hooks
from aqt import mw
import datetime
import logging
import os
from typing import Dict, Tuple, List, Dataclass, Optional

# Set up logger
logger = mw.addonManager.get_logger(__name__)
if os.environ.get("ANKIDEV"):
    logger.setLevel(logging.DEBUG)

@dataclass
class ReviewConfig:
    """Configuration settings for the add-on"""
    manually_forgot_color: str
    rated_again_color: str
    rated_hard_color: str
    rated_good_color: str
    rated_easy_color: str
    show_label: bool
    constantly_show_addon: bool
    vertical_position: str
    size: str
    width: str
    limit_number: int
    only_show_learning_reviews_in_learning_stage: bool

    def __post_init__(self):
        logger.debug(f"ReviewConfig initialized with: {self.__dict__}")

    def get_color_map(self) -> Dict[int, str]:
        """Map review ratings to their corresponding colors"""
        color_map = {
            0: self.manually_forgot_color,
            1: self.rated_again_color,
            2: self.rated_hard_color,
            3: self.rated_good_color,
            4: self.rated_easy_color
        }
        return color_map

class ReviewHistory:
    """Handles review data processing and statistics"""
    def __init__(self, config: ReviewConfig):
        self.config = config
        self.stats = {
            'again': 0,
            'hard': 0, 
            'good': 0,
            'easy': 0
        }
        logger.debug("ReviewHistory initialized")
        
    def process_review(self, review: Tuple, sched_ver: int) -> Dict:
        """Process a single review entry and return formatted data"""
        try:
            rating, time_ms, raw_ivl, raw_ease, raw_type = review
            logger.debug(f"Processing review: rating={rating}, time={time_ms}, interval={raw_ivl}, ease={raw_ease}, type={raw_type}")
            
            interval = self._format_interval(raw_ivl)
            ease = f"{raw_ease // 10}%" if raw_ease != 0 else "N/A"
            date = datetime.fromtimestamp(time_ms / 1000).strftime('%Y-%m-%d <br> %I:%M %p')
            
            # Handle scheduler v1 special case
            if sched_ver == 1 and raw_type != 1 and rating != 1:
                logger.debug(f"Adjusting rating for scheduler v1: {rating} -> {rating + 1}")
                rating += 1
                
            self._update_stats(rating)
            
            result = {
                'color': self.config.get_color_map()[rating],
                'label': self.config.labels[rating],
                'date': date,
                'ease': ease,
                'interval': interval,
                'review_type': self.config.types[raw_type]
            }
            logger.debug(f"Processed review data: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing review: {str(e)}", exc_info=True)
            raise

# class TemplateManager:
#     """Manages HTML templates and rendering"""
#     def __init__(self, config: ReviewConfig):
#         self.config = config
#         self._build_styles()
#         self.html = """
#             <div id = "legend-container">
#                 <div id = "legend">  
#                     <div id = "squares">
#                     </div> 
#                 </div>
#             </div>
#         """

#     def (self)-> str:
#         inject_styles = """
#             $('head').append(`
#                 <style id="legend-style">
#                 .square {
#                     height: 20px!important;
#                     width: 20px!important;
#                     margin: 5px!important;
#                     border-radius: 5px!important;
#                 }

#             .night_mode #legend{
#                 background-color: #46464A!important;
#             }

#             .tooltip {
#                 position: relative!important;
#                 display: inline-block!important;
#             }

#             .tooltip .tooltiptext {
#                 visibility: hidden!important;
#                 width: 200px!important;
#                 max-width: 700px!important;
#                 background-color: black!important;
#                 font-family:  ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace!important;
#                 color: #fff!important;
#                 text-align: center!important;
#                 border-radius: 6px!important;
#                 padding: 5px 0!important;
#                 position: absolute!important;
#                 z-index: 1!important;
#                 top: 200%!important;
#                 left: 50%!important;
#                 font-size: 20px!important;
#                 margin-left: -100px!important;
#                 line-height: normal !important;
#             }

#             .tooltip .tooltiptext::after {
#                 content: ""!important;
#                 position: absolute!important;
#                 bottom: 100%!important;
#                 left: 50%!important;
#                 margin-left: -5px!important;
#                 border-width: 5px !important;
#                 border-style: solid !important;
#                 border-color: transparent transparent black transparent !important;
#             }

#             .tooltip:hover .tooltiptext {
#                 visibility: visible !important;
#             }

#             #squares{
#                 display: flex !important;
#                 align-items: center !important;
#                 max-width: 660px !important;
#                 flex-wrap: wrap !important;
#             }

#             .legend-label{
#                 display: flex !important;
#                 align-items: center !important;
#                 text-align: center !important;
#                 font-weight: 1000 !important;
#                 font-size: 15px !important;
#                 font-family:  ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace!important;
#                 padding-left: 8px !important;
#                 color: #CACACA !important;
#             }

#             .night_mode .legend-label{
#                 color: #75757A !important;
#             }

#             #legend-container{
#                 display: flex !important;
#                 justify-content: center !important;
#             }

#                 .vl {
#                 border-left: 2px solid #75757A !important;
#                 margin-left: 10px !important;
#                 margin-right: 10px !important;
#                 align-self: center !important;
#                 height: 29px !important;
#                     }

#             #legend{
#                 direction: ltr !important;
#                 display: flex !important;
#                 justify-content: center !important;
#                 border-radius: 5px !important;
#                 width: max-content !important;
#                 padding: 5px !important;
#                 margin-top: 20px !important;
#                 margin-bottom: 20px !important;
#                 padding-left: 5px !important;
#                 padding-right: 5px !important;
#                 border-radius: 10px !important;
#                 background-color: #F0F0F0 !important;
#                 box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19) !important;
#                 line-height: normal !important;
#         """

#         user_changeable = '''
#             width: %s!important;
#             zoom: %s!important;
#         ''' % (self.config.width, self.config.size)

#         closing_tag = ''' } </style>` )  })() '''

#         logger.debug(f"Injecting styles: {inject_styles + (user_changeable + closing_tag)}")

#         return inject_styles + (user_changeable + closing_tag)
        
    def render_history(self, reviews: List[Dict], stats: Dict, total: int) -> str:
        """Render the complete history visualization"""
        try:
            logger.debug(f"Rendering history with {len(reviews)} reviews")
            squares_html = self._render_squares(reviews)
            stats_html = self._render_stats(stats, total)
            
            html = self.base_template.format(
                squares=squares_html,
                stats=stats_html,
                styles=self.styles
            )
            logger.debug("History rendered successfully")
            return html
        except Exception as e:
            logger.error(f"Error rendering history: {str(e)}", exc_info=True)
            raise

class CardHistoryAddon:
    """Main add-on class managing the visualization"""
    def __init__(self):
        try:
            logger.info("Initializing Card History Add-on")
            self.config = ReviewConfig(**mw.addonManager.getConfig(__name__))
            self.history = ReviewHistory(self.config)
            self.template = TemplateManager()
            self._setup_hooks()
            logger.info("Add-on initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize add-on: {str(e)}", exc_info=True)
            raise

    def _setup_hooks(self):
        """Configure Anki hooks based on add-on settings"""
        try:
            if self.config.constantly_show_addon:
                # logger.debug("Setting up hooks for constant display")
                gui_hooks.reviewer_did_show_question.append(self.render_widget)
                gui_hooks.reviewer_did_show_answer.append(self.render_widget)
            else:
                # logger.debug("Setting up hooks for answer-only display")
                gui_hooks.reviewer_did_show_question.append(self.unrender_widget)
                gui_hooks.reviewer_did_show_answer.append(self.render_widget)
        except Exception as e:
            logger.error(f"Error setting up hooks: {str(e)}", exc_info=True)
            raise

    def _process_reviews(self, reviews: List[Tuple]) -> List[Dict]:
        """Process all reviews and apply configured limits"""
        try:
            processed_reviews = []
            sched_ver = mw.col.schedVer()
            
            for review in reviews:
                if not self._should_show_review(review):
                    continue
                    
                processed = self.history.process_review(review, sched_ver)
                if processed:
                    processed_reviews.append(processed)

            # Apply configured limit
            if len(processed_reviews) > self.config.limit_number:
                processed_reviews = processed_reviews[-self.config.limit_number:]
                
            logger.debug(f"Processed {len(processed_reviews)} reviews")
            return processed_reviews
            
        except Exception as e:
            logger.error(f"Error processing reviews: {str(e)}", exc_info=True)
            raise

    def _should_show_review(self, review: Tuple) -> bool:
        """Determine if a review should be shown based on configuration"""
        try:
            if not self.config.only_show_learning_reviews_in_learning_stage:
                return True
                
            _, _, _, _, review_type = review
            return review_type == 0  # Show only learning reviews
            
        except Exception as e:
            logger.error(f"Error checking review visibility: {str(e)}", exc_info=True)
            return False

    def render_widget(self, card: Card) -> None:
        """Initialize the card history display"""
        try:
            cmd = "select ease, id, ivl, factor, type from revlog where cid = ? ORDER BY id ASC"
            reviews = mw.col.db.all(cmd, [card.id])
            if not reviews: 
                return 

            processed_reviews = self._process_reviews(reviews)
            mw.reviewer.web.eval(html)
            logger.debug("Card history display initialized")
            
        except Exception as e:
            logger.error(f"Error initializing card history: {str(e)}", exc_info=True)
            self.unrender_widget(card)

    def unrender_widget(self) -> None:
        """Remove the card history display"""
        try:
            cleanup_js = """
                (function() {
                    document.getElementById('legend-container')?.remove();
                    document.getElementById('legend')?.remove();
                })();
            """
            mw.reviewer.web.eval(cleanup_js)
        except Exception as e:
            logger.error(f"Error removing card history: {str(e)}", exc_info=True)


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
    limitNum = int(config['limit-number'])
    lenOfallData = len(allData)

    if (limitNum >= lenOfallData):
        for i in range(lenOfallData):
            container += javascript % (allData[i]['color'], allData[i]['label'], allData[i]['date'], allData[i]['ease'], allData[i]['interval'], allData[i]['reviewType'])
    else:
        for i in range(limitNum):
            a = lenOfallData - limitNum + i
            container += javascript % (allData[a]["color"], allData[a]["label"], allData[a]["date"], allData[a]["ease"], allData[a]["interval"], allData[a]["reviewType"])

    return container

# Initialize the add-on
try:
    addon = CardHistoryAddon()
    logger.info("Card History Add-on loaded successfully")
except Exception as e:
    logger.error(f"Failed to load add-on: {str(e)}", exc_info=True)
    raise
