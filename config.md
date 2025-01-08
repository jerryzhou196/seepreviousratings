**If you are here to remove the "Card Rating History" label, change <i> Show Label </i> to "false"** 

# Configuration Options

### `show_label`
- Controls visibility of the "Card Rating History" label
- Default: "true"
- Valid values: "true" or "false"

### `limit_number`
- Maximum number of review history squares to display
- Default: "30"
- Accepts positive integers

### `size`
- Controls the CSS zoom level of the rating history display
- Default: "100%"
- Uses percentage values (e.g., "75%", "150%")

### `width`
- Controls the width of the rating history display
- Default: "inherit"
- Accepts CSS width values (e.g., "100px", "50%")

### `vertical_position`
- Determines whether the rating history appears at the top or bottom of the reviewer
- Default: "bottom"
- Valid values: "top" or "bottom"

### `constantly_show_addon`
- Determines if the rating history should show on both question and answer sides
- Default: "false"
- When "false", only shows on the answer side
- When "true", shows on both question and answer sides

## Color Settings

### `manually_forgot_color`
- Color for manually forgotten cards
- Default: "white"
- Accepts CSS color values (hex, rgb, or color names)

### `rated_again_color`
- Color for cards rated "Again"
- Default: "#c03c1c"
- Accepts CSS color values

### `rated_hard_color`
- Color for cards rated "Hard"
- Default: "#D8A700"
- Accepts CSS color values

### `rated_good_color`
- Color for cards rated "Good"
- Default: "#B9D870"
- Accepts CSS color values

### `rated_easy_color`
- Color for cards rated "Easy"
- Default: "#006344"
- Accepts CSS color values

### `only_show_learning_reviews_in_learning_stage`
- Controls whether to show learning reviews for cards not in the learning stage
- Default: "true"
- When "true", only shows learning reviews for cards currently in learning

### `dont_show_reviews_before_manually_forgot`
- Controls whether to hide reviews that occurred before a manual forget
- Default: "false"
- When "true", clears history before manually forgotten cards

## Notes
- All boolean values should be specified as strings ("true" or "false")
- Color values can be any valid CSS color format
- The add-on will automatically adjust its display based on these settings
- Invalid configurations will fall back to default values
